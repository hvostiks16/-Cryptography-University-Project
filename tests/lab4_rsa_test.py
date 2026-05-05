import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from labs.lab4_rsa import RSACore
import os

@pytest.fixture(scope="module")
def rsa_keys():
    return RSACore.generate_keys(key_size=2048)

def test_keys_generation(rsa_keys):
    priv, pub = rsa_keys
    assert priv is not None
    assert pub is not None
    assert isinstance(priv, rsa.RSAPrivateKey)
    assert isinstance(pub, rsa.RSAPublicKey)

def test_save_load_keys_no_password(tmp_path, rsa_keys):
    priv_key, pub_key = rsa_keys
    priv_path = tmp_path / "priv.pem"
    pub_path = tmp_path / "pub.pem"
    
    RSACore.save_private_key(priv_key, str(priv_path))
    RSACore.save_public_key(pub_key, str(pub_path))
    
    assert priv_path.exists()
    assert pub_path.exists()
    
    loaded_priv = RSACore.load_private_key(str(priv_path))
    loaded_pub = RSACore.load_public_key(str(pub_path))
    
    assert loaded_priv is not None
    assert loaded_pub is not None

def test_save_load_keys_with_password(tmp_path, rsa_keys):
    priv_key, _ = rsa_keys
    priv_path = tmp_path / "priv_enc.pem"
    password = b"super_secret_password"
 
    RSACore.save_private_key(priv_key, str(priv_path), password=password)
    assert priv_path.exists()
    
    loaded_priv = RSACore.load_private_key(str(priv_path), password=password)
    assert loaded_priv is not None

def test_encrypt_decrypt_empty_file(tmp_path, rsa_keys):
    priv_key, pub_key = rsa_keys
    empty_in = tmp_path / "empty.txt"
    empty_enc = tmp_path / "empty.rsa"
    empty_dec = tmp_path / "empty_dec.txt"
    
    empty_in.write_bytes(b"")
    
    RSACore.encrypt_file(str(empty_in), str(empty_enc), pub_key)
    RSACore.decrypt_file(str(empty_enc), str(empty_dec), priv_key, key_size=2048)
    
    assert empty_dec.read_bytes() == b""

def test_file_encryption_decryption_roundtrip(tmp_path, rsa_keys):
    priv_key, pub_key = rsa_keys
    original_file = tmp_path / "original.txt"
    encrypted_file = tmp_path / "encrypted.rsa"
    decrypted_file = tmp_path / "decrypted.txt"
    
    test_data = b"Hello, RSA Encryption! This is a test file for Lab 4." * 50
    original_file.write_bytes(test_data)
  
    RSACore.encrypt_file(str(original_file), str(encrypted_file), pub_key)
    assert encrypted_file.exists()
    assert encrypted_file.read_bytes() != test_data

    RSACore.decrypt_file(str(encrypted_file), str(decrypted_file), priv_key, key_size=2048)
    assert decrypted_file.exists()

    assert decrypted_file.read_bytes() == test_data

def test_encrypt_decrypt_exact_chunk_size(tmp_path, rsa_keys):
    priv_key, pub_key = rsa_keys
    original_file = tmp_path / "exact.txt"
    encrypted_file = tmp_path / "exact.rsa"
    decrypted_file = tmp_path / "exact_dec.txt"
    test_data = os.urandom(190)
    original_file.write_bytes(test_data)
    
    RSACore.encrypt_file(str(original_file), str(encrypted_file), pub_key)
    RSACore.decrypt_file(str(encrypted_file), str(decrypted_file), priv_key, key_size=2048)
    
    assert decrypted_file.read_bytes() == test_data