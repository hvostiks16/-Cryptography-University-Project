from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

class RSACore:
    @staticmethod
    def generate_keys(key_size=2048):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
        )
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def save_private_key(private_key, filename, password=None):
        enc_algo = serialization.BestAvailableEncryption(password) if password else serialization.NoEncryption()
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=enc_algo
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
    def load_private_key(filename, password=None):
        with open(filename, "rb") as key_file:
            return serialization.load_pem_private_key(key_file.read(), password=password)

    @staticmethod
    def load_public_key(filename):
        with open(filename, "rb") as key_file:
            return serialization.load_pem_public_key(key_file.read())

    @staticmethod
    def encrypt_file(input_filepath, output_filepath, public_key, key_size=2048):
        chunk_size = (key_size // 8) - 2 * hashes.SHA256().digest_size - 2
        
        with open(input_filepath, 'rb') as f_in, open(output_filepath, 'wb') as f_out:
            while True:
                chunk = f_in.read(chunk_size)
                if not chunk:
                    break
                encrypted_chunk = public_key.encrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                f_out.write(encrypted_chunk)

    @staticmethod
    def decrypt_file(input_filepath, output_filepath, private_key, key_size=2048):
        chunk_size = key_size // 8
        with open(input_filepath, 'rb') as f_in, open(output_filepath, 'wb') as f_out:
            while True:
                chunk = f_in.read(chunk_size)
                if not chunk:
                    break
                decrypted_chunk = private_key.decrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                f_out.write(decrypted_chunk)