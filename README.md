# AI/ML News Digest

A Claude Managed Agent that scrapes the web daily for AI/ML research papers and news, then posts a formatted digest to Slack across three topic-specific channels.

## Channels

| Channel | ID | Content |
|---|---|---|
| `#ai-news` | `C0AUU0QD8S3` | Model releases, product announcements, AI policy |
| `#ml-news` | `C0AV62C9G2H` | Research papers, arXiv, benchmarks, architectures |
| `#misc` | `C0AV62BDE77` | Hardware, tooling, CS conference news |

## How it works

1. Agent searches the web sequentially (max 4 searches) for fresh AI/ML content
2. Curates 5–10 items with verified, non-fabricated URLs from search results
3. Writes 2-sentence summaries in its own words
4. Posts one Slack message per channel via the Slack MCP

## Setup

### Prerequisites

- Anthropic API key with Managed Agents access
- A Claude Managed Agent deployed (see `agent_config.json`)
- A vault with a Slack credential for `https://mcp.slack.com/mcp`
- Slack bot invited to `#ai-news`, `#ml-news`, and `#misc`

### Environment variables

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `AGENT_ID` | The deployed agent ID |
| `ENVIRONMENT_ID` | The `aiml-news-digest-env` environment ID |
| `VAULT_ID` | The vault containing the Slack credential |

### Run manually

```bash
pip install anthropic
export ANTHROPIC_API_KEY=...
export ENVIRONMENT_ID=...
python run_digest.py
```

### Run on a schedule (GitHub Actions)

1. Fork this repo
2. Add the four environment variables as **repository secrets** under Settings → Secrets → Actions
3. The workflow in `.github/workflows/daily_digest.yml` runs at 9am UTC Monday–Friday automatically
4. Trigger it manually any time from the Actions tab → **Daily AI/ML Digest** → **Run workflow**

## Slack delivery troubleshooting

If `slack_send_message` returns "permission denied":

1. **Check OAuth scopes** — the Slack credential in your vault must have `chat:write` scope
2. **Check bot membership** — run `/invite @your-bot-name` in each channel
3. **Re-authorize** — delete and re-add the Slack credential in the vault, watching the OAuth consent screen for write scopes
4. **Fallback** — the agent will print the formatted digest to the session transcript for manual copy-paste if posting fails

## Agent design notes

- **Model**: `claude-haiku-4-5` (higher rate limits than Sonnet; sufficient for summarization)
- **One tool call per turn**: enforced by prompt to prevent parallel search fan-out that causes rate limit errors
- **No fabrication rule**: agent must have a verbatim URL from search results for every item; generic landing pages are rejected
- **Sequential delivery**: one Slack post per turn, one channel at a time
