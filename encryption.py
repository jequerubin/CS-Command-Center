import os
from cryptography.fernet import Fernet

_fernet = None


def _get_fernet():
    global _fernet
    if _fernet is not None:
        return _fernet

    key = os.environ.get("FERNET_KEY")
    if not key:
        generated = Fernet.generate_key().decode()
        print(
            f"\nWARNING: FERNET_KEY is not set in your environment.\n"
            f"A temporary key has been generated for this session,\n"
            f"encrypted data will now be UNREADABLE after restart.\n"
            f"Add the following line to your .env file:\n\n"
            f"    FERNET_KEY={generated}\n"
        )
        key = generated

    _fernet = Fernet(key.encode() if isinstance(key, str) else key)
    return _fernet


def encrypt_token(token: str) -> str:
    return _get_fernet().encrypt(token.encode()).decode()


def decrypt_token(encrypted_token: str) -> str:
    return _get_fernet().decrypt(encrypted_token.encode()).decode()
