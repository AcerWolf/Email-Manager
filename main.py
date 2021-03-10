import email
import imaplib
from email.header import decode_header
from time import sleep


def get_code():
    email_address = "simonXXX.de"
    password = "XXX"
    imap = imaplib.IMAP4_SSL("imap.gmx.de")
    imap.login(email_address, password)
    count = 0
    while True:
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
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                print("Subject:", subject)
                print("From:", From)
                if subject == "Dein Anmeldungsbestätigungscode für Twitch":
                    body = msg.get_payload(decode=True).decode()
                    soup = BeautifulSoup(body, 'html.parser')
                    div = soup.findAll("div", {"class": "text-center mb-0"})
                    p_children = div[0].findChildren("p", recursive=False)
                    code = p_children[0].text.strip()
                    imap.store(str(latest_message), "+FLAGS", "\\Deleted")
                    imap.expunge()
                    imap.close()
                    imap.logout()
                    return code
                print(count, "sec waiting...")
                count += 1
                if count > 20:
                    return None
                sleep(1)


if __name__ == '__main__':
    pass

