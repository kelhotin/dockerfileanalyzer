# import docker
# import requests
import docker_parser.docker_parser as parser
import utils
import subprocess
import sys

# # Create a Docker client object
# client = docker.from_env()

# # Get a list of all Docker images
# images = client.images.list()

# # Sort the images by creation time in descending order
# sorted_images = sorted(images, key=lambda image: image.attrs['Created'], reverse=True)

# Print the IDs of the 10 most recently created images
# for image in sorted_images[:1]:
#     print(image.id)

# repositoryName = "node"
# # https://hub.docker.com/v2/repositories/library/node/tags?page_size=1000
# api_url = f'https://hub.docker.com/v2/repositories/library/{repositoryName}/tags/?page_size=100'

# response = requests.get(api_url)

# tags = response.json()['results']
# tag_names = [tag['name'] for tag in tags]
# creation_dates = [tag['last_updated'] for tag in tags]

# for tag, date in zip(tag_names, creation_dates):
#     print(f'{tag} ({date})')

exitStatus = 0

def checkTrustStatus(img):
    global exitStatus
    print(img)
    result = subprocess.run(['docker', 'trust', 'inspect', img], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    if (result.returncode == 1):
        exitStatus = 1
        print("Couldn't verify that image is trusted")


def checkBaseImageTag(img):
    global exitStatus

    l = img.split(":")
    if(len(l) == 1):
        print("Add specific tag to the base image")
        exitStatus = 1

def preferCopyOverAdd(tree):
    global exitStatus
    node = utils.getObject(tree, 'instruction', 'ADD')
    if(node and node['instruction'].upper() == "ADD"):
        print(f"Prefer COPY over ADD at line {node['startline']}")
        exitStatus = 1

def checkIfUserIsRoot(tree):
    global exitStatus

    node = utils.getObject(tree, 'instruction', 'USER')
    
    if(node and node['instruction'].upper() == "USER"):
        if(node['value'].upper() == "ROOT"):
            print(f"Avoid root user at line {node['startline']}")
            exitStatus = 1
    if(not node):
        print("No USER tag found. This may mean that container is executed with root privileges.")

def checkExposedPortNumber(tree):
    global exitStatus
    node = utils.getObject(tree, 'instruction', 'EXPOSE')

    if node and int(node['value']) < 1025:
            print(f"Avoid well-known ports, use ports higher than 1024 current value {node['value']} at line {node['startline']}")
            exitStatus = 1

if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print("Give dockerfile as argument")
        exit(1)
    f = sys.argv[1]
    try:
        p = parser.parseFile(f)
    except:
        raise Exception("Cannot parse file")
    checkBaseImageTag(p.baseimage)
    preferCopyOverAdd(p.structure)
    checkIfUserIsRoot(p.structure)
    checkExposedPortNumber(p.structure)
    checkTrustStatus(p.baseimage)
    exit(exitStatus)