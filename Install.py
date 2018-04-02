import os
import _winreg
import re
import argparse
import shutil
import distutils.dir_util

QT_CREATOR_SETTING_EXTERNAL_TOOLS = "[ExternalTools]"
QT_CREATOR_SETTING_KEYBOARD_SHOURTCUTS = "[KeyboardShortcuts]"

TESTRUNNER_EXTERNAL_TOOLS = "OverrideCategories\\testrunnerx\\size=1\nOverrideCategories\\testrunnerx\\1\\Tool=qmltestrunnerx"
TESTRUNNER_SHORTCUT = "Tools.External.qmltestrunnerx=Ctrl+`"

def backup_qt_setting_file():

    qt_creator_setting_file_path = os.getenv("APPDATA") + "\\QtProject\\QtCreator.ini"
    shutil.copy2(qt_creator_setting_file_path, qt_creator_setting_file_path + ".bk")


def modify_qt_creator_settings_file():
    
    global QT_CREATOR_SETTING_EXTERNAL_TOOLS
    global QT_CREATOR_SETTING_KEYBOARD_SHOURTCUTS
    global TESTRUNNER_EXTERNAL_TOOLS
    global TESTRUNNER_SHORTCUT

    qt_creator_setting_file_path = os.getenv("APPDATA") + "\\QtProject\\QtCreator.ini"
    setting_file = open(qt_creator_setting_file_path, "r")
    settings = setting_file.read()
    setting_file.close()

    external_tools_index = settings.find(QT_CREATOR_SETTING_EXTERNAL_TOOLS)
    if external_tools_index != -1:
        settings = settings[:external_tools_index + len(QT_CREATOR_SETTING_EXTERNAL_TOOLS)] + "\n" + TESTRUNNER_EXTERNAL_TOOLS + settings[external_tools_index + len(QT_CREATOR_SETTING_EXTERNAL_TOOLS):]
    else:
        settings += "\n" + QT_CREATOR_SETTING_EXTERNAL_TOOLS + "\n" + TESTRUNNER_EXTERNAL_TOOLS

    keyboard_shortcuts_index = settings.find(QT_CREATOR_SETTING_KEYBOARD_SHOURTCUTS)
    if keyboard_shortcuts_index != -1:
        settings = settings[:keyboard_shortcuts_index + len(QT_CREATOR_SETTING_KEYBOARD_SHOURTCUTS)] + "\n" + TESTRUNNER_SHORTCUT + settings[keyboard_shortcuts_index + len(QT_CREATOR_SETTING_KEYBOARD_SHOURTCUTS):]
    else:
        settings += "\n" + QT_CREATOR_SETTING_KEYBOARD_SHOURTCUTS + "\n" + TESTRUNNER_SHORTCUT

    setting_file = open(qt_creator_setting_file_path, "w")
    setting_file.write(settings)
    setting_file.close()


def modify_external_setting_file(qml_import_test_path):
    
    qt_creator_setting_path = os.getenv("APPDATA") + "\\QtProject\\qtcreator\\externaltools"

    f = open(qt_creator_setting_path + "\\qmltestrunnerx.xml", "r")
    content = f.read()
    f.close()

    f = open(qt_creator_setting_path + "\\qmltestrunnerx.xml", "w")
    f.write(re.sub("@test@", qml_import_test_path, content))
    f.close()


def modify_testrunner_script(qt_path):
    
    bin_path = qt_path + "\\bin"
    vast_registy = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\WOW6432Node\VIVOTEK, Inc.\VAST")
    install_path = _winreg.QueryValueEx(vast_registy, "INSTALL_PATH")[0] + "\\Client\\Vast2"

    f = open(bin_path + "\\qmltestrunnerX.bat", "r")
    content = f.read()
    f.close()

    f = open(bin_path + "\\qmltestrunnerX.bat", "w")
    f.write(re.sub("@vast2@", install_path, content))
    f.close()


def copy_file_to_qt_path(qt_path):

    bin_path = qt_path + "\\bin"

    shutil.copy2(".\\highlighter.py", bin_path)
    shutil.copy2(".\\qmltestrunnerX.bat", bin_path)
    distutils.dir_util.copy_tree(".\\ansiconx64", bin_path + "\\ansiconx64")


def copy_file_to_qt_creator():

    qt_creator_setting_path = os.getenv("APPDATA") + "\\QtProject\\qtcreator\\externaltools"

    if not os.path.exists(qt_creator_setting_path):
        os.makedirs(qt_creator_setting_path)
    
    shutil.copy2(".\\qmltestrunnerx.xml", qt_creator_setting_path)


def install(qml_import_test_path, qt_path):

    backup_qt_setting_file()
    modify_qt_creator_settings_file()
    copy_file_to_qt_path(qt_path)
    modify_testrunner_script(qt_path)
    copy_file_to_qt_creator()
    modify_external_setting_file(qml_import_test_path)


def main():
    parser = argparse.ArgumentParser(description='Install QtCreator QmlTestrunnerUtililty')
    
    parser.add_argument('qml_import_test_path', help='QML/VAST2/Test')
    parser.add_argument('qt_path', help='qt/msvc2013')
    
    args = parser.parse_args()
    install(args.qml_import_test_path, args.qt_path)

if __name__ == "__main__":
    main()
