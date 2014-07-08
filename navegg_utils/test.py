#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
import unittest
from selenium import webdriver


class NaveggBaseTest(unittest.TestCase):

    '''Use these clausules to test:

    self.assertEqual(a, b)                                   a == b
    self.assertNotEqual(a, b)                                a != b
    self.assertTrue(x)                                       bool(x) is True
    self.assertFalse(x)                                      bool(x) is False
    self.assertIs(a, b)                                      a is b
    self.assertIsNot(a, b)                                   a is not b
    self.assertIsNone(x)                                     x is None
    self.assertIsNotNone(x)                                  x is not None
    self.assertIn(a, b)                                      a in b
    self.assertNotIn(a, b)                                   a not in b
    self.assertIsInstance(a, b)                              isinstance(a, b)
    self.assertNotIsInstance(a, b)                           not isinstance(a, b)
    self.assertRaises(exc, fun, *args, **kwds)               fun(*args, **kwds) raises exc
    self.assertRaisesRegexp(exc, r, fun, *args, **kwds)      fun(*args, **kwds) raises exc and the message matches regex r
    self.assertAlmostEqual(a, b)                             round(a-b, 7) == 0
    self.assertNotAlmostEqual(a, b)                          round(a-b, 7) != 0
    self.assertGreater(a, b)                                 a > b
    self.assertGreaterEqual(a, b)                            a >= b
    self.assertLess(a, b)                                    a < b
    self.assertLessEqual(a, b)                               a <= b
    self.assertRegexpMatches(s, r)                           r.search(s)
    self.assertNotRegexpMatches(s, r)                        not r.search(s)
    self.assertItemsEqual(a, b)                              sorted(a) == sorted(b) and works with unhashable objs
    self.assertDictContainsSubset(a, b)                      all the key/value pairs in a exist in b
    self.assertMultiLineEqual(a, b)                          strings
    self.assertSequenceEqual(a, b)                           sequences
    self.assertListEqual(a, b)                               lists
    self.assertTupleEqual(a, b)                              tuples
    self.assertSetEqual(a, b)                                sets or frozensets
    self.assertDictEqual(a, b)                               dicts'''

    def setUp(self):
        '''Write in this function all the actions to execute on setup of the test'''
        pass

    def tearDown(self):
        '''Write in this function all the actions to execute on destruction of the test'''
        pass

    def run(self, result=None):
        super(NaveggBaseTest, self).run(result)

    @staticmethod
    def go():
        unittest.main()


class NaveggTest(NaveggBaseTest):

    '''To use this class in test case do:

1. create a file with this content:

from navegg_utils import NaveggTest

class MyTest(NaveggTest):

    def setUp(self):
        self.a = 1
        self.b = 1

    def test_sum(self):
        self.assertEqual(2, self.a+self.b)

if __name__ == '__main__':
    MyTest.go()

2. run python myfile.py (myfile is a name for a file)

To alter tests you only need create new defs contains unittest clauses'''

    pass


class NaveggWebTest(NaveggBaseTest):

    '''Please, read the documentation [1]

To use this class in test case do:

1. create a file with this content:

from navegg_utils import NaveggWebTest

class MyTest(NaveggWebTest):

    def setUp(self):
        self.driver.get("http://www.navegg.com/")

    def test_title(self):
        self.assertIn("Navegg", self.driver.title)

if __name__ == '__main__':
    MyTest.go()

2. run python myfile.py (myfile is a name for a file)

To alter tests you only need create new defs contains unittest clauses
and change the URL in the setUp

[1] http://selenium-python.readthedocs.org/en/latest/getting-started.html'''

    def __init__(self, *args, **kwargs):
        '''Overwrite the __init__ function to add the chromedrive based on system architecture'''

        pwd = os.path.dirname(os.path.realpath(__file__))
        if '64' in platform.architecture()[0]:
            chromedrive = os.path.join(pwd, 'chromedriver_x64')
        else:
            chromedrive = os.path.join(pwd, 'chromedriver_x86')

        self.driver_list = [webdriver.Firefox(), webdriver.Chrome(chromedrive)]

        super(NaveggWebTest, self).__init__(*args, **kwargs)

    def tearDown(self):
        '''writed here the destruction of the webdrivers after finish the tests'''
        self.driver.close()

    def run(self, result=None):
        for driver in self.driver_list:
            self.driver = driver
            try:
                super(NaveggWebTest, self).run(result)
            except Exception as e:
                print 'Fail: {}'.format(e)
                continue
