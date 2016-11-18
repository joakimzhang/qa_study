# coding:utf8
import optparse
import sys
parser = optparse.OptionParser()
parser.add_option('-a', action="store_true", default=False, help="the a option")
parser.add_option('-b', action="store", dest="b", help="the b option")
parser.add_option('-c', action="store", dest="c", type="int", help="the c option")


parser2 = optparse.OptionParser()
parser2.add_option('-d', action="store", help="the option d")
parser2.add_option('-e', action="store", type="int", dest="e")

(option, args) = parser2.parse_args()

print option.e, "!!!!!!!!!!!"


