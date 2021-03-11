import email
import imaplib
from email.header import decode_header
from pathlib import Path
from time import sleep
import Encryption


BLACKLIST_FILE = Path("blacklist.txt")


def get_blacklisting(blacklist_file=BLACKLIST_FILE):
    with open(blacklist_file) as blacklist:
        return blacklist.read().splitlines()


def connect_imap(email_address, password, imap_address):
    imap = imaplib.IMAP4_SSL(imap_address)
    imap.login(email_address, password)
    return imap


def delete(imap, sender_list=[], subject_list=[]):
    imap.noop()
    status, messages = imap.select("INBOX")
    latest_message = int(messages[0])
    res, msg = imap.fetch(str(latest_message), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding)
            sender, encoding = decode_header(msg.get("From"))[0]
            if isinstance(sender, bytes):
                sender = sender.decode(encoding)
            sender_address = (sender.split('<'))[1].split('>')[0]
            print("Subject:", subject, "--- from:", sender, end='')
            if sender_address in sender_list or subject in subject_list:
                #body = msg.get_payload(decode=True).decode()
                imap.store(str(latest_message), "+FLAGS", "\\Deleted")
                imap.expunge()
                imap.close()
                imap.logout()
                print(" --- deleted")
            else:
                print(" --- NOT deleted")


def xxx(attr=[]):
    pass


if __name__ == '__main__':
    email_list = Encryption.get_emails()
    print(email_list)
    for login in email_list:
        print(login[0])
        imap = connect_imap(*login)
        delete(imap, sender_list=get_blacklisting())
    print(get_blacklisting())
