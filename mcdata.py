from collections import Counter
import json

directory = 'data/pc/'

# Diamond block/ore, emerald block/ore, gold block/ore, lapis block/ore, iron block/ore, beacon
unrealistic = [56, 57, 129, 133, 14, 41, 21, 22, 173, 138, 15, 42]

def blocks(version):
    with open(directory + str(version)) as json_file:
        data = json.load(json_file)
        return data

def blockFromID(id):
    return blocks('1.8')[id]

def findBlocks(array):
    materials = Counter(array)
    return materials

def isRealistic(id):
    if int(id) in unrealistic:
        return False
    return True

def isUnrealistic(id):
    if int(id) in unrealistic:
        return True
    return False