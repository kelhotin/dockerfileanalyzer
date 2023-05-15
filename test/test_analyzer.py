import sys
sys.path.append('../')  
import  analyzer.analyzer as analyzer 
import docker_parser.docker_parser as parser
import pytest

def testIfRoot():
    analyzer.exitStatus = 0
    p = parser.parseFile('dockerfile.test')
    print(analyzer.foo())
    analyzer.checkIfUserIsRoot(p.structure)
    s = analyzer.exitStatus
    assert s == 1

def testExposedPort():
    analyzer.exitStatus = 0
    p = parser.parseFile('dockerfile.test')
    analyzer.checkExposedPortNumber(p.structure)
    s = analyzer.exitStatus
    assert s == 1

def testCopyOverAdd():
    analyzer.exitStatus = 0
    p = parser.parseFile('dockerfile.test')
    analyzer.preferCopyOverAdd(p.structure)
    s = analyzer.exitStatus
    assert s == 1

def testTruststatusInvalidname():
    analyzer.exitStatus = 0
    analyzer.checkTrustStatus("invalid:name;@1")
    s = analyzer.exitStatus
    assert s == 1


def testTruststatusValidName():
    analyzer.exitStatus = 0
    analyzer.checkTrustStatus("node:15")
    s = analyzer.exitStatus
    assert s == 0


def testTruststatusUntrusted():
    analyzer.exitStatus = 0
    analyzer.checkTrustStatus("thisIsMalicious:asd123")
    s = analyzer.exitStatus
    assert s == 1

def testAnalyseValid():
    analyzer.exitStatus = 0
    with pytest.raises(SystemExit) as e:
        analyzer.runAnalysis("dockerfile.test-valid")
    assert e.type == SystemExit
    assert e.value.code == 0


def testAnalyseInvalid():
    analyzer.exitStatus = 0
    with pytest.raises(SystemExit) as e:
        analyzer.runAnalysis("dockerfile.test")
    assert e.type == SystemExit
    assert e.value.code == 1

