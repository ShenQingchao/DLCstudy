import ast 
from TVMfuzz.elements import ingredient
import os
from TVMfuzz.colors import *
from TVMfuzz.elements import *
import random

if not os.path.exists('byproduct'):
    import platform
    osType = platform.system()
    if osType == 'Windows':
        os.makedirs('byproduct')

    elif osType == 'Linux':
        os.makedirs('byproduct')
        
record_path = 'byproduct/astTree.txt'

dir = 'tests/'
print(Red('dir: '+ dir))
filelist = os.listdir(dir)
fileID = 0
os.environ['funcID'] = str(0)
os.environ['isFunc'] = str('False')

import random
random.shuffle(filelist)

for file in filelist:
    
    helperStatDef_global.clear()
    helperStatDef_local.clear()
    funcDefs.clear()

    fileID += 1
    os.environ['fileID'] = str(fileID)
    from TVMfuzz.getAST import *

    file_path = dir + file

    with open(file_path, 'r') as source:
	    tree_node = ast.parse(source.read())

    with open(record_path, 'w') as astTree:
        astTree.write(ast.dump(tree_node, indent=2))

    NodeTransformer().visit(tree_node)

f = open('byproduct/log.txt', 'w')
for ing in ingredient:
    f.write('~~~~~~~~~~~~~~~~~~~~\n')
    f.write(str(ing) + '\n')

from TVMfuzz.generation import generate
generate()
