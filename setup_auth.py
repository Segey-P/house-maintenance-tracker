"""Run once to authorize Google Calendar + Gmail access for this project."""
from pathlib import Path

CLIENT_SECRET = Path("config/credentials/client_secret.json")
TOKEN_PATH = Path("config/credentials/token.json")

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.send",
]


def main():
    if not CLIENT_SECRET.exists():
        print(f"\nERROR: {CLIENT_SECRET} not found.\n")
        print("Steps:")
        print("  1. Go to console.cloud.google.com → APIs & Services → Credentials")
        print("  2. Enable: Google Calendar API + Gmail API in the same project")
        print("  3. Download your OAuth 2.0 client secret JSON")
        print(f"  4. Save it as: {CLIENT_SECRET.resolve()}\n")
        return

    from google_auth_oauthlib.flow import InstalledAppFlow

    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
    creds = flow.run_local_server(port=0)
    TOKEN_PATH.write_text(creds.to_json())
    print(f"\nDone. Token saved to {TOKEN_PATH}")


if __name__ == "__main__":
    main()
