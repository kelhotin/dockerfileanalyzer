import sys
sys.path.append('../')  
import analyzer
import docker_parser.docker_parser as parser

def testIfRoot():
    p = parser.parseFile('dockerfile.test')
    analyzer.checkIfUserIsRoot(p.structure)
    s = analyzer.exitStatus
    assert s == 1
