import tempfile
import os
import pytest
from labs.lab2_md5 import MD5Core


# --- Hash string ---
def test_hash_string_known_values():
    cases = {
        "": "D41D8CD98F00B204E9800998ECF8427E",
        "a": "0CC175B9C0F1B6A831C399E269772661",
        "abc": "900150983CD24FB0D6963F7D28E17F72",
        "message digest": "F96B697D7CB7938D525A2F31AAF161D0",
        "abcdefghijklmnopqrstuvwxyz": "C3FCD3D76192E4007DFB496CCA67E13B",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789": "D174AB98D277D9F5A5611C2C9F419D9F",
        "12345678901234567890123456789012345678901234567890123456789012345678901234567890": "57EDF4A22BE3C955AC49DA2E2107B67A"
    }
    for s, expected in cases.items():
        assert MD5Core.hash_string(s) == expected


def test_hash_string_empty():
    assert MD5Core.hash_string("") == "D41D8CD98F00B204E9800998ECF8427E"


# --- Hash file ---
def test_hash_file_correct(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("abc", encoding="utf-8")
    h = MD5Core.hash_file(str(file))
    assert h == "900150983CD24FB0D6963F7D28E17F72"


def test_hash_file_empty(tmp_path):
    file = tmp_path / "empty.txt"
    file.write_text("", encoding="utf-8")
    h = MD5Core.hash_file(str(file))
    assert h == "D41D8CD98F00B204E9800998ECF8427E"


# --- Verify file ---
def test_verify_file_true(tmp_path):
    file = tmp_path / "data.txt"
    file.write_text("abc", encoding="utf-8")
    md5_value = MD5Core.hash_file(str(file))
    md5_file = tmp_path / "data.txt.md5"
    md5_file.write_text(md5_value, encoding="utf-8")

    assert MD5Core.verify_file(str(file), str(md5_file))


def test_verify_file_false(tmp_path):
    file = tmp_path / "data.txt"
    file.write_text("abc", encoding="utf-8")
    md5_file = tmp_path / "data.txt.md5"
    md5_file.write_text("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF", encoding="utf-8")

    assert not MD5Core.verify_file(str(file), str(md5_file))