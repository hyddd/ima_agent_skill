# Ima Agent Skill

Control the **ima.copilot** desktop application (AI search client) via Chrome DevTools Protocol (CDP).
Can automatically launch the app if it's not running, and open new tabs for search queries.

## Tools

### ima_search
Open a new tab in ima.copilot and search for the specified query.

- **query** (required): The text to search for.

```bash
python /opt/homebrew/lib/node_modules/clawdbot/skills/ima_agent_skill/scripts/launcher.py "{query}"
```

## Setup & Requirements

- **Python Environment**: Requires a python environment with `websocket-client` installed.
- **Application**: Expects `ima.copilot.app` in `/Applications` or `~/Applications`.
- **Port**: Uses localhost port **8315** for CDP.

## Notes

- The script automatically handles the `--remote-allow-origins=*` flag required by modern Electron apps.
- If the app is closed, it will attempt to launch it.
