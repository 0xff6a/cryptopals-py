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

def test_from_fix_params_buffer():
    data = (
        "\x00\x00\x00\x01\x00\x00\x00\x02ff" +
        "\x00\x00\x00\x00\x00\x02ee\x00\x00"
    )

    msg = Message.from_buffer(data)

    assert_equal(msg.data, { 'code' : 1, 'dh_p' : 'ff', 'dh_g' : 'ee' })

def test_key_exchg():
    msg = Message(Message.KEY_EXCHG, public_key='ffffffff')

    assert_equal(msg.data, { 'code' : 2, 'public_key' : 'ffffffff' })

def test_from_key_exchg_buffer():
    data = "\x00\x00\x00\x02\x00\x00\x00\x08ffffffff"
    msg = Message.from_buffer(data)

    assert_equal(msg.data, { 'code' : 2, 'public_key' : 'ffffffff' })

def test_send_enc():
    msg = Message(Message.SEND_ENC, server_msg='hello')

    assert_equal(msg.data, { 'code' : 3, 'server_msg' : 'hello' })

def test_from_send_enc_buffer():
    data = "\x00\x00\x00\x03\x00\x00\x00\x05hello\x00\x00\x00"
    msg = Message.from_buffer(data)

    assert_equal(msg.data, { 'code' : 3, 'server_msg' : 'hello' })

def test_recv_enc():
    msg = Message(Message.RECV_ENC, client_msg='bye!')

    assert_equal(msg.data, { 'code' : 4, 'client_msg' : 'bye!' })

def test_from_recv_enc_buffer():
    data = "\x00\x00\x00\x04\x00\x00\x00\x04bye!\x00\x00\x00"
    msg = Message.from_buffer(data)

    assert_equal(msg.data, { 'code' : 4, 'client_msg' : 'bye!' })
