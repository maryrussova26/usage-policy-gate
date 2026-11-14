"""Plugin entrypoint: runs the UserPromptSubmit hook from the bundled library (no install needed)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
from policy_gate.claude_code_hook import main  # noqa: E402

raise SystemExit(main())
