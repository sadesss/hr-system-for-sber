import base64
import yaml
from pathlib import Path

class GigaCredentials:
    client_id: str
    client_secret: str

    def __init__(self):
        creds_path: Path = Path("./creds.yaml")
        file_str: str = Path.read_text(creds_path)
        data = yaml.safe_load(file_str)
        self.client_id = data['client_id']
        self.client_secret = data['client_secret']

    def get_base_encoded(self) -> bytes:
        cred_string: str = self.client_id + ":" + self.client_secret
        encoded_string: bytes = base64.b64encode(cred_string.encode("utf-8"))
        return encoded_string