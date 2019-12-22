import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from binary import Binary
import pytest

@pytest.mark.description("test int conversion of binary")
def test_binary_init_int():
    binary = Binary(6)
    assert int(binary) == 6

def test_binary_init_bitstr():
    binary = Binary('110')
    assert int(binary) == 6

def test_binary_init_binstr():
    binary = Binary('0b110')
    assert int(binary) == 6

def test_binary_init_hexstr():
    binary = Binary('0x6')
    assert int(binary) == 6

def test_binary_init_hex():
    binary = Binary(0x6)
    assert int(binary) == 6

def test_binary_init_intseq():
    binary = Binary([1,1,0])
    assert int(binary) == 6

def test_binary_init_strseq():
    binary = Binary(['1','1','0'])
    assert int(binary) == 6

def test_binary_init_negative():
    with pytest.raises(ValueError):
        binary = Binary(-4)
        assert int(binary) == -4