from nose.tools import *

from crypt.diffie_hellman import KeyPair

def test_key_pair():
    alice_keys = KeyPair(37, 5)
    bob_keys = KeyPair(37, 5)

    assert_not_equal(alice_keys.get_public(), bob_keys.get_public())
    assert_not_equal(alice_keys.get_secret(), bob_keys.get_secret())

def test_session_key():
    alice_keys = KeyPair(37, 5)
    bob_keys = KeyPair(37, 5)

    alice_secret = alice_keys.session_key(bob_keys.get_public())
    bob_secret = bob_keys.session_key(alice_keys.get_public())

    assert_equal(alice_secret.bytes, bob_secret.bytes)

def test_real_session_key():
    alice_keys = KeyPair() # uses NIST parameters by default
    bob_keys = KeyPair() # uses NIST parameters by default

    alice_secret = alice_keys.session_key(bob_keys.get_public())
    bob_secret = bob_keys.session_key(alice_keys.get_public())

    assert_equal(alice_secret.bytes, bob_secret.bytes)
