#!/usr/bin/env python3
"""
Daily Briefing — update.py
Run this script each day to refresh the website and send the email.

Usage:
    python update.py
"""

import os
import smtplib
import subprocess
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import anthropic

# ── Configuration ──────────────────────────────────────────────────────────────
# These values are read from environment variables you set during setup.
ANTHROPIC_API_KEY  = os.environ.get("ANTHROPIC_API_KEY", "")
GMAIL_ADDRESS      = os.environ.get("GMAIL_ADDRESS", "gvillalpp@gmail.com")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
RECIPIENT_EMAIL    = "gvillalpp@gmail.com"

DOCS_DIR = Path(__file__).parent / "docs"
DOCS_DIR.mkdir(exist_ok=True)

# ── Helpers ────────────────────────────────────────────────────────────────────

def check_config():
    """Make sure required environment variables are set before we start."""
    missing = []
    if not ANTHROPIC_API_KEY:
        missing.append("ANTHROPIC_API_KEY")
    if not GMAIL_APP_PASSWORD:
        missing.append("GMAIL_APP_PASSWORD")
    if missing:
        print("\n❌  Missing environment variables:")
        for m in missing:
            print(f"   export {m}=your_value_here")
        print("\nSee README.md for setup instructions.")
        raise SystemExit(1)


def research_topic(client: anthropic.Anthropic, topic: str, instructions: str) -> str:
    """
    Ask Claude to search the web and write one briefing section.
    Returns the section as an HTML string ready to paste into the page.
    """
    today = datetime.now().strftime("%A, %B %d, %Y")
    print(f"   🔍  Researching {topic}…")

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        tools=[{
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 8,
        }],
        messages=[{
            "role": "user",
            "content": f"""Today is {today}.

You are writing the {topic} section of a daily briefing for a beginner investor/learner
based in Mexico. Search the web for the most relevant and trending news from the last
24–48 hours.

{instructions}

IMPORTANT FORMATTING RULES:
- Return ONLY valid HTML — no markdown, no backticks, no code fences.
- Every headline must be a real hyperlink (<a href="..."> pointing to the actual article.
- Include 4–6 news items.
- End with one "Learn the Basics" concept block.
- Use exactly this HTML structure (copy it precisely):

<div class="items">

  <div class="item">
    <h3><a href="ARTICLE_URL" target="_blank" rel="noopener">HEADLINE HERE</a>
        <span class="source">Source Name</span></h3>
    <p class="summary">2–3 sentence plain-English summary of the news.</p>
    <p class="why"><strong>Why it matters:</strong> 1–2 sentences explaining the significance.</p>
  </div>

</div>

<div class="learn">
  <h3>💡 Today's Concept: CONCEPT NAME</h3>
  <p>2–3 sentence beginner-friendly explanation.</p>
</div>
"""
        }],
    )

    # Pull all text blocks out of the response
    html = ""
    for block in response.content:
        if hasattr(block, "text"):
            html += block.text

    return html.strip()


def build_html(finance: str, economics: str, ai: str) -> str:
    """Combine the three sections into a complete HTML page."""
    now = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Daily Briefing — {datetime.now().strftime("%b %d, %Y")}</title>
  <style>
    /* ── Base ── */
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      background: #f5f5f0;
      color: #1a1a1a;
      line-height: 1.65;
      padding: 0 1rem 4rem;
    }}
    a {{ color: inherit; }}
    a:hover {{ text-decoration: underline; }}

    /* ── Header ── */
    header {{
      max-width: 780px; margin: 0 auto;
      padding: 2.5rem 0 1.5rem;
      border-bottom: 2px solid #1a1a1a;
    }}
    header h1 {{ font-size: 1.9rem; font-weight: 700; letter-spacing: -0.5px; }}
    header p  {{ color: #555; font-size: 0.88rem; margin-top: 0.3rem; }}

    /* ── Section wrapper ── */
    .section {{
      max-width: 780px; margin: 2.5rem auto 0;
      background: #fff;
      border-radius: 8px;
      border: 1px solid #e0e0d8;
      overflow: hidden;
    }}
    .section-header {{
      padding: 1rem 1.5rem;
      font-weight: 700;
      font-size: 0.78rem;
      letter-spacing: 1.2px;
      text-transform: uppercase;
    }}
    .finance   .section-header {{ background: #1a3a5c; color: #fff; }}
    .economics .section-header {{ background: #1c5c2e; color: #fff; }}
    .ai        .section-header {{ background: #3d1a5c; color: #fff; }}

    /* ── Items ── */
    .items {{ padding: 0 1.5rem; }}
    .item {{
      padding: 1.2rem 0;
      border-bottom: 1px solid #eee;
    }}
    .item:last-child {{ border-bottom: none; }}
    .item h3 {{
      font-size: 1rem;
      font-weight: 600;
      margin-bottom: 0.45rem;
      line-height: 1.4;
    }}
    .item h3 a {{ text-decoration: none; color: #1a1a1a; }}
    .item h3 a:hover {{ text-decoration: underline; }}
    .source {{
      display: inline-block;
      margin-left: 0.5rem;
      font-size: 0.72rem;
      font-weight: 500;
      color: #888;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .summary {{ font-size: 0.93rem; color: #333; margin-bottom: 0.4rem; }}
    .why {{ font-size: 0.88rem; color: #555; }}
    .why strong {{ color: #1a1a1a; }}

    /* ── Learn block ── */
    .learn {{
      margin: 0 1.5rem;
      padding: 1rem 1.2rem;
      background: #f9f9f6;
      border-radius: 6px;
      border-left: 3px solid #ccc;
      margin-bottom: 1.5rem;
    }}
    .finance   .learn {{ border-color: #1a3a5c; }}
    .economics .learn {{ border-color: #1c5c2e; }}
    .ai        .learn {{ border-color: #3d1a5c; }}
    .learn h3 {{ font-size: 0.9rem; margin-bottom: 0.4rem; }}
    .learn p  {{ font-size: 0.88rem; color: #444; }}

    /* ── Footer ── */
    footer {{
      max-width: 780px; margin: 2.5rem auto 0;
      font-size: 0.8rem; color: #999; text-align: center;
    }}
  </style>
</head>
<body>

<header>
  <h1>Daily Briefing</h1>
  <p>Last updated: {now}</p>
</header>

<!-- FINANCE -->
<div class="section finance">
  <div class="section-header">📈 Finance &amp; Markets</div>
  {finance}
</div>

<!-- ECONOMICS -->
<div class="section economics">
  <div class="section-header">🌎 Economics — World &amp; Mexico</div>
  {economics}
</div>

<!-- AI -->
<div class="section ai">
  <div class="section-header">🤖 AI — Personal Life &amp; GTM</div>
  {ai}
</div>

<footer>
  <p>Generated by Claude · Sources linked above · Not financial advice</p>
</footer>

</body>
</html>
"""


def save_html(html: str):
    """Write the HTML file to the docs/ folder."""
    output = DOCS_DIR / "index.html"
    output.write_text(html, encoding="utf-8")
    print(f"   ✅  Saved website → {output}")


def push_to_github():
    """Commit and push the updated HTML so the website goes live."""
    repo = Path(__file__).parent
    try:
        subprocess.run(["git", "add", "docs/index.html"], cwd=repo, check=True)
        msg = f"Daily briefing {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(["git", "commit", "-m", msg], cwd=repo, check=True)
        subprocess.run(["git", "push"], cwd=repo, check=True)
        print("   ✅  Website pushed to GitHub Pages")
    except subprocess.CalledProcessError as e:
        print(f"   ⚠️   Git push failed (website not updated online): {e}")
        print("       Check README.md for GitHub setup instructions.")


def send_email(html: str):
    """Send the briefing as an HTML email via Gmail."""
    subject = f"Daily Briefing — {datetime.now().strftime('%A, %B %d')}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = GMAIL_ADDRESS
    msg["To"]      = RECIPIENT_EMAIL

    # Plain-text fallback (for email clients that don't render HTML)
    plain = "Your daily briefing is ready. Open the HTML version to read it."
    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html,  "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
        print(f"   ✅  Email sent to {RECIPIENT_EMAIL}")
    except Exception as e:
        print(f"   ⚠️   Email failed: {e}")
        print("       Check README.md for Gmail App Password instructions.")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("\n🗞️  Daily Briefing — starting update…\n")
    check_config()

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # ── Finance section ──
    finance_html = research_topic(
        client,
        topic="Finance & Markets",
        instructions="""
Cover:
- What the major US indices (S&P 500, Nasdaq, Dow) did today and WHY (specific drivers).
- Notable sector moves and why they moved.
- Macro data that matters: interest rates, Fed commentary, inflation figures.
- USD/MXN exchange rate and any Banxico (Mexico's central bank) news.
- 1–2 notable company or earnings stories.
- Always include real numbers (%, index levels, rate figures) from reputable sources
  (WSJ, Bloomberg, Reuters, Financial Times, CNBC, Banxico.org.mx).
- Frame everything as context and education. No buy/sell recommendations.
"""
    )

    # ── Economics section ──
    economics_html = research_topic(
        client,
        topic="Economics — World & Mexico",
        instructions="""
Cover global macro + strong Mexico focus:
- Key global economic events: GDP data, employment, trade, central bank decisions.
- Mexico-specific: peso (MXN), INEGI data, Banxico policy, inflation, remittances,
  nearshoring trends, government fiscal news (SHCP), US-Mexico trade.
- Sources: Reuters, Bloomberg, El Financiero, El Economista, INEGI, Banxico, IMF, World Bank.
- Explain economic terms simply (e.g., "GDP is the total value of everything a country produces").
"""
    )

    # ── AI section ──
    ai_html = research_topic(
        client,
        topic="AI — Personal Life & Go-to-Market",
        instructions="""
Cover two angles:
1. Personal productivity: new AI tools, tips, or features that help individuals work
   smarter, save time, or learn faster. (Apps, prompting tricks, new model releases.)
2. Go-to-market (GTM): how companies are using AI to grow — marketing, sales, customer
   success, product launches. Real examples preferred.
- Sources: TechCrunch, The Verge, Wired, VentureBeat, a16z blog, X/Twitter threads
  from AI researchers, official announcements from OpenAI/Anthropic/Google.
- Keep it practical: "here's how this helps you today."
"""
    )

    print("\n   📝  Building HTML page…")
    html = build_html(finance_html, economics_html, ai_html)
    save_html(html)

    print("   📤  Pushing to GitHub…")
    push_to_github()

    print("   📧  Sending email…")
    send_email(html)

    print("\n✅  Done! Briefing is live.\n")


if __name__ == "__main__":
    main()
