from nose.tools import *

from utils import *

def test_properties():
    buf = Buffer([1, 2, 3])

    assert_equal(buf.bytes, [1, 2, 3])
    assert_equal(buf.size, 3)

def test_init():
    buf = Buffer.init(5, 16)

    assert_equal(buf.bytes, [16, 16, 16, 16, 16])

def test_to_base64():
    buf = Buffer('base64 test')

    assert_equal(buf.to_base64(), 'YmFzZTY0IHRlc3Q=')

def test_to_hex():
    buf = Buffer('hex test')

    assert_equal(buf.to_hex(), '6865782074657374')

def test_to_bin():
    buf = Buffer('Az')

    assert_equal(buf.to_bin(), '0100000101111010')
