"""
Translate uploaded text files to Hindi and email the translated file
to the PR author.
"""

import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

from googletrans import Translator


def translate_file_to_hindi(file_path: str) -> str:
    """Read a text file and return its Hindi translation."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        print(f"Skipping empty file: {file_path}")
        return ""

    translator = Translator()
    # Split into chunks of ~4000 chars to avoid API limits
    chunk_size = 4000
    chunks = [content[i : i + chunk_size] for i in range(0, len(content), chunk_size)]

    translated_chunks = []
    for chunk in chunks:
        result = translator.translate(chunk, dest="hi")
        translated_chunks.append(result.text)

    return "".join(translated_chunks)


def send_email(
    recipient_email: str,
    pr_author: str,
    original_filename: str,
    translated_content: str,
):
    """Send the translated file as an attachment via SMTP."""
    smtp_host = os.environ["SMTP_HOST"]
    smtp_port = int(os.environ["SMTP_PORT"])
    smtp_user = os.environ["SMTP_USER"]
    smtp_password = os.environ["SMTP_PASSWORD"]
    sender_email = os.environ["SENDER_EMAIL"]

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = f"Hindi Translation: {original_filename}"

    body = (
        f"Hi @{pr_author},\n\n"
        f'Your file "{original_filename}" has been translated to Hindi.\n'
        f"Please find the translated file attached.\n\n"
        f"— Automated Translation Bot"
    )
    msg.attach(MIMEText(body, "plain", "utf-8"))

    # Attach translated file
    translated_filename = Path(original_filename).stem + "_hindi.txt"
    attachment = MIMEBase("application", "octet-stream")
    attachment.set_payload(translated_content.encode("utf-8"))
    encoders.encode_base64(attachment)
    attachment.add_header(
        "Content-Disposition", f"attachment; filename={translated_filename}"
    )
    msg.attach(attachment)

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

    print(f"Email sent to {recipient_email} with translated file: {translated_filename}")


def main():
    changed_files = os.environ.get("CHANGED_FILES", "").strip()
    recipient_email = os.environ.get("RECIPIENT_EMAIL", "").strip()
    pr_author = os.environ.get("PR_AUTHOR", "unknown")

    if not changed_files:
        print("No new .txt files found in uploads/. Nothing to do.")
        sys.exit(0)

    if not recipient_email:
        print(
            f"WARNING: Could not determine email for @{pr_author}. "
            "Make sure the GitHub profile has a public email."
        )
        sys.exit(1)

    for file_path in changed_files.splitlines():
        file_path = file_path.strip()
        if not file_path or not file_path.endswith(".txt"):
            continue

        print(f"Translating: {file_path}")
        translated = translate_file_to_hindi(file_path)
        if not translated:
            continue

        original_name = Path(file_path).name
        send_email(recipient_email, pr_author, original_name, translated)

    print("All files processed.")


if __name__ == "__main__":
    main()
