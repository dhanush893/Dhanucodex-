#!/usr/bin/env python3
"""DHANU-CODEX AI - lightweight Termux CLI assistant."""

import os
import sys
from openai import OpenAI

SYSTEM_PROMPT = """You are DHANU-CODEX AI, a practical personal AI assistant.

Motto: Think. Create. Code. Evolve.

You help with programming, Python, web development, Termux/Linux,
cybersecurity education, study help, writing, debugging, and general questions.
Be accurate and concise. Do not pretend to know unknown or current facts.
For cybersecurity, support authorized, defensive, and educational use only.
"""


def main() -> None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\n[!] OPENAI_API_KEY is not set.")
        print("Set it with: export OPENAI_API_KEY='your-key'\n")
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    history = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("""
╭──────────────────────────────────────────────╮
│                                              │
│             D H A N U - C O D E X           │
│                  A I  v1.0                   │
│                                              │
│       THINK · CREATE · CODE · EVOLVE        │
│                                              │
╰──────────────────────────────────────────────╯

Commands: /help  /clear  /exit
""")

    while True:
        try:
            prompt = input("dhanu@ai ❯ ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break

        if not prompt:
            continue
        if prompt.lower() in {"/exit", "/quit"}:
            print("Goodbye.")
            break
        if prompt.lower() == "/clear":
            history = [{"role": "system", "content": SYSTEM_PROMPT}]
            print("Conversation cleared.\n")
            continue
        if prompt.lower() == "/help":
            print("\n/help  Show commands\n/clear Clear conversation\n/exit  Quit\n")
            continue

        history.append({"role": "user", "content": prompt})
        try:
            response = client.responses.create(
                model=os.getenv("DHANU_CODEX_MODEL", "gpt-5-mini"),
                input=history,
            )
            answer = response.output_text.strip()
            print(f"\nDHANU-CODEX ❯ {answer}\n")
            history.append({"role": "assistant", "content": answer})
        except Exception as exc:
            history.pop()
            print(f"\n[ERROR] {exc}\n")


if __name__ == "__main__":
    main()
