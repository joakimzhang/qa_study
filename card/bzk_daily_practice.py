import unittest
import pdb
import os
import binascii
import array


class SimplisticTest(unittest.TestCase):

    def test(self):
        self.failUnless(True)


class OutcomesTest(unittest.TestCase):
    def testPass(self):
        return
    '''
    def testFail(self):
        self.failIf(True)

    def testError(self):
        raise RuntimeError('Test error!')
    '''


class TruthTest(unittest.TestCase):

    def testFailUnless(self):
        self.failUnless(True)

    def testAssertTrue(self):
        self.assertTrue(True)

    def testFailIf(self):
        self.failIf(False)

    def testAssertFalse(self):
        self.assertFalse(False, "the assert false")


class FixturesTest(unittest.TestCase):

    def setUp(self):
        print 'In setUp()'
        self.fixture = range(1, 10)

    def tearDown(self):
        print 'in teardown()'
        del self.fixture

    def test(self):
        print 'In test()'
        self.failUnlessEqual(self.fixture, range(1, 10))


class MyObj(object):

    def __init__(self, num_loops):
        self.num_loops = num_loops
        print "init"

    def go(self):

        for i in range(self.num_loops):
            print i
        return


class GetWalk(object):

    def __init__(self, _root_path):
        self.root_path = _root_path

    def get_walk(self):
        contents = os.walk(self.root_path)
        for _dir, sub_dir, _file in contents:
            print _dir+"\\"
            for i in sub_dir:
                print i+"\\"
            for j in _file:
                print j

            print


class BinArray(object):
    def testbin(self):
        a = "a"
        a = array.array("c", a)
        print a
        print binascii.hexlify(a)
        for i, j in enumerate(a):
            print i, j

import tempfile
class FileToArray(object):

    def read_file(self):
        a = array.array('i', xrange(11))
        #a.byteswap()
        print "A1:", a
        with open("test.txt", "rb") as _read:
            print binascii.hexlify(_read.read())


        output = open("test.txt", "wb")
        a.tofile(output)
        print output.name
        output.close()

        with open("test.txt", "rb") as _read:
            print binascii.hexlify(_read.read())
            print "aaaaaaaa"


        with open(output.name, 'rb') as input:

            raw_data = input.read()

            print len(raw_data)
            print type(raw_data)
            print 'raw contents:%s' % binascii.b2a_hex(raw_data)

            input.seek(0)

            a2 = array.array('i')
            a2.fromfile(input, len(a))
            print "len(a):", len(a)
            print "A2:", a2


import struct
import binascii


class StructTest(object):

    def test_struct(self):
        values = (1, 'ab', 2.7)
        s = struct.Struct('I 2s f')
        packed_data = s.pack(*values)
        print 'Original values:', values
        print 'Format string:', s.format
        print 'Uses:', s.size, 'bytes'
        print 'packed value:', binascii.hexlify(packed_data)
        print binascii.unhexlify("61")

    def test_struct_endianness(self):
        values = (1, 'ab', 2.7)
        endianness = [('@', 'native,native'),
                      ('=', 'native, standard'),
                      ('<', 'little-endian'),
                      ('>', 'big-endian'),
                      ('!', 'network'),
                      ]
        for code, name in endianness:
            s = struct.Struct(code + ' I 2s f')
            packed_data = s.pack(*values)


            print
            print 'format string:', s.format, 'for', name
            print 'uses:', s.size, 'bytes'
            print 'packed value:', binascii.hexlify(packed_data)
            print 'unpacked value:', s.unpack(packed_data)
    
    def struct_buffer(self):
        s = struct.Struct('I 2s f')
        values = (1, 'ab', 2.7)
        print 'original:', values
        print
        print 'ctypes string buffer'
        import ctypes
        b = ctypes.create_string_buffer(s.size)
        print 'before:', binascii.hexlify(b.raw)
        s.pack_into(b, 0, *values)
        print 'After :', binascii.hexlify(b.raw)
        print 'unpacked:', s.unpack_from(b, 0)
        print
        print 'array'
        
        import array
        a = array.array('c', '\0' * s.size)
        print 'before:', binascii.hexlify(a)
        s.pack_into(a, 0, *values)
        print 'after:', binascii.hexlify(a)
        print 'unpacked:', s.unpack_from(a, 0)


import datetime
class DatetimeTest(object):

    def time_test(self):
        c_time = datetime.datetime.now()
        print c_time.strftime('%Y-%m-%d %H:%M:%S')
        

if __name__ == '__main__':
    #pdb.set_trace()
    # unittest.main()
    #MyObj(5).go()
    #GetWalk("D:\djtest").get_walk()
    #BinArray().testbin()
    #FileToArray().read_file()
   #with open("test.txt", "rb") as a:
   #    print a.read()
    #StructTest().test_struct_endianness()
    #StructTest().struct_buffer()
    #DatetimeTest().time_test()
    StructTest().test_struct()
