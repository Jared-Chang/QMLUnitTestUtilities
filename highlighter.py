import sys
import ctypes

if __name__ == "__main__":

    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    for line in sys.stdin:

        firstToken = line.split()[0]

        if firstToken == 'PASS':
            print '\033[0;32m' + line.rstrip() + '\033[0m'

        elif firstToken == 'FAIL!':
            print '\033[1;31m' + line.rstrip() + '\033[0m'

        elif firstToken == 'QWARN':
            print '\033[93m' + line.rstrip() + '\033[0m'

        else:
            print line.rstrip()