from nose.tools import *

from utils import *

def test_properties():
    buf = Buffer([1,2,3])

    assert_equal(buf.bytes, [1,2,3])
    assert_equal(buf.size, 3)
