
from random import random, choice
import sys
m, n = map(int, sys.argv[1:])
with open('hard-test-case{0}x{1}.txt'.format(m, n), 'w') as test_file:
    test_file.write('{0}\n{1}\n'.format(m, n))
    matrix = '\n'.join([' '.join([choice('01') for i in range(n)]) for i in range(m)])
    test_file.write(matrix)
