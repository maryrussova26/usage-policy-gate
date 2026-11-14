"""policy-gate CLI.  Exit codes: 0 allowed (pass/note), 1 warn (needs ack), 2 block."""
import argparse
import json
import sys

from .i18n import render
from .validator import Validator


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="policy-gate",
                                 description="Unofficial pre-submit check against the public Anthropic Usage Policy.")
    ap.add_argument("text", nargs="?", help="Request text (reads stdin if omitted)")
    ap.add_argument("--lang", choices=["ru", "en"])
    ap.add_argument("--json", action="store_true", help="Machine-readable output")
    ap.add_argument("--ack", action="store_true", help="Treat as risk-acknowledged (gray areas only)")
    a = ap.parse_args(argv)
    text = a.text if a.text is not None else sys.stdin.read()
    v = Validator().check(text, lang=a.lang, ack=a.ack or None)
    msg = render(v)
    if a.json:
        d = v.to_dict(); d["message"] = msg
        print(json.dumps(d, ensure_ascii=False, indent=2))
    else:
        print(f"[{v.level.upper()}] {msg}".rstrip())
    return {"pass": 0, "note": 0, "warn": 1, "block": 2}[v.level]


if __name__ == "__main__":
    raise SystemExit(main())
