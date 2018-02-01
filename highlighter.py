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
        current_dir = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))
        subprocess.call([current_dir + "/ansiconx64/ansicon.exe", "-i"])
        
    elif (is_win10):
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    is_fail = False
    fail_list = []
    warning_list = []

    for line in sys.stdin:
        firstToken = line.split()[0]

        if firstToken == 'PASS':
            is_fail = False
            print '\033[0;32m' + line.rstrip() + '\033[0m'

        elif firstToken == 'QWARN':
            is_fail = False
            warning_list.append(line)
            
        elif firstToken == 'Totals:':
            is_fail = False

            for warning in warning_list:                
                print '\033[93m' + warning.rstrip() + '\033[0m'

            for fail in fail_list:
                print '\033[1;31m' + fail.rstrip() + '\033[0m'

            print '\033[1m' + line.rstrip() + '\033[0m'

        elif firstToken == 'FAIL!' or is_fail:
            is_fail = True
            fail_list.append(line)

        else:
            print '\033[1m' + line.rstrip() + '\033[0m'