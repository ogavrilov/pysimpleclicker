import unittest
import os
import subprocess

class SimpleWidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.testFileName = 'tests/testtext.txt'
        self.testInitialValue = '---'
        self.testCorrectResultValue = '111'
        with open(self.testFileName, 'w') as testFile:
            testFile.write(self.testInitialValue)
    
    def tearDown(self):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), self.testFileName)
        os.remove(path)

    def executeWinCommand(self, cmd):
        resultText = ''
        print(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        if out != None:
            out_ = out.decode('utf-8')
            result = out_.split('\n')
            for lin in result:
                if not lin.startswith('#'):
                    resultText += '\n' + lin
        if err != None:
            err_ = err.decode('utf-8')
            result = err_.split('\n')
            for lin in result:
                if not lin.startswith('#'):
                    resultText += '\n' + lin
        return p, resultText

    def test_basefunctions(self):
        # test operations
        explorer, resultText = self.executeWinCommand('explorer ' + os.path.abspath(os.path.dirname(__file__)) + '\\tests')
        print(resultText)
        script, resultText = self.executeWinCommand('python pysimpleclicker.py')
        print(resultText)
        script.terminate()
        explorer.terminate()
        # result check
        testResultValue = ''
        with open(self.testFileName, 'r') as testFile:
            testResultValue = testFile.read()
        self.assertEqual(testResultValue, self.testCorrectResultValue)

if __name__ == '__main__':
    unittest.main()