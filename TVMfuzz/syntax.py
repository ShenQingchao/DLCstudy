from TVMfuzz.colors import *
import ast

def mainstring(self, string, surround, restname, prefix):
    string += prefix + '---restname---\n'
    string += prefix + str(restname) + '\n'
    string += prefix + '---surround---\n'
    if surround:
        string += surround.__str__(prefix + ' ') + '\n'
    string += prefix + '---Parents---\n'
    if self.parents:
        string += prefix
    for p in self.parents:
        if isinstance(p, pFunc):
            string += p.funcName + ' ' + str(self.parents[p]) + '\n'
        elif isinstance(p, pWith):
            string += 'with '
        else:
            if p.varobjects[0].Type == 'variable':
                string += p.varobjects[0].name + \
                    p.varobjects[0].restname + ' '
            elif p.varobjects[0].Type == 'subscript':
                string += p.varobjects[0].fullstr + ' '
    if self.parents:
        string += '\n'
    string += prefix + '---Children---\n'
    if self.children:
        string += prefix
    for c in self.children:
        if isinstance(c, pFunc):
            string += c.funcName + ' ' 
        elif isinstance(c, pWith):
            string += 'with '
        else:
            if c.varobjects[0].Type == 'variable':
                string += c.varobjects[0].name + \
                    c.varobjects[0].restname + ' '
            elif c.varobjects[0].Type == 'subscript':
                string += c.varobjects[0].fullstr + ' '
    if self.children:
        string += '\n'
    string += prefix + '---varobjects---\n'
    if self.varobjects:
        string += self.varobjects[0].__str__(prefix + ' ')
        string += '\n'
    return string

class Param:
    
    def __init__(self):

        self.Type = ''
        self.pref = '' # **params
        self.surround = None
        self.restname = ''
        self.parents = {} # a dict mapping param to the number of the param
        self.children = set() # a set of params
        self.varobjects = [] # list of param (variable)
        self.masters = set()
        self.shouldBeAdjunct = False
        self.indent = -1

    def add_master(self, master):
        if not isinstance(master, Param) and master != None:
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(master))))
        self.masters.add(master)
    
    def add_indent(self, indent):
        if not isinstance(indent, int):
            raise Exception(Cyan('Type error! Expect int but receive ' + str(type(indent))))
        
        self.indent = indent
    
    def update_masters(self, masters):
        if not isinstance(masters, set) and masters != None:
            raise Exception(Cyan('Type error! Expect set but receive ' + str(type(masters))))
        self.masters.update(masters)

    def add_surround(self, param):
        if not isinstance(param, Param) and param != None:
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(param))))
        self.surround = param 
    
    def add_restname(self, restname):
        if not isinstance(restname, str):
            raise Exception(Cyan('Type error! Expect str but receive ' + str(type(restname))))
        self.restname = restname
    
    def add_parent(self, ele):
        if not isinstance(ele, Param):
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(ele))))

        if ele not in self.parents:
            self.parents[ele] = 1
        else:
            self.parents[ele] += 1
    
    def get_parent_number(self, ele):
        
        if not isinstance(ele, Param):
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(ele))))
        
        if ele not in self.parents:
            raise Exception(Cyan('The parent pfunc\'s not in parents when asking for the needed number of it'))

        return self.parents[ele]

    def add_child(self, ele):
        if not isinstance(ele, Param):
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(ele))))
        
        self.children.add(ele)
    
    def add_varobject(self, varobject):
        if not isinstance(varobject, Param):
            raise Exception(Cyan('Type error! Expect list but receive ' + str(type(varobject))))
            
        self.varobjects.append(varobject)

    def add_varobjects(self, varobjects):
        if not isinstance(varobjects, list):
            raise Exception(Cyan('Type error! Expect list but receive ' + str(type(varobjects))))
        
        self.varobjects = varobjects

class pConst(Param):
    
    def __init__(self, const=None):
        
        super().__init__()
        self.Type = 'const'
        if not isinstance(const, str) and const != None:
            raise Exception(Cyan('Type error! Expect str but receive ' + str(type(const))))
        self.const = const
        self.consts = set()
        if const: self.consts.add(const)

    def add_const(self, const):
        if not isinstance(const, str):
            raise Exception(Cyan('Type error! Expect str but receive ' + str(type(const))))
        self.const = const
        self.consts.add(const)
    
    def add_consts_set(self, consts):
        if not isinstance(consts, set):
            raise Exception(Cyan('Type error! Expect set but receive ' + str(type(consts))))
        self.consts.update(consts)
    
    def add_consts_ele(self, const):
        if not isinstance(const, str):
            raise Exception(Cyan('Type error! Expect str but receive ' + str(type(const))))
        self.consts.add(const)
    
    def __str__(self, prefix=''):
        string = prefix + '===pConst===\n'
        string += prefix + '---const---\n'
        string += prefix + self.const + '\n'
        string += prefix + '---consts---\n'
        if self.consts:
            string += prefix
        for ele in self.consts:
            string += ele + ' '
        if self.consts:
            string += '\n'
        string = mainstring(self,
                            string, 
                            self.surround, 
                            self.restname,
                            prefix)
        return string

class pNumber(Param):

    def __init__(self, num=None):
        if num and not isinstance(num, int) \
            and not isinstance(num, float):

            raise Exception(Cyan('Passing parameter is not an int object, but ' + str(type(num))))
        
        super().__init__()
        self.Type = 'number'
        self.num = num

    def addNum(self, num):
        if not isinstance(num, int) and not isinstance(num, float):
            raise Exception(Cyan('Type error! Expect int or float but receive ' + str(type(num))))
        self.num = num 

    def __str__(self, prefix=''):
        string = prefix + '===pNumber===\n'
        string += prefix + '---num---\n'
        string += prefix + str(self.num) + '\n'
        string = mainstring(self,
                            string, 
                            self.surround, 
                            self.restname,
                            prefix)
        return string
    
class pVar(Param):
    
    def __init__(self, name=''):
        
        super().__init__()
        self.name = name
        self.varTofunc = set()
        self.varTocls = set()
        self.varTowith = set()
        self.Type = 'variable'
    
    def add_name(self, name):
        if not isinstance(name, str):
            raise Exception(Cyan('Type error! Expect str but receive ' + str(type(name))))
        self.name = name
    
    def update_varTocls_ele(self, ele):
        if not isinstance(ele, Param):
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(ele))))
        self.varTocls.add(ele)

    def update_varTofunc_set(self, se):
        if not isinstance(se, set):
            raise Exception(Cyan('Type error! Expect set but receive ' + str(type(se))))
        self.varTofunc.update(se)
    
    def update_varTofunc_ele(self, ele):
        if not isinstance(ele, Param):
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(ele))))
        self.varTofunc.add(ele)
    
    def update_varTowith_ele(self, ele):
        if not isinstance(ele, tuple):
            raise Exception(Cyan('Type error! Expect tuple but receive ' + str(type(ele))))
        
        self.varTowith.add(ele)
    
    def __str__(self, prefix=''):
        string = prefix + '===pVar===\n'
        string += prefix + '---name---\n'
        string += prefix + self.name + self.restname + '\n'
        string += prefix + '---varTofunc---\n'
        if self.varTofunc:
            string += prefix
            for ele in self.varTofunc:
                string += ele.funcName + ' '
            string += '\n'
        string += prefix + '---varTocls---\n'
        if self.varTocls:
            string += prefix
            for ele in self.varTocls:
                string += str(ele) + '\n'
            string += '\n'
        string = mainstring(self,
                            string, 
                            self.surround, 
                            self.restname,
                            prefix)
        return string

class pKeyword(Param):
    
    def __init__(self):
        super().__init__()
        self.keywordStr = '' 
        self.keywordContent = [] 
        self.Type = 'keyword'

    def add_keyWordStr(self, keywordStr):
        if not isinstance(keywordStr, str):
            raise Exception(Cyan('Type error! Expect str but receive ' + str(type(keywordStr))))
        self.keywordStr = keywordStr
    
    def add_keywordContent(self, ele):
        if not isinstance(ele, Param):
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(ele))))
        self.keywordContent.append(ele)

    def __str__(self, prefix=''):
        string = prefix + '===pKeyword===\n'
        string += prefix + '---keywordStr---\n'
        string += prefix + self.keywordStr + '\n'
        string += prefix + '---keywordContent---\n'
        for ele in self.keywordContent:
            string += ele.__str__(prefix + '  ') + '\n'
        string = mainstring(self,
                            string, 
                            self.surround, 
                            self.restname,
                            prefix)
        return string

class pList(Param):

    def __init__(self):
        super().__init__()
        self.content = [] # if not mutable, contains a list of Params
        self.mutable = False
        self.Type = 'list'
    
    def add_content(self, ele):
        if not isinstance(ele, Param):
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(ele))))
        self.content.append(ele)
    
    def __str__(self, prefix=''):
        string = prefix + '===pList===\n'
        string += prefix + '---content---\n'
        for ele in self.content:
            string += ele.__str__(prefix + '  ') + '\n'
        string += prefix + '---mutable---\n'
        string += prefix + str(self.mutable) + '\n'
        string = mainstring(self,
                            string, 
                            self.surround, 
                            self.restname,
                            prefix)
        return string

class pTuple(Param):

    def __init__(self):
        super().__init__()
        self.content = [] #a list of Params
        self.Type = 'tuple'
    
    def add_content(self, ele):
        if not isinstance(ele, Param):
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(ele))))
        self.content.append(ele)
    
    def __str__(self, prefix=''):
        string = prefix + '===pTuple===\n'
        string += prefix + '---content---\n'
        for ele in self.content:
            string += ele.__str__(prefix + '  ') + '\n'
        string = mainstring(self,
                            string, 
                            self.surround, 
                            self.restname,
                            prefix)
        return string

class pDict(Param):

    def __init__(self):
        super().__init__()
        self.keyContents = [] # a list of Params
        self.valueContents = [] # a list of Params
        self.Type = 'dict'
    
    def add_keyContents(self, ele):
        if not isinstance(ele, Param):
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(ele))))
        self.keyContents.append(ele)
    
    def add_valueContents(self, ele):
        if not isinstance(ele, Param):
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(ele))))
        self.valueContents.append(ele)
    
    def __str__(self, prefix=''):
        string = prefix + '===pDict===\n'
        string += prefix + '---keyContents---\n'
        for kc in self.keyContents:
            string += kc.__str__(prefix + '  ') + '\n'
        string += prefix + '---valueContents---\n'
        for vc in self.valueContents:
            string += vc.__str__(prefix + '  ') + '\n'
        string = mainstring(self,
                            string, 
                            self.surround, 
                            self.restname,
                            prefix)
        return string

class pNone(Param):

    def __init__(self):
        super().__init__()
        self.Type = 'none'
    
    def __str__(self, prefix=''):
        string = prefix + '===pNone===\n'
        return string

class pSet(Param):

    def __init__(self):
        super().__init__()
        self.content = []
        self.Type = 'set'
    
    def add_content(self, ele):
        if not isinstance(ele, Param):
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(ele)))) 
        self.content.append(ele)

    def __str__(self, prefix=''):
        string = prefix + '===pSet===\n'
        string += prefix + '---content---\n'
        for ele in self.content:
            string += ele.__str__(prefix + ' ') + '\n'
        string = mainstring(self,
                            string, 
                            self.surround, 
                            self.restname,
                            prefix)
        return string

class pSubs(Param):
    
    def __init__(self):

        super().__init__()
        self.content = []
        self.prefix = []
        self.Type = 'subscript'
        self.subsTosubs = None
        self.fullstr = ''
    
    def update_subsTosubs_ele(self, ele):
        if not isinstance(ele, Param):
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(ele))))
        self.subsTosubs = ele

    def add_fullstr(self, fullstr):
        if not isinstance(fullstr, str):
            raise Exception(Cyan('Type error! Expect str but receive ' + str(type(fullstr)))) 
            
        self.fullstr = fullstr

    def add_prefix(self, prefix):
        if not isinstance(prefix, pVar):
            raise Exception(Cyan('Type error! Expect pVar but receive ' + str(type(prefix)))) 
        self.prefix.append(prefix)
        
        if len(self.prefix) > 1:
            raise Exception(Cyan('self.prefix\'s lengh is larger than 1'))

    def add_content(self, ele):
        if not isinstance(ele, Param):
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(ele)))) 
        self.content.append(ele)

        if len(self.content) > 1:
            raise Exception(Cyan('self.content\'s lengh is larger than 1'))

    def __str__(self, prefix=''):
        string = prefix + '===pSubs===\n'
        string += prefix + '---fullstr---\n'
        string += prefix + self.fullstr + '\n'
        string += prefix + '---subsTosubs---\n'
        if self.subsTosubs:
            string += self.subsTosubs.__str__(prefix + ' ')
        string = mainstring(self,
                            string, 
                            self.surround, 
                            self.restname,
                            prefix)
        return string

class pComp(Param):

    def __init__(self):
        super().__init__()
        self.ops = []
        self.left = []
        self.right = []
        self.Type = 'compare'

    def add_op(self, op):
        if not isinstance(op, str):
            raise Exception(Cyan('Type error! Expect str but receive ' + str(type(op))))
        self.ops.append(op)

    def add_left(self, ele):
        if not isinstance(ele, Param):
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(ele))))
        self.left.append(ele)
    
    def add_right(self, ele):
        if not isinstance(ele, Param):
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(ele))))
        self.right.append(ele)
    
    def __str__(self, prefix=''):
        string = prefix + '===pComp===\n'
        string += prefix + '---left---\n'
        for kc in self.left:
            string += kc.__str__(prefix + '  ') + '\n'
        string += prefix + '---right---\n'
        for vc in self.right:
            string += vc.__str__(prefix + '  ') + '\n'
        string = mainstring(self,
                            string, 
                            self.surround, 
                            self.restname,
                            prefix)
        return string
 
class pBinop(Param):

    def __init__(self):
        super().__init__()
        self.left = [] # a param object
        self.right = [] # a param object
        self.op = ''
        self.Type = 'binop'
    
    def add_left(self, ele):
        self.left.append(ele)
    
    def add_right(self, ele):
        self.right.append(ele)

    def __str__(self, prefix=''):
        string = prefix + '===pBinop===\n'
        string += prefix + '---left---\n'
        for kc in self.left:
            string += kc.__str__(prefix + '  ') + '\n'
        string += prefix + '---right---\n'
        for vc in self.right:
            string += vc.__str__(prefix + '  ') + '\n'
        string = mainstring(self,
                            string, 
                            self.surround, 
                            self.restname,
                            prefix)
        return string

class pUop(Param):

    def __init__(self):
        super().__init__()
        self.operand = []  # a param object
        self.Type = 'uop'
        self.op = ''
    
    def add_operand(self, ele):
        if not isinstance(ele, Param):
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(ele))))
        self.operand.append(ele)
    
    def __str__(self, prefix=''):
        string = prefix + '===pUop===\n'
        string += prefix + '---operand---\n'
        for kc in self.operand:
            string += kc.__str__(prefix + '  ') + '\n'
        string = mainstring(self,
                            string,  
                            self.surround, 
                            self.restname,
                            prefix)
        return string

class pFunc(Param):

    def __init__(self, 
                 funcName='', 
                 Type='', 
                 params=None, 
                 suffix=None, 
                 indent = -1,
                 restricted=None,
                 surround=None):
        super().__init__()

        if not isinstance(funcName, str):
            raise Exception(Cyan('funcName Type Error! Expect str but receive ' + str(type(funcName))))

        self.funcName = funcName # string, generally representing the variable 
                                 # name on the left-side, or the function name
                                 # if no variable stays on the left-side

        self.funcNameSuffix = ''

        if Type != 'function' and \
           Type != 'onlyFunc' and \
           Type != 'restrictedFunction' and \
           Type != 'restrictedOnlyFunc' and \
           Type != 'closure' and \
           Type != 'onlyClosure' and \
           Type != '':
            raise Exception(Cyan('Incorrect pFunc Type: ' + Type))
        
        self.Type = Type  # function | onlyFunc | restrictedFunction | restrictedOnlyFunc
        self.params = params if params else []
        self.id = 0
        # restricted may be of pFunc or other Param Types
        self.restricted = restricted
        self.suffix = suffix
        self.indent = indent
        self.adjuncts = set()
        self.surround = surround

    def add_adjunct(self, adjunct):
        if not isinstance(adjunct, Param):
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(adjunct))))
            
        self.adjuncts.add(adjunct)

    def add_funcNameSuffix(self, funcNameSuffix):
        if not isinstance(funcNameSuffix, str):
            raise Exception(Cyan('Type error! Expect str but receive ' + str(type(funcNameSuffix))))
            
        self.funcNameSuffix = funcNameSuffix
    
    def add_suffix(self, suffix):
        if not isinstance(suffix, str):
            raise Exception(Cyan('Type error! Expect str but receive ' + str(type(suffix))))
    
        self.suffix = suffix
    
    def add_funcName(self, funcName):
        if not isinstance(funcName, str):
            raise Exception(Cyan('Type error! Expect str but receive ' + str(type(funcName))))
            
        self.funcName = funcName

    def add_param(self, param):
        if not isinstance(param, Param):
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(param))))
        self.params.append(param)
    
    def add_Type(self, Type):
        self.Type = Type
    
    def add_restricted(self, param):
        if not isinstance(param, Param) and param != None:
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(param))))
        self.restricted = param

    def __str__(self, prefix=''):
        string = prefix + '===pFunc===\n'
        string += prefix + '---funcName---\n'
        string += prefix + self.funcName + '\n'
        string += prefix + '---params---\n'
        for p in self.params:
            string += p.__str__(prefix + '  ') + '\n'
        string += '\n'
        string += prefix + '---id---\n'
        string += prefix + str(self.id) + '\n'
        string += prefix + '---suffix---\n'
        string += prefix + str(self.suffix) + '\n'
        string += prefix + '---adjuncts---\n'
        if self.adjuncts:
            string += prefix
            for ele in self.adjuncts:
                string += ele.__str__(prefix + ' ') + '\n'

        string = mainstring(self,
                            string, 
                            self.surround, 
                            self.restname,
                            prefix)
        return string

class pWith(Param):

    def __init__(self):
        super().__init__()
        self.Type = 'with'
        self.withitems = [] # a list of tuple consisting of context_expr and optional_vars
        self.body = []
        self.id = -1
    
    def set_id(self, id):
        if not isinstance(id, int):
            raise Exception(Cyan('Type error! Expect int but receive ' + str(type(id))))
        self.id = id

    def add_withitem(self, withitem):
        if not isinstance(withitem, tuple):
            raise Exception(Cyan('Type error! Expect tuple but receive ' + str(type(withitem))))
    
        self.withitems.append(withitem)
    
    def add_body(self, ele):
        if not isinstance(ele, Param):
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(ele))))
        self.body.append(ele)
    
    def __str__(self, prefix=''):
        string = prefix + '===pWith===\n'
        string += prefix + '---withitems---\n'
        for kc in self.withitems:
            string += kc[0].__str__(prefix + '  ') + '\n'
        string += '---body---\n'
        string = mainstring(self,
                            string, 
                            self.surround, 
                            self.restname,
                            prefix)
        return string

class pSlice(Param):

    def __init__(self):
        super().__init__()
        self.Type = 'slice'
        self.content = ':'
    
    def __str__(self, prefix=''):
        string = prefix + '===pSlice==='
        return string

class pLambda(Param):

    def __init__(self):
        super().__init__()
        self.Type = 'lambda'
        self.args = []
        self.body = []

    def add_arg(self, arg):
        if not isinstance(arg, Param):
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(arg))))
        self.args.append(arg)
    
    def add_body(self, body):
        if not isinstance(body, Param):
            raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(body))))
        self.body.append(body)

    def __str__(self, prefix=''):
        string = prefix + '===pLambda===\n'
        return string
    