import sys
import os
import inspect
import ctypes
import platform
import subprocess

if __name__ == "__main__":

    winVersion = platform.platform()

    is_win7 = not winVersion.find("Windows-7") == -1
    is_win10 = not winVersion.find("Windows-10") == -1

    if (is_win7):
        current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        subprocess.call([current_dir + "/ansiconx64/ansicon.exe", "-i"])
        
    elif (is_win10):
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
            

    if (is_win7):
        current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        subprocess.call([current_dir + "/ansiconx64/ansicon.exe", "-u"])