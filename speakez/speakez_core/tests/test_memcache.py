from django.test import TestCase
from django.core.cache import cache


class MemcacheTestCase(TestCase):
    def setUp(self):
        cache.set('1', 'one')
        cache.set('2', 'two')
        cache.set('3', 'three')
        cache.set('4', 'four')
        cache.set('5', 'five')

    def test_cache_get(self):
        print('==================memcache test result===================')
        print(cache.get('1'))
        print(cache.get('2'))
        print(cache.get('3'))
        print(cache.get('4'))
        print(cache.get('5'))
        print('==================memcache test result===================')

