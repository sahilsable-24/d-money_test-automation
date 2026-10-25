import re
import time 
from config.settings import INBOX_APP_PASSWORD, INBOX_EMAIL
from imap_tools import AND, MailBox, MailMessageFlags


def mark_old_otps_as_read(recipient:str) -> None:
    """Clear stale OTP emails so a test never picks up an old code."""
    address = INBOX_EMAIL
    password= INBOX_APP_PASSWORD

    with MailBox("imap.gmail.com").login(address,password) as mailbox:
        stale_ids = list(mailbox.uids(AND(to=recipient, subject="OTP", seen=False)))
        if stale_ids:
            mailbox.flag(stale_ids, MailMessageFlags.SEEN, True)


def get_latest_otp(recipient: str, timeout: int = 30) -> str:
    """Keep checking the inbox until an otp arrives, or gives up"""
    give_up_at = time.time() + timeout

    while time.time() < give_up_at:
        otp = _check_inbox_for_otp(recipient)
        if otp:
            return otp
        time.sleep(2)
    raise TimeoutError(f"No OTP Email for {recipient} after {timeout} seconds")

def _check_inbox_for_otp(recipient:str) -> str | None:
    """Look once at the inbox. Return the otp if found, otherwise None."""
    address = INBOX_EMAIL
    password= INBOX_APP_PASSWORD

    with MailBox("imap.gmail.com").login(address,password) as mailbox:
        unread_emails = mailbox.fetch(AND(to=recipient,subject="OTP", seen=False), reverse=True, limit=1)

        for message in unread_emails:
            match = re.search(r"login is:\s*(\d{4})", message.text or message.html)
            if match:
                return match.group(1)
    return None
