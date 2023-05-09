"""
Input array of maps
"""
def getObject(arr, key, value):
    for i in arr:
        if(i[key] == value):
            return i
    return None