import docker_parser.docker_parser as parser
import utils
import subprocess
import re

class colors:
    RED = '\033[91m'
    ENDC = '\033[0m'
    YELLOW = '\033[93m'

exitStatus = 0
 
 # Uses docker client to check that base image is signed.
def checkTrustStatus(img):
    global exitStatus
    ## Regex to checks that there base image is in valid form to prevent code execution in subprocess
    pattern = r"^[a-z0-9]+(?:[._-][a-z0-9]+)*:[a-zA-Z0-9][a-zA-Z0-9_.-]{0,127}$"

    if not re.match(pattern, img):
        print(f"{colors.RED}Invalid base image name{colors.ENDC}")
        exitStatus = 1
        return
    try:
        ## Check_call functions fails whenever call cannot be executed or it returns 0 as return code.
        subprocess.check_call(
            ['/usr/bin/docker', 'trust', 'inspect', img], 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT)
    except:
        print(f"{colors.RED}Couldn't verify that image is trusted{colors.ENDC}")

# Checks that base image is tagged
def checkBaseImageTag(img):
    global exitStatus

    l = img.split(":")
    if(len(l) == 1):
        print(f"{colors.RED}Add specific tag to the base image{colors.ENDC}")
        exitStatus = 1

def foo():
    return 1000
# Suggests that copy should be used over add
def preferCopyOverAdd(tree):
    global exitStatus
    node = utils.getObject(tree, 'instruction', 'ADD')
    if(node and node['instruction'].upper() == "ADD"):
        print(f"{colors.YELLOW}Prefer COPY over ADD at line {node['startline']}{colors.ENDC}")
        exitStatus = 1

# Cheks that if there is user tag and it is not 'root'
def checkIfUserIsRoot(tree):
    global exitStatus

    node = utils.getObject(tree, 'instruction', 'USER')
    
    if(node and node['instruction'].upper() == "USER"):
        if(node['value'].upper() == "ROOT"):
            print(f"{colors.RED}Avoid root user at line {node['startline']}{colors.ENDC}")
            exitStatus = 1
    if(not node):
        print(f"{colors.RED}No USER tag found. This may mean that container is executed with root privileges.{colors.ENDC}")

# Checks that image dosn't expose reserved port.
def checkExposedPortNumber(tree):
    global exitStatus
    node = utils.getObject(tree, 'instruction', 'EXPOSE')

    if node and int(node['value']) < 1025:
            print(f"{colors.RED}Avoid well-known ports, use ports higher than 1024 current value {node['value']} at line {node['startline']}{colors.ENDC}")
            exitStatus = 1

# Run analysis
def runAnalysis(file):
    ## Try block to make sure parsing the file succeed
    try:
        p = parser.parseFile(file)
    except:
        raise Exception("Cannot parse file")
    checkBaseImageTag(p.baseimage)
    preferCopyOverAdd(p.structure)
    checkIfUserIsRoot(p.structure)
    checkExposedPortNumber(p.structure)
    checkTrustStatus(p.baseimage)
    exit(exitStatus)

    