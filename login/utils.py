import base64
import hashlib
import hmac

class Utils:
    def get_secret_hash(username, client_id, client_secret):
        msg = str(username) + client_id
        dig = hmac.new(str(client_secret).encode('utf-8'),
                    msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
        d2 = base64.b64encode(dig).decode()
        return d2
