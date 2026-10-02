#!/usr/bin/env python3
"""DHANU-CODEX AI - Termux CLI assistant.

Uses the OpenAI Responses REST API directly so Termux does not need the
OpenAI Python SDK or its native Rust-based jiter dependency.
"""

import json
import os
import sys
from pathlib import Path

import requests

API_URL = "https://api.openai.com/v1/responses"
CONFIG_FILE = Path.home() / ".config" / "dhanu-codex" / "api_key"

SYSTEM_PROMPT = """You are DHANU-CODEX AI, a practical personal AI assistant.

Motto: Think. Create. Code. Evolve.

You help with programming, Python, web development, Termux/Linux,
cybersecurity education, study help, writing, debugging, and general questions.
Be accurate and concise. Do not pretend to know unknown or current facts.
For cybersecurity, support authorized, defensive, and educational use only.
"""


def get_api_key() -> str | None:
    key = os.getenv("OPENAI_API_KEY")
    if key:
        return key.strip()
    if CONFIG_FILE.is_file():
        return CONFIG_FILE.read_text(encoding="utf-8").strip()
    return None


def extract_text(data: dict) -> str:
    """Extract text from a Responses API JSON response."""
    chunks: list[str] = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") == "output_text" and content.get("text"):
                chunks.append(content["text"])
    return "\n".join(chunks).strip()


def ask(api_key: str, history: list[dict]) -> str:
    payload = {
        "model": os.getenv("DHANU_CODEX_MODEL", "gpt-5-mini"),
        "input": history,
    }
    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=120,
    )

    if not response.ok:
        try:
            detail = response.json().get("error", {}).get("message", response.text)
        except ValueError:
            detail = response.text
        raise RuntimeError(f"API {response.status_code}: {detail}")

    text = extract_text(response.json())
    if not text:
        raise RuntimeError("The API returned no text output.")
    return text


def main() -> None:
    api_key = get_api_key()
    if not api_key:
        print("\n[!] OPENAI_API_KEY is not set.")
        print("Run: export OPENAI_API_KEY='your-key'\n")
        print(f"Or save it to: {CONFIG_FILE}\n")
        sys.exit(1)

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
            answer = ask(api_key, history)
            print(f"\nDHANU-CODEX ❯ {answer}\n")
            history.append({"role": "assistant", "content": answer})
        except Exception as exc:
            history.pop()
            print(f"\n[ERROR] {exc}\n")


if __name__ == "__main__":
    main()
