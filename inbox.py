import requests

# ===== CONFIG =====
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REFRESH_TOKEN = "YOUR_REFRESH_TOKEN"
ACCOUNT_ID = "YOUR_ACCOUNT_ID"  # Zoho Mail account ID
DATA_CENTER = "com"  # e.g., com, in, eu

def get_access_token():
    url = f"https://accounts.zoho.{DATA_CENTER}/oauth/v2/token"
    params = {
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token"
    }
    r = requests.post(url, params=params)
    r.raise_for_status()
    return r.json()["access_token"]

def read_inbox(limit=10):
    token = get_access_token()
    url = f"https://mail.zoho.{DATA_CENTER}/api/accounts/{ACCOUNT_ID}/messages/view"
    headers = {"Authorization": f"Zoho-oauthtoken {token}"}
    params = {"folderId": "Inbox", "limit": limit}

    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()
    return r.json().get("data", [])

if __name__ == "__main__":
    mails = read_inbox(5)
    for mail in mails:
        print("From:", mail["fromAddress"])
        print("Subject:", mail["subject"])
        print("-" * 40)
