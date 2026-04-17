# House Maintenance Tracker — Deployment Guide

## What Needs to Happen

| Step | Who Does It | Time |
|---|---|---|
| 1. Fix the code for cloud | Claude | ~5 min |
| 2. Create a free Supabase database | You | ~5 min |
| 3. Generate your password hash | You (one command) | 2 min |
| 4. Deploy on Streamlit Community Cloud | You | ~5 min |
| 5. Paste secrets into Streamlit | You | 2 min |

Total: ~20 minutes.

---

## Step 1 — Fix the Code (ask Claude)

Tell Claude:

> "Fix the code for Streamlit Cloud deployment: add missing packages to requirements.txt and switch the database from SQLite to Supabase Postgres."

Claude will update `requirements.txt` and `src/db.py`. Once done, it will commit and push. You do nothing in this step — just confirm you want it done.

---

## Step 2 — Create a Free Supabase Database

Supabase is a free hosted Postgres database. Your data lives there permanently, survives restarts.

1. Go to **[supabase.com](https://supabase.com)** → click **Start your project** → sign in with GitHub.
2. Click **New project**.
3. Fill in:
   - **Name:** `house-maintenance-tracker` (or anything you like)
   - **Database Password:** choose a strong password — **write it down**, you'll need it in Step 5
   - **Region:** `US East (N. Virginia)` — closest free option for Canada
4. Click **Create new project** — wait ~2 minutes for it to spin up.
5. In the left sidebar, go to **Settings → Database**.
6. Scroll to **Connection string** → select the **URI** tab.
7. Copy the string — it looks like:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxxxxxx.supabase.co:5432/postgres
   ```
   Replace `[YOUR-PASSWORD]` with the password you set in step 3.
8. **Save this string** — you'll paste it into Streamlit secrets in Step 5.

---

## Step 3 — Generate Your Password Hash

You need a bcrypt hash of your chosen app password. Do this on any computer with Python installed.

Open Terminal and run:

```bash
python3 -c "import bcrypt; print(bcrypt.hashpw(b'YOUR_PASSWORD_HERE', bcrypt.gensalt(12)).decode())"
```

Replace `YOUR_PASSWORD_HERE` with whatever password you want to use to log in to the app.

The output will look like:
```
$2b$12$AbCdEfGhIjKlMnOpQrStUvWxYz1234567890abcdefghijklmnop
```

**Copy and save this hash** — you'll need it in Step 5.

> If you don't have Python locally, you can also run this in a Streamlit app locally or ask Claude to generate a test hash for a specific password.

---

## Step 4 — Deploy on Streamlit Community Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub.
2. Click **Create app** (top right).
3. Select **Deploy a public app from GitHub** (or private — your repo is private, that's fine).
4. Fill in:
   - **Repository:** `Segey-P/house-maintenance-tracker`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** choose something like `house-maintenance-sp` (this becomes the subdomain)
5. **Do not click Deploy yet** — go to Step 5 first.

---

## Step 5 — Configure Secrets

Still on the deploy screen, click **Advanced settings** → **Secrets**.

Paste this block, replacing both placeholder values with your real ones from Steps 2 and 3:

```toml
password_hash = "$2b$12$PASTE_YOUR_HASH_HERE"

[database]
url = "postgresql://postgres:YOUR_PASSWORD@db.xxxxxxxxxxxx.supabase.co:5432/postgres"
```

Click **Save** → then click **Deploy**.

Streamlit will install packages and start the app. First deploy takes ~3 minutes.

---

## Step 6 — Verify It Works

1. Open your app URL (e.g. `https://house-maintenance-sp.streamlit.app`).
2. Enter your password — you should see the dashboard.
3. Go to **Inventory** → add a test device.
4. Go to **Schedules** → add a schedule for that device.
5. Go back to **Dashboard** — confirm the device and schedule appear.
6. Refresh the page — data should still be there (confirms database persistence works).

If anything shows an error, copy the error message and share it with Claude.

---

## Step 7 — Bookmark and Share

The app is password-protected, so you can access it from any browser or phone.

- Bookmark: `https://[your-app-name].streamlit.app`
- Mobile: open in Safari/Chrome, tap Share → Add to Home Screen for an app-like experience.

---

## Google Calendar & Email Alerts (Optional — Phase 2)

The Notifications tab is built but requires a one-time Google OAuth setup that doesn't work automatically on Streamlit Cloud. It will show an error if you click the buttons — that's expected for now.

To enable it later:
1. Run `python3 setup_auth.py` locally (follows browser OAuth flow).
2. This creates `config/credentials/token.json`.
3. Ask Claude to "add Google credentials to secrets so the Notifications tab works on Streamlit Cloud."

Claude will encode the token file into the secrets block. This is a 10-minute task for a future session.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| White screen / module not found | Missing package in requirements.txt | Tell Claude which package is missing |
| "No password hash configured" | Secrets not saved correctly | Check Streamlit → App settings → Secrets |
| "could not connect to server" | Wrong database URL in secrets | Re-copy the URI from Supabase Settings → Database |
| Data disappears on refresh | Database not connected — using SQLite fallback | Confirm Step 1 (code fix) was committed and pushed |
| Notifications tab error | Expected — Google auth not set up on cloud | See Phase 2 above |
