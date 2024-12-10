import smtplib
from email.mime.text import MIMEText
import random
import sys
import os
import json
from dotenv import load_dotenv

load_dotenv()

family_members = json.load(open("input.json"))
f = open("log.txt", "w")


def draw_names(names):
    """
        Unit tests:
        >>> import random
        >>> random.seed(0)  # Set seed for deterministic test
        >>> names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
        >>> pairs = draw_names(names)

        # Ensure no one is their own Secret Santa
        >>> all(giver != receiver for giver, receiver in pairs.items())
        True

        # Ensure everyone has exactly one Secret Santa
        >>> len(set(pairs.keys())) == len(names)
        True

        # Ensure each person is a Secret Santa for exactly one person
        >>> len(set(pairs.values())) == len(names)
        True

        # Ensure randomness by checking multiple draws
        >>> random.seed(None)  # Reset seed for randomness
        >>> results = [draw_names(names) for _ in range(10)]
        >>> len(set(frozenset(p.items()) for p in results)) > 1  # At least one unique draw
        True

    """
    givers = names[:]
    receivers = names[:]
    random.shuffle(receivers)
    while any(giver == receiver for giver, receiver in zip(givers, receivers)):
        random.shuffle(receivers)
    return dict(zip(givers, receivers))


# Email configuration for Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(sender_email, sender_password, recipient_email, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        f.write(f"Email sent to {recipient_email}. Subject: {subject}, body: {body}")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "test":
        import doctest
        doctest.testmod(verbose=True)
        sys.exit(1)

    names = list(family_members.keys())
    secret_santa_pairs = draw_names(names)

    for giver, receiver in secret_santa_pairs.items():
        subject = "Amic invisible"
        body = f"Hola {giver},\n\n aquest any, t'ha tocat fer-li el regal de l'amic invisible a: {receiver}!\n\n"
        recipient_email = family_members[giver]

        try:
            send_email(EMAIL_ADDRESS, EMAIL_PASSWORD, recipient_email, subject, body)
        except Exception as e:
            print(f"Failed to send email to {recipient_email}: {e}")
