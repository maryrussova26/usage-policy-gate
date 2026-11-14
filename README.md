# usage-policy-gate (unofficial)

A pre-submit request checker that maps prompts to the **public** Anthropic Usage Policy, tells users plainly
*what* looks problematic and *why*, offers a compliant alternative, and lets them knowingly accept risk in gray areas.

> **Not affiliated with or endorsed by Anthropic. Not legal advice.** It is a heuristic first line of defense.
> It does **not** guarantee that Anthropic will not warn, limit or suspend an account, and it never helps hide
> activity from Anthropic's systems. Always read the current policy: https://www.anthropic.com/legal/aup

## Install (Claude Code, one minute)
```
/plugin marketplace add maryrussova26/usage-policy-gate
/plugin install usage-policy-gate@usage-policy-gate-marketplace
```
Then every prompt you submit is checked locally before it reaches Claude. No data leaves your machine, nothing is logged.
Requires `python3` on PATH. Skill-only use (claude.ai): upload `plugins/usage-policy-gate/skills/usage-policy-gate/`.
Pip alternative: `pip install git+https://github.com/maryrussova26/usage-policy-gate`.

## Verdicts
| Level | Meaning | Proceeds? |
|---|---|---|
| `pass` | nothing found | yes |
| `note` | allowed, with a high-risk note, a crisis-support message, or an acknowledged/softened gray area | yes |
| `warn` | gray area; add `[accept-risk]` / `[принимаю риск]` to proceed (only for categories where that is meaningful) | with ack |
| `block` | clear violation; acknowledgement does **not** change it | no |

Hard categories (child safety, mass-casualty weapons, malware creation, violent extremism) are never softened.
Crisis messages (self-harm) are **never blocked**: the user gets a supportive message instead.

## Three ways to use it
1. **CLI** — `policy-gate "text"` (`--json`, `--lang ru|en`). Exit 0 allowed / 1 warn / 2 block.
2. **Claude Code hook** — `UserPromptSubmit`; bundled in the plugin; manual setup in `examples/claude-code-settings.json`. Blocking stops the prompt before it reaches Claude.
   `POLICY_GATE_MODE=shadow` only adds hints. Fail-open on internal errors.
3. **Claude Enterprise inference hooks** (chat, Cowork, Claude Code, ...; Owner configures) — `policy-gate-server`.
   Verifies Standard Webhooks signatures (`webhook-id.timestamp.body`, HMAC-SHA256, 5-min tolerance, rotation-aware),
   evaluates only the **latest user message** (a denied message stays in the transcript, so scanning history would
   deny every later turn), returns `{"action":"allow"|"deny","deny_reason","reference_id"}`. Run behind TLS; start in shadow mode.
4. **Skill** — `plugins/usage-policy-gate/skills/` for claude.ai / Claude Code: model-side judgment with the same tiers.

## Design principles
- Judge the **request**, never the person: nationality, origin or language are not signals.
- Warn once, clearly, with a lawful alternative; no threats, no "you are flagged".
- Obfuscation (homoglyphs, spaced letters, leetspeak) is detected only to assess the request.
- Privacy: no logging of prompt text, no network calls, zero dependencies.
- Transparent rules (`validator.py`): auditable, easy to extend or localize.

## Known limits
Regex rules miss paraphrases and can over-flag; context-dependent cases need a human or model judge.
The inference-hook API is beta and Enterprise-only (not on API/Bedrock/Vertex); images are not inspected.
Rules reflect the AUP as read on 2026-11-14 and need review when it changes.

## Develop
`python3 -m unittest discover -s tests` — add cases to `tests/test_validator.py` (both blocks **and** false-positive passes).
MIT license.
