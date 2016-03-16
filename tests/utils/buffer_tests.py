from nose.tools import *

from utils import *

def test_properties():
    buf = Buffer([1, 2, 3])

    assert_equal(buf.bytes, [1, 2, 3])
    assert_equal(buf.size, 3)

def test_get():
    buf = Buffer([0, 16, 0])

    assert_equal(buf.get(1), 16)

def test_set():
    buf = Buffer([0, 0, 0, 0])
    buf.set(1, 16)

    assert_equal(buf.get(1), 16)

def test_init():
    buf = Buffer.init(5, 16)

    assert_equal(buf.bytes, [16, 16, 16, 16, 16])

def test_to_b64():
    buf = Buffer('base64 test')

    assert_equal(buf.to_b64(), 'YmFzZTY0IHRlc3Q=')

def test_from_b64():
    buf = Buffer.from_b64('aGVsbG8=')

    assert_equal(buf.to_string(), 'hello')

def test_to_hex():
    buf = Buffer('hex test')

    assert_equal(buf.to_hex(), '6865782074657374')

def test_from_hex():
    buf = Buffer.from_hex('68656c6c6f')

    assert_equal(buf.to_string(), 'hello')

def test_to_bin():
    buf = Buffer('Az')

    assert_equal(buf.to_bin(), '0100000101111010')

def test_from_bin():
    buf = Buffer.from_bin('0100000101111010')

    assert_equal(buf.to_string(), 'Az')

def test_xor():
    buf1 = Buffer('abc')
    buf2 = Buffer('   ')
    xord = buf1.xor(buf2)

    assert_equal(xord.to_string(), 'ABC')
