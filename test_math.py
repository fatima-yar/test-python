import pytest
from math_module import add 

def test_add():
    assert add(2, 6) == 8

#to run the test
#pytest test_math.py
