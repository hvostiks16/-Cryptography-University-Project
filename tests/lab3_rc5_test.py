import pytest
from unittest.mock import patch, MagicMock
from labs.lab3_rc5 import RC5Core, RC5Manager

@pytest.fixture
def rc5_instance():
    key = b'\x00' * 16
    return RC5Core(key, w=64, r=8)


def test_rotations(rc5_instance):
    assert rc5_instance.rotl(1, 1) == 2
    assert rc5_instance.rotr(2, 1) == 1
    
    max_val = rc5_instance.mask
    assert rc5_instance.rotl(max_val, 5) == max_val
    assert rc5_instance.rotr(max_val, 5) == max_val


def test_block_encryption_decryption(rc5_instance):
    data = b'1234567890abcdef'
    
    cipher_block = rc5_instance.encrypt_block(data)
    assert data != cipher_block 
    
    plain_block = rc5_instance.decrypt_block(cipher_block)
    assert data == plain_block


@patch('labs.lab3_rc5.MD5Core.hash_string')
def test_derive_key(mock_md5_hash):
    mock_md5_hash.return_value = 'a' * 32
    
    assert len(RC5Manager.derive_key("password", 64)) == 8
    assert len(RC5Manager.derive_key("password", 128)) == 16
    assert len(RC5Manager.derive_key("password", 256)) == 32
    assert mock_md5_hash.called


@patch('labs.lab3_rc5.LCGCore')
def test_generate_iv(MockLCGCore):
    mock_lcg_instance = MagicMock()
    mock_lcg_instance.lcg.return_value = [255] * 16 
    MockLCGCore.return_value = mock_lcg_instance
    
    iv = RC5Manager.generate_iv()
    assert len(iv) == RC5Manager.BLOCK_SIZE
    assert iv == b'\xff' * 16


@pytest.mark.parametrize("original_data, description", [
    (b"", "empty_file"),
    (b"hello", "partial_block"),
    (b"1234567890abcdef", "exact_single_block"),
    (b"1234567890abcdef_extra_data_here", "multi_block")
])

def test_file_encryption_decryption_integration(tmp_path, original_data, description):
    file_in = tmp_path / f"in_{description}.bin"
    file_enc = tmp_path / f"enc_{description}.enc"
    file_dec = tmp_path / f"dec_{description}.bin"

    file_in.write_bytes(original_data)
    password = "super_secure_password"

    RC5Manager.encrypt_file(str(file_in), str(file_enc), password, key_size_bits=128)
    RC5Manager.decrypt_file(str(file_enc), str(file_dec), password, key_size_bits=128)

    decrypted_data = file_dec.read_bytes()
    assert original_data == decrypted_data