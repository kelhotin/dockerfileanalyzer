from dockerfile_parse import DockerfileParser

def parseFile(name) -> DockerfileParser:
    parser = DockerfileParser()
    try:
        parser.content = open(name).read()
    except:
        raise Exception("Cannot open the file")
    return parser
    # tree = parser.structure
    # cleanedTree = removeComments(tree)
    # return cleanedTree

def removeComments(tree):
    removed = []
    for node in tree:
        if node['instruction'] == 'COMMENT':
            continue
        else:
            removed.append(node)
    return removed

if __name__ == '__main__':
    print(parseFile('Dockerfile'))