import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.exceptions import InvalidSignature

class DSACore:
    @staticmethod
    def generate_keys(key_size=2048):
        private_key = dsa.generate_private_key(key_size=key_size)
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def save_private_key(private_key, filename):
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(filename, 'wb') as f:
            f.write(pem)

    @staticmethod
    def save_public_key(public_key, filename):
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open(filename, 'wb') as f:
            f.write(pem)

    @staticmethod
    def load_private_key(filename):
        with open(filename, "rb") as key_file:
            return serialization.load_pem_private_key(key_file.read(), password=None)

    @staticmethod
    def load_public_key(filename):
        with open(filename, "rb") as key_file:
            return serialization.load_pem_public_key(key_file.read())

    @staticmethod
    def sign_data(private_key, data: bytes):
        return private_key.sign(data, hashes.SHA256())

    @staticmethod
    def verify_signature(public_key, signature: bytes, data: bytes):
        try:
            public_key.verify(signature, data, hashes.SHA256())
            return True
        except InvalidSignature:
            return False