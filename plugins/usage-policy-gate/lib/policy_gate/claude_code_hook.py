"""Claude Code UserPromptSubmit hook.

Register in .claude/settings.json (or ~/.claude/settings.json):
  {"hooks": {"UserPromptSubmit": [{"hooks": [{"type": "command", "command": "policy-gate-claude-code-hook"}]}]}}

Behaviour: block/warn(no ack) -> {"decision":"block","reason":...} (prompt never reaches Claude).
           note -> additionalContext hint. pass -> silent.
Env: POLICY_GATE_MODE=shadow  (never block, only add context)   POLICY_GATE_LANG=ru|en
Privacy: prompt text is never logged or sent anywhere.
Fail-open: any internal error allows the prompt (a validator must not break your workflow).
"""
import json
import os
import sys

from .i18n import render
from .validator import Validator


def run(payload: dict, mode: str = "enforce", lang=None):
    prompt = payload.get("prompt") or ""
    v = Validator().check(prompt, lang=lang)
    msg = render(v)
    if v.level in ("block", "warn") and mode != "shadow":
        return {"decision": "block", "reason": msg}
    if msg:
        return {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                                       "additionalContext": f"[policy-gate:{v.level}] {msg}"}}
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        out = run(payload, os.environ.get("POLICY_GATE_MODE", "enforce"), os.environ.get("POLICY_GATE_LANG"))
        if out:
            print(json.dumps(out, ensure_ascii=False))
    except Exception as e:  # fail-open
        print(f"policy-gate: internal error, allowing prompt ({type(e).__name__})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
