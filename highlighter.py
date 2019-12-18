import ctypes
import sys

if __name__ == "__main__":

    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    is_fail = False

    for line in sys.stdin:
        firstToken = line.split()[0]

        if firstToken == 'PASS':
            is_fail = False

        elif firstToken == 'QWARN':
            is_fail = False
            print('\033[93m' + line.rstrip() + '\033[0m')

        elif firstToken == 'QDEBUG':
            is_fail = False
            print('\033[96m' + line.rstrip() + '\033[0m')

        elif firstToken == 'FAIL!':
            is_fail = True
            print('\033[1;31m' + line.rstrip() + '\033[0m')

        elif is_fail:
            print('\033[33m' + line.rstrip() + '\033[0m')

        else:
            print('\033[1m' + line.rstrip() + '\033[0m')