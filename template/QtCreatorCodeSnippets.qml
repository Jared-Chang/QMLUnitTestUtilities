import QtQuick 2.11
import QtTest 1.11

import "../"

Item {

    property $name$ testItem: testItemLoader.active ? testItemLoader.item : null
    Loader {
        id: testItemLoader

        sourceComponent: $name$ {
        }
    }

    SignalSpy {
        id: spy

        function init(target, signalName)
        {
            spy.signalName = "";
            spy.target = target;
            spy.signalName = signalName;
            spy.clear();
        }
    }

    TestCase {
        name: "$name$"

        function init()
        {
            testItemLoader.active = true;
        }

        function cleanup()
        {
            testItemLoader.active = false;
            spy.init(undefined, "");
        }
        
        function test_()
        {
            
        }
    }
}
