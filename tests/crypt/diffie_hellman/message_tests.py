from nose.tools import *

from crypt.diffie_hellman import Message

def test_buffer():
    msg = Message(Message.FIX_PARAMS, dh_p='ff', dh_g='ee')

    assert_equal(msg.buffer,
        "\x00\x00\x00\x01\x00\x00\x00\x02ff" +
        "\x00\x00\x00\x00\x00\x02ee\x00\x00"
    )

def test_fix_params():
    msg = Message(Message.FIX_PARAMS, dh_p='37', dh_g='5')

    assert_equal(msg.data, { 'code' : 1, 'dh_p' : '37', 'dh_g' : '5' })

def test_key_exchg():
    msg = Message(Message.KEY_EXCHG, public_key='ffffffff')

    assert_equal(msg.data, { 'code' : 2, 'public_key' : 'ffffffff' })
