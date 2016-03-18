from nose.tools import *

from utils import HashSet

def test_add():
    hashset = HashSet()
    hashset.add('element')

    assert_equal(hashset.to_list(), ['element'])

def test_remove():
    hashset = HashSet(['remove me'])
    hashset.remove('remove me')

    assert_equal(hashset.to_list(), [])

def test_clear():
    hashset = HashSet([1, 2, 3])
    hashset.clear()

    assert_equal(hashset.to_list(), [])

def test_contains():
    hashset = HashSet(['an element'])

    assert_is(hashset.contains('an element'), True)
    assert_is(hashset.contains('not an element'), False)
