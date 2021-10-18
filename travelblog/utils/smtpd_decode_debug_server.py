import asyncore
import email
from smtpd import DebuggingServer


class ActualDebuggingServer(DebuggingServer):
    def _print_message_content(self, peer, data):
        msg = email.message_from_bytes(data)
        for (header, value) in msg.items():
            print(header, ': ', value)
        for part in msg.walk():
            print('---------- a part: ----------')
            maybe_decoded_payload = part.get_payload(decode=True)
            if maybe_decoded_payload is not None:
                print(bytes.decode(maybe_decoded_payload, encoding="utf-8"))


if __name__ == '__main__':
    ActualDebuggingServer(('0.0.0.0', 1025), ('0.0.0.0', 1025))
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass
