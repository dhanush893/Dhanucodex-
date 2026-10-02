# DHANU-CODEX AI v1.0

A lightweight AI chatbot for Termux using the OpenAI API.

## Termux

```bash
git clone https://github.com/dhanush893/Dhanucodex-.git
cd Dhanucodex-/ai
pkg install python git -y
chmod +x run.sh
export OPENAI_API_KEY='YOUR_API_KEY'
./run.sh
```

Optional model override:

```bash
export DHANU_CODEX_MODEL='gpt-5-mini'
```

Never commit an API key to GitHub. Store it in an environment variable instead.

## Commands

- `/help` - show commands
- `/clear` - clear conversation
- `/exit` - quit
