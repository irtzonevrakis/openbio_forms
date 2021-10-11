import unittest
from fd_parser import parse_field_definition
class test_field_parser(unittest.TestCase):
    def test_int(self):
        l = 'test_field,This is a test field.,int,10,none,none,TEST\n'
        obj = parse_field_definition(l)
        self.assertEqual(set(obj.keys()), set(['name', 
                                               'descr', 
                                               'type', 
                                               'cast_function',
                                               'default_value',
                                               'lim_min',
                                               'lim_max',
                                               'stored_name']))
        self.assertEqual(obj['name'], 'test_field')
        self.assertEqual(obj['descr'], 'This is a test field.')
        self.assertEqual(obj['type'], 'int')
        self.assertEqual(obj['default_value'], 10)
        self.assertIsNone(obj['lim_min'])
        self.assertIsNone(obj['lim_max'])
        self.assertEqual(obj['stored_name'], 'TEST')
    def test_str(self):
        l = 'test_field,This is a test field.,str,Hello World!,256,TEST\n'
        obj = parse_field_definition(l)
        self.assertEqual(set(obj.keys()), set(['name', 
                                               'descr', 
                                               'type', 
                                               'cast_function',
                                               'default_value',
                                               'lim_max',
                                               'stored_name']))
        self.assertEqual(obj['name'], 'test_field')
        self.assertEqual(obj['descr'], 'This is a test field.')
        self.assertEqual(obj['type'], 'str')
        self.assertEqual(obj['default_value'], 'Hello World!')
        self.assertEqual(obj['lim_max'], 256)
        self.assertEqual(obj['stored_name'], 'TEST')
    def test_str_no_maxlen(self):
        l = 'test_field,This is a test field.,str,Hello World!,none,TEST\n'
        obj = parse_field_definition(l)
        self.assertEqual(set(obj.keys()), set(['name', 
                                               'descr', 
                                               'type', 
                                               'cast_function',
                                               'default_value',
                                               'lim_max',
                                               'stored_name']))
        self.assertEqual(obj['name'], 'test_field')
        self.assertEqual(obj['descr'], 'This is a test field.')
        self.assertEqual(obj['type'], 'str')
        self.assertEqual(obj['default_value'], 'Hello World!')
        self.assertEqual(obj['lim_max'], None)
        self.assertEqual(obj['stored_name'], 'TEST')

    def test_str_default_ol(self):
        l = 'test_field,This is a test field.,str,Hello World!,3,TEST\n'
        with self.assertRaises(ValueError):
            self.assertRaises(parse_field_definition(l))
    def test_int_default_ol(self):
        l = 'test_field,This is a test field.,int,10,0,5,TEST\n'
        with self.assertRaises(ValueError):
            self.assertRaises(parse_field_definition(l))
    def test_int_default_ul(self):
        l = 'test_field,This is a test field.,int,-1,0,5,TEST\n'
        with self.assertRaises(ValueError):
            self.assertRaises(parse_field_definition(l))
    def test_float(self):
        l = 'test_field,This is a test field.,float,3.141,none,none,TEST\n'
        obj = parse_field_definition(l)
        self.assertEqual(set(obj.keys()), set(['name', 
                                               'descr', 
                                               'type', 
                                               'cast_function',
                                               'default_value',
                                               'lim_min',
                                               'lim_max',
                                               'stored_name']))
        self.assertEqual(obj['name'], 'test_field')
        self.assertEqual(obj['descr'], 'This is a test field.')
        self.assertEqual(obj['type'], 'float')
        self.assertEqual(obj['default_value'], 3.141)
        self.assertIsNone(obj['lim_min'])
        self.assertIsNone(obj['lim_max'])
        self.assertEqual(obj['stored_name'], 'TEST')
    def test_float_default_ol(self):
        l = 'test_field,This is a test field.,float,10,0,5,TEST\n'
        with self.assertRaises(ValueError):
            self.assertRaises(parse_field_definition(l))
    def test_float_default_ul(self):
        l = 'test_field,This is a test field.,float,-1,0,5,TEST\n'
        with self.assertRaises(ValueError):
            self.assertRaises(parse_field_definition(l))
    def test_file(self):
        l = 'test_field,This is a test field.,file.h5,TEST\n'
        obj = parse_field_definition(l)
        self.assertEqual(set(obj.keys()), set(['name', 
                                               'descr', 
                                               'type', 
                                               'cast_function',
                                               'stored_name']))
        self.assertEqual(obj['name'], 'test_field')
        self.assertEqual(obj['descr'], 'This is a test field.')
        self.assertEqual(obj['type'], 'file.h5')
        self.assertEqual(obj['stored_name'], 'TEST')

if __name__ == '__main__':
    unittest.main()
