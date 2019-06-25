from django.test import TestCase
from django.core.cache import cache
import uuid


class MemcacheTestCase(TestCase):
    def test_cache_get(self):
        one = uuid.uuid4().hex
        two = uuid.uuid4().hex
        three = uuid.uuid4().hex
        four = uuid.uuid4().hex
        five = uuid.uuid4().hex
        cache.set(one, 'one')
        cache.set(two, 'two')
        cache.set(three, 'three')
        cache.set(four, 'four')
        cache.set(five, 'five')
        print('==================memcache test result===================')
        print(cache.get(one))
        print(cache.get(two))
        print(cache.get(three))
        print(cache.get(four))
        print(cache.get(five))
        print('==================memcache test result===================')

