import math
import random
import pytest
from labs.lab1_lcg import LCGCore


@pytest.fixture
def core():
    return LCGCore()


# --- LCG ---
def test_lcg_generates_correct_length(core):
    seq = core.lcg(10)
    assert len(seq) == 10

def test_lcg_values_in_range(core):
    seq = core.lcg(100)
    assert all(0 <= x < core.m for x in seq)

def test_lcg_reproducibility(core):
    seq1 = core.lcg(20)
    seq2 = core.lcg(20)
    assert seq1 == seq2

def test_lcg_zero(core):
    seq = core.lcg(0)
    assert seq == []


# --- GCD ---
def test_gcd_basic_cases():
    assert LCGCore.gcd(10, 5) == 5
    assert LCGCore.gcd(17, 13) == 1
    assert LCGCore.gcd(0, 5) == 5
    assert LCGCore.gcd(5, 0) == 5


# --- Period ---
def test_lcg_period_positive(core):
    period = core.lcg_period()
    assert period > 0
    assert period <= core.m


# --- Estimate π (LCG) ---
def test_estimate_pi_lcg_returns_float(core):
    result = core.estimate_pi_lcg(1000)
    assert isinstance(result, float)

def test_estimate_pi_lcg_not_none(core):
    result = core.estimate_pi_lcg(100)
    assert result is not None

def test_estimate_pi_lcg_close_to_real(core):
    result = core.estimate_pi_lcg(5000)
    assert abs(result - math.pi) < 0.5


# --- Estimate π (System random) ---
def test_estimate_pi_system_returns_float(core):
    random.seed(0)
    result = core.estimate_pi_system(1000)
    assert isinstance(result, float)

def test_estimate_pi_system_not_none(core):
    random.seed(0)
    result = core.estimate_pi_system(100)
    assert result is not None

def test_pi_system_close_to_real(core):
    random.seed(0)
    result = core.estimate_pi_system(5000)
    assert abs(result - math.pi) < 0.5
