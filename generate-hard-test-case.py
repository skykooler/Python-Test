
from random import randint, random, choice
import sys
m, n = map(int, sys.argv[1:])
with open('hard-test-case{0}x{1}.txt'.format(m, n), 'w') as test_file:
    test_file.write('%d\n' % m)
    test_file.write('%d\n' % n)
    matrix = '\n'.join([' '.join([choice(['0', '1']) for i in range(n)]) for i in range(m)])
    test_file.write(matrix)
