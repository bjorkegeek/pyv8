import unittest
import PyV8
import json
import itertools

class Neq(object):
    def __eq__(self,other):
        return False

class PyV8Test(unittest.TestCase):
    def setUp(self):
        self.ctx = PyV8.JSContext()
        self.ctx.enter()
    
    def assertStrongerEqual(self,o1,o2):
        self.assertEqual(type(o1),type(o2))
        self.assertEqual(o1,o2)

    def assertSeqEqual(self,s1,s2):
        return all((i1==i2
                    for i1,i2
                    in itertools.izip_longest(s1,s2,fillvalue=Neq())))

class StringTests(PyV8Test):
    def test_js_to_py_string(self):
        self.assertStrongerEqual(self.ctx.eval('"abc"'),u"abc")

    def test_py_to_js_string(self):
        js_len = self.ctx.eval('(function(st) { return st.length; })')
        js_ord = self.ctx.eval('(function(st) { return st.charCodeAt(0); })')

        test_st = u'\xe4'

        self.assertStrongerEqual(len(test_st), js_len(test_st))
        self.assertStrongerEqual(ord(test_st), js_ord(test_st))

    def test_unicode_passthrough(self):
        addsomething = self.ctx.eval('(function(st) { return st+"x"; })')
        self.assertStrongerEqual(u"\xe4"+u"x",addsomething(u"\xe4"))

class ListTests(PyV8Test):
    def setUp(self):
        super(ListTests,self).setUp()
        self.py_list = [1,2,3,4,5]
        self.js_list = self.ctx.eval(json.dumps(self.py_list))
    
    def test_element_access(self):
        for i in xrange(len(self.py_list)):
            self.assertEqual(self.py_list[i],self.js_list[i])

    def test_reverse_element_access(self):
        for i in xrange(len(self.py_list)):
            self.assertEqual(self.py_list[-1-i],self.js_list[-1-i])

    def test_splice(self):
        py_mid = self.py_list[1:-1]
        js_mid = self.js_list[1:-1]
        for i, py_item in enumerate(py_mid):
            self.assertEqual(py_item, js_mid[i])

    def test_len(self):
        self.assertEqual(len(self.py_list),len(self.js_list))

    def test_iteration(self):
        self.assertSeqEqual(iter(self.py_list),iter(self.js_list))

class DictTests(PyV8Test):
    def setUp(self):
        super(self.__class__,self).setUp()
        self.py_dict = {u"a":3,u"b":4}
        self.js_dict = self.ctx.eval("("+json.dumps(self.py_dict)+")")

    def test_keys(self):
        self.assertSeqEqual(self.py_dict.keys(),self.js_dict.keys())
    
    def test_values(self):
        self.assertSeqEqual(self.py_dict.values(),self.js_dict.values())

    def test_items(self):
        self.assertSeqEqual(self.py_dict.items(),self.js_dict.items())

    def test_iterkeys(self):
        self.assertSeqEqual(self.py_dict.iterkeys(),self.js_dict.iterkeys())

    def test_itervalues(self):
        self.assertSeqEqual(self.py_dict.itervalues(),self.js_dict.itervalues())

    def test_iteritems(self):
        self.assertSeqEqual(self.py_dict.iteritems(),self.js_dict.iteritems())

if __name__ == '__main__':
    unittest.main()
