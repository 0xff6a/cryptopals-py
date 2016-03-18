from nose.tools import *

from crypt.diffie_hellman import KeyPair

def test_key_pair():
    keys = KeyPair(37, 5)
    public_key = keys.get_public().bytes
    private_key = keys.get_secret().bytes

    assert_equal(public_key, [])
    assert_equal(private_key, [])
