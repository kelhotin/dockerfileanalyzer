import sys
sys.path.append('../')  
import docker_parser.docker_parser as parser

def testFileParsing():
    p = parser.parseFile('dockerfile.test')
    assert (p is not None)

def testCorrectImage():
    p = parser.parseFile('dockerfile.test')
    img = p.baseimage
    assert img == "node:14"

def testRemoveComment():
    p = parser.parseFile('dockerfile.test')
    tree = p.structure
    noComment = parser.removeComments(tree)
    mappedTo = list(map(lambda a: a['instruction'] == 'COMMENT', noComment))
    assert  any(mappedTo) is False
    