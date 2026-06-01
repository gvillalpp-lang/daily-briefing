# Daily Briefing — Project Context

## What This Is
A Python script (`update.py`) that searches the web for daily news, builds a static
HTML page hosted on GitHub Pages, and emails the briefing to gvillalpp@gmail.com.

## Owner
Guillermo — beginner (uses Claude/ChatGPT but has not built software before).
Explain things in plain language. Avoid jargon. Keep code simple over clever.

## Topics Covered
1. **Finance** — major indices, sectors, macro data (rates, inflation, USD/MXN, Banxico),
   earnings. Goal: help Guillermo understand markets and form his own views. Never give
   buy/sell recommendations. Always include real figures + source links.
2. **Economics** — global macro with a strong Mexico focus. Banxico, INEGI, SHCP,
   peso, remittances, trade, GDP.
3. **AI** — personal productivity use cases + go-to-market / GTM strategy angle.

## Architecture
```
update.py  →  Claude API (web_search tool)  →  docs/index.html  →  git push  →  GitHub Pages
                                            →  Gmail SMTP  →  gvillalpp@gmail.com
```

## Key Files
- `update.py`       — main script, run this each day
- `requirements.txt` — Python dependencies (just `anthropic`)
- `docs/index.html`  — generated website (overwritten each run)
- `README.md`        — step-by-step human setup guide

## Environment Variables Required
```
ANTHROPIC_API_KEY   — from console.anthropic.com
GMAIL_ADDRESS       — gvillalpp@gmail.com
GMAIL_APP_PASSWORD  — 16-char App Password from Google Account settings
```

## Website URL
`https://<github-username>.github.io/daily-briefing`
GitHub Pages serves from the `docs/` folder on the `main` branch.

## Email
Sent via Gmail SMTP (port 587, STARTTLS). HTML email, same content as website.
Recipient: gvillalpp@gmail.com

## How to Run
```bash
cd ~/Desktop/daily-briefing
python update.py
```

## Future Ideas (not built yet)
- Cron job / GitHub Actions to run automatically each morning
- Persistent archive of past briefings
- User-configurable topic weights
