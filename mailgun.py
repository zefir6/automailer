import os
import requests
import config

def mailgun_message(
    sender,
    subject,
    to,
    contents,
    MAILGUN_API_KEY,
    MAILGUN_DOMAIN,
    cc=None,
    bcc=None,
    MAILGUN_API_BASE = "https://api.mailgun.net/v3"
):
    print("Mailguning email")

    data = {
        "from": sender,
        "to": to,
        "subject": subject,
        "html": contents,
    }

    if cc:
        data["cc"] = cc

    if bcc:
        data["bcc"] = bcc

    response = requests.post(
        f"{MAILGUN_API_BASE}/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data=data,
        timeout=10,
    )

    response.raise_for_status()
    return response.json()