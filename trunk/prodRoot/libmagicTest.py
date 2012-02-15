print 'first'
import magic
print 'after import'
m = magic.Magic()
print m
print m.from_file("D:\\sys\\android-sd-2011-09-29\\51\\51friend\\HeadImg\\ying422176328_80_20110615205901")
print '------------------------'
print m.from_buffer(open("D:\\sys\\android-sd-2011-09-29\\51\\51friend\\HeadImg\\ying422176328_80_20110615205901").read(1024))
print '------------------------'