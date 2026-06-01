# Daily Briefing — Setup Guide

Follow these steps once and you're done. Each step says exactly what to type or click.

---

## Step 1 — Create a GitHub Account

GitHub is a free website that stores your code and hosts your public website.

1. Go to **https://github.com** and click **Sign up**.
2. Pick a username (this becomes part of your website URL, e.g. `guillermo` → `guillermo.github.io/daily-briefing`).
3. Verify your email and complete signup.

---

## Step 2 — Create Your Repository (the folder on GitHub)

A repository is just a project folder that GitHub can see.

1. Once logged in, click the **+** button (top right) → **New repository**.
2. Repository name: `daily-briefing`
3. Set it to **Public** (required for free GitHub Pages hosting).
4. Check ✅ **Add a README file**.
5. Click **Create repository**.

---

## Step 3 — Enable GitHub Pages (your website)

1. Inside your new `daily-briefing` repo, click **Settings** (top menu).
2. In the left sidebar click **Pages**.
3. Under "Build and deployment" → Source → select **Deploy from a branch**.
4. Branch: `main` | Folder: `/docs` → click **Save**.
5. Your website URL is now: `https://YOUR-USERNAME.github.io/daily-briefing`
   (It won't show content yet — that comes after your first run.)

---

## Step 4 — Download Your Repository to Your Mac

We need to get the GitHub folder onto your computer so the script can push updates.

1. Open **Terminal** on your Mac.
   - Press `Cmd + Space`, type `Terminal`, press Enter.
2. Type these commands one by one (replace `YOUR-USERNAME` with your GitHub username):

```bash
cd ~/Desktop
git clone https://github.com/YOUR-USERNAME/daily-briefing.git github-repo
```

This creates a folder called `github-repo` on your Desktop.

3. Now copy the project files into it:

```bash
cp -r ~/Desktop/daily-briefing/* ~/Desktop/github-repo/
cp ~/Desktop/daily-briefing/CLAUDE.md ~/Desktop/github-repo/
mkdir -p ~/Desktop/github-repo/docs
```

4. Push everything to GitHub:

```bash
cd ~/Desktop/github-repo
git add .
git commit -m "Initial setup"
git push
```

> **Note:** Git may ask you to log in. Use your GitHub username and a
> Personal Access Token (not your password). To create one:
> GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)
> → Generate new token → check `repo` scope → copy the token and use it as your password.

From now on, **run all commands from `~/Desktop/github-repo`**, not `daily-briefing`.

---

## Step 5 — Install Python

Check if Python is already installed:

```bash
python3 --version
```

If you see `Python 3.x.x` you're good. If not:
1. Go to **https://www.python.org/downloads/**
2. Click the big yellow "Download Python" button and install it.

---

## Step 6 — Install the Required Packages

In Terminal, run:

```bash
cd ~/Desktop/github-repo
pip3 install -r requirements.txt
```

This installs the `anthropic` Python library (the package that talks to Claude).

---

## Step 7 — Get an Anthropic API Key

This key lets the script call Claude to search the web.

1. Go to **https://console.anthropic.com**
2. Sign up for an account (you can use your Google account).
3. Click **API Keys** in the left menu → **Create Key**.
4. Copy the key (it starts with `sk-ant-...`). **Save it — you can only see it once.**
5. Add $5–10 in credits (Settings → Billing). Each daily run costs ~$0.15–0.30.

---

## Step 8 — Set Up Gmail App Password

A Gmail App Password lets the script send email without exposing your real password.

1. Go to **https://myaccount.google.com/security**
2. Make sure **2-Step Verification** is ON (required for App Passwords).
   If it's off, click it and follow the steps to turn it on.
3. Search for "App passwords" in the Google Account search bar → click it.
4. Under "Select app" choose **Mail**, under "Select device" choose **Mac**.
5. Click **Generate**. Google shows a 16-character password like `abcd efgh ijkl mnop`.
6. Copy it (remove the spaces, so: `abcdefghijklmnop`).

---

## Step 9 — Set Your Environment Variables

Environment variables are how you give the script your secret keys without putting
them in the code (where they could accidentally be shared).

In Terminal:

```bash
# Open your shell profile file
open ~/.zshrc
```

A text editor opens. Scroll to the bottom and add these three lines
(replace the values with your actual keys):

```
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
export GMAIL_ADDRESS="gvillalpp@gmail.com"
export GMAIL_APP_PASSWORD="abcdefghijklmnop"
```

Save and close the file. Then run:

```bash
source ~/.zshrc
```

This loads the new settings. You only need to do this once.

---

## Step 10 — Run Your First Briefing!

```bash
cd ~/Desktop/github-repo
python3 update.py
```

You'll see progress messages. It takes about 2–3 minutes (Claude is searching the web).
When done:
- Visit `https://YOUR-USERNAME.github.io/daily-briefing` — your website is live!
- Check `gvillalpp@gmail.com` — the email arrived!

---

## Running It Again Tomorrow

Every day, just open Terminal and run:

```bash
cd ~/Desktop/github-repo
python3 update.py
```

That's it. The website and email both update automatically.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ANTHROPIC_API_KEY not set` | Run `source ~/.zshrc` and try again |
| `Email failed` | Double-check your App Password has no spaces |
| `Git push failed` | Make sure you used a Personal Access Token (not your password) |
| Website not updating | Wait 1–2 min after push; GitHub Pages has a small delay |

---

## What Each File Does

| File | Purpose |
|---|---|
| `update.py` | The main script — runs everything |
| `requirements.txt` | List of Python packages needed |
| `docs/index.html` | The generated website (overwritten each run) |
| `CLAUDE.md` | Instructions for Claude in future sessions |
| `README.md` | This guide |
