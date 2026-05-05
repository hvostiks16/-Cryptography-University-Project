import os
import pytest
from labs.lab5_dsa import DSACore
from cryptography.hazmat.primitives.asymmetric import dsa

def test_generate_keys():
    priv, pub = DSACore.generate_keys(key_size=1024)
    assert isinstance(priv, dsa.DSAPrivateKey)
    assert isinstance(pub, dsa.DSAPublicKey)

def test_save_and_load_keys(tmp_path):
    priv_file = tmp_path / "priv.pem"
    pub_file = tmp_path / "pub.pem"
    
    priv, pub = DSACore.generate_keys(1024)
    
    DSACore.save_private_key(priv, str(priv_file))
    DSACore.save_public_key(pub, str(pub_file))
    
    assert os.path.exists(priv_file)
    assert os.path.exists(pub_file)
    
    loaded_priv = DSACore.load_private_key(str(priv_file))
    loaded_pub = DSACore.load_public_key(str(pub_file))
    
    assert isinstance(loaded_priv, dsa.DSAPrivateKey)
    assert isinstance(loaded_pub, dsa.DSAPublicKey)

def test_sign_and_verify_correct():
    priv, pub = DSACore.generate_keys(1024)
    data = b"Hello, DSS!"
    
    signature = DSACore.sign_data(priv, data)
    assert isinstance(signature, bytes)
    
    is_valid = DSACore.verify_signature(pub, signature, data)
    assert is_valid is True

def test_verify_incorrect_data():
    priv, pub = DSACore.generate_keys(1024)
    data = b"Original Data"
    wrong_data = b"Modified Data"
    
    signature = DSACore.sign_data(priv, data)
    is_valid = DSACore.verify_signature(pub, signature, wrong_data)
    
    assert is_valid is False

def test_verify_incorrect_signature():
    priv, pub = DSACore.generate_keys(1024)
    data = b"Data"
    
    fake_signature = b"a" * 40 
    
    is_valid = DSACore.verify_signature(pub, fake_signature, data)
    assert is_valid is False

def test_sign_verify_hex_flow():
    priv, pub = DSACore.generate_keys(1024)
    data = b"Hex workflow test"
    
    sig = DSACore.sign_data(priv, data)
    sig_hex = sig.hex()
    
    sig_from_hex = bytes.fromhex(sig_hex)
    assert DSACore.verify_signature(pub, sig_from_hex, data) is True