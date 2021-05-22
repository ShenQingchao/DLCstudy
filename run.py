import ast 
from TVMfuzz.elements import ingredient
import os
from TVMfuzz.colors import *
from TVMfuzz.elements import *
import random

# file_path = 'D:\\shared\\tvm\\tests\\python\\relay\\test_ir_bind.py'
# file_path = 'tests/testVariable.py'
if not os.path.exists('byproduct'):
    import platform
    osType = platform.system()
    if osType == 'Windows':
        os.system('mkdir byproduct')
    elif osType == 'Linux':
        os.system('mkdir byproduct')
        
record_path = 'byproduct/astTree.txt'

# dir = 'tests/' + ''.join(random.choices(['relay', 'relay-latest'], k=1)) + '/'
# dir = 'tests/topi/'
# dir = 'tests/relay-latest/'
# dir = 'tests/collection/'
# dir = 'tests/integration/'
# dir = 'tests/relay/'
dir = 'tests/'
print(Red('dir: '+ dir))
filelist = os.listdir(dir)
# filelist = os.listdir('mytests')

fileID = 0
os.environ['funcID'] = str(0)
os.environ['isFunc'] = str('False')

# with open('template.py', 'w') as f:
#     f.write('')

import random
random.shuffle(filelist)

for file in filelist:
    
    helperStatDef_global.clear()
    helperStatDef_local.clear()
    funcDefs.clear()

    fileID += 1
    os.environ['fileID'] = str(fileID)
    # print(Red('file: '+ file))
    from TVMfuzz.getAST import *

    # file_path = 'mytests/' + file
    file_path = dir + file

    with open(file_path, 'r') as source:
	    tree_node = ast.parse(source.read())

    with open(record_path, 'w') as astTree:
        astTree.write(ast.dump(tree_node, indent=2))

    NodeTransformer().visit(tree_node)
# NodeVisitor().visit(tree_node)

f = open('byproduct/log.txt', 'w')
for ing in ingredient:
    f.write('~~~~~~~~~~~~~~~~~~~~\n')
    f.write(str(ing) + '\n')

from TVMfuzz.generation import generate
generate()

# os.system('python byproduct/program.py')