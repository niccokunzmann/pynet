import unittest
import pickle
import VeryPicklableObject
from VeryPicklableObject import PicklableType, X, picklable, picklableAttribute

class PicklableSubclass(object):

    a = 1
    @picklable
    def someMethod(self):
        return 1

    @picklable
    @classmethod
    def clsMethod(cls):
        return 2

    @picklable
    @staticmethod
    def staticMethod():
        return 3

    def __eq__(self, other):
        return self.__class__ == other.__class__

class PicklabilityTestBase(unittest.TestCase):

    def assertPickles(self, obj):
        s = pickle.dumps(obj)
        obj2 = pickle.loads(s)
        self.assertEquals(obj2, obj)


class PicklabilityTest(PicklabilityTestBase):

    P = PicklableSubclass

    def setUp(self):
        self.p = self.P()

    def test_pickle(self):
        self.assertPickles(self.p)

    def test_pickle_instance_methods_raw(self):
        self.assertPickles(self.P.__dict__['someMethod'])

    def test_pickle_class_methods_raw(self):
        self.assertPickles(self.P.__dict__['clsMethod'])

    def test_pickle_static_methods_raw(self):
        self.assertPickles(self.P.__dict__['staticMethod'])

    def test_pickle_instance_methods_cls(self):
        self.assertPickles(self.P.someMethod)

    def test_pickle_class_methods_cls(self):
        self.assertPickles(self.P.clsMethod)

    def test_pickle_static_methods_cls(self):
        self.assertPickles(self.P.staticMethod)

    def test_pickle_instance_methods(self):
        self.assertPickles(self.p.someMethod)

    def test_pickle_class_methods(self):
        self.assertPickles(self.p.clsMethod)

    def test_pickle_static_methods(self):
        self.assertPickles(self.p.staticMethod)

    def test_exec_static_methods(self):
        self.assertEquals(self.p.staticMethod(), 3)

    def test_exec_class_methods(self):
        self.assertEquals(self.p.clsMethod(), 2)

    def test_exec_instance_methods(self):
        self.assertEquals(self.p.someMethod(), 1)


class PicklableTypeTest(unittest.TestCase):

    def setUp(self):
        self.pt = PicklableType(int)

    def test_pickle_identity(self):
        s = pickle.dumps(self.pt)
        obj2 = pickle.loads(s)
        self.assertIs(obj2, self.pt)

    def test_calls_type(self):
        self.pt.picklable = lambda x: x
        self.assertEquals(self.pt('23'), 23)

@picklable
def f():pass

class picklableTest(PicklabilityTestBase):

    def test_twice_picklable_is_once_picklable(self):
        self.assertIs(picklable(f), f)

class Z(object):

    @picklableAttribute
    def f(self):
        return 1

    @picklableAttribute
    def g(self):
        return [1,2,3,4]

    @picklableAttribute
    def h():pass
    _h = h
    h = 3

    def __eq__(self, other):
        return type(self) == type(other)


class TestAccessibleAttribute(PicklabilityTestBase):

    Z = Z

    def setUp(self):
        self.z = self.Z()

    def test_can_be_called_f(self):
        self.assertEquals(self.z.f(), 1)
    
    def test_can_be_called_g(self):
        self.assertEquals(self.z.g(), [1,2,3,4])

    def test_pickles_of_instance(self):
        self.assertPickles(self.z.f)
        self.assertPickles(self.z.g)

    def test_pickles_of_class(self):
        self.assertPickles(self.Z.f)
        self.assertPickles(self.Z.g)

    def test_can_compare_functions(self):
        self.assertEquals(self.z.f, self.z.f)
        self.assertIsNot(self.z.f, self.z.f)

    def test_if_not_accessible_error(self):
        self.assertRaises(AssertionError,
                          lambda: self.z._h)
    
    def test_if_not_accessible_error_class(self):
        self.assertRaises(AssertionError,
                          lambda: self.Z._h)
    

if __name__ == '__main__':
    unittest.main(exit = False, verbosity = 1)
