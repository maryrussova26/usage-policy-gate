"""Verdict server for Claude Enterprise inference hooks (Owner-configured). Stdlib only.

Env: POLICY_GATE_SECRET  signing secret (whsec_...)  [required]
     POLICY_GATE_SECRET_PREV  previous secret during rotation [optional]
     POLICY_GATE_PORT (8000)  POLICY_GATE_LANG
Behaviour
* Rejects unsigned/invalid/stale requests (HTTP 401) per Anthropic's signature spec.
* Only the LATEST user message's text/attachment text is evaluated. A denied message stays in the
  transcript, so scanning history would deny every following turn.
* tool_call frames, unknown frame types, tool_result-only turns: allow.
* warn without ack -> deny with hint; block -> deny. deny_reason <= 500 chars, reference_id opaque.
* Put it behind TLS. Deploy in shadow mode first (configured on Anthropic's side).
"""
import base64
import hashlib
import hmac
import json
import os
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .i18n import render
from .validator import Validator

TOLERANCE = 300
_V = Validator()


def verify(secrets, headers, body: bytes) -> bool:
    h = {k.lower(): v for k, v in headers.items()}
    try:
        mid, ts, sigs = h["webhook-id"], h["webhook-timestamp"], h["webhook-signature"]
        signed_at = int(ts)
    except (KeyError, ValueError):
        return False
    if abs(time.time() - signed_at) > TOLERANCE:
        return False
    payload = f"{mid}.{ts}.".encode() + body
    for secret in secrets:
        try:
            key = base64.b64decode(secret.removeprefix("whsec_"), validate=True)
        except ValueError:
            continue
        expected = b"v1," + base64.b64encode(hmac.new(key, payload, hashlib.sha256).digest())
        if any(hmac.compare_digest(expected, c.encode()) for c in sigs.split()):
            return True
    return False


def last_user_text(frame: dict) -> str:
    msgs = frame.get("messages") or []
    if not msgs or msgs[-1].get("role") != "user":
        return ""
    parts = []
    for b in msgs[-1].get("content") or []:
        t = b.get("type")
        if t == "text" and b.get("text"):
            parts.append(b["text"])
        elif t == "attachment" and b.get("text"):
            parts.append(b["text"])
    return "\n".join(parts)


def decide(frame: dict, lang=None) -> dict:
    if frame.get("type") != "prompt":
        return {"action": "allow"}
    text = last_user_text(frame)
    if not text:
        return {"action": "allow"}
    v = _V.check(text, lang=lang)
    if v.allowed:
        return {"action": "allow"}
    rid = f"pg:{v.primary.rule_id}:{hashlib.sha256((frame.get('request_id') or '').encode()).hexdigest()[:8]}"
    return {"action": "deny", "deny_reason": render(v)[:500], "reference_id": rid[:50]}


def make_handler(secrets, lang):
    class H(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def _send(self, code, obj):
            b = json.dumps(obj, ensure_ascii=False).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)

        def do_POST(self):
            body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            if not verify(secrets, dict(self.headers.items()), body):
                return self._send(401, {"error": "invalid signature"})
            try:
                verdict = decide(json.loads(body), lang)
            except Exception:
                verdict = {"action": "allow"}  # fail-open on parse errors
            self._send(200, verdict)

        def log_message(self, *a):  # never log request content
            pass
    return H


def main() -> int:
    secret = os.environ.get("POLICY_GATE_SECRET")
    if not secret:
        raise SystemExit("POLICY_GATE_SECRET is required")
    secrets = [secret] + ([os.environ["POLICY_GATE_SECRET_PREV"]] if os.environ.get("POLICY_GATE_SECRET_PREV") else [])
    port = int(os.environ.get("POLICY_GATE_PORT", "8000"))
    ThreadingHTTPServer(("", port), make_handler(secrets, os.environ.get("POLICY_GATE_LANG"))).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
