import random
from TVMfuzz.colors import *
from TVMfuzz.syntax import *
from TVMfuzz.utils import varNameGenerator
from TVMfuzz.elements import *
import astunparse

random.seed()

def integerGenerator(a, b):
    return random.randint(a, b)

def floatGenerator(str_):

    if 'e' in str_:
        return '1e-' + str(integerGenerator(1, 7))
    else:
        lt = str_.split('.')
        integer = lt[0]
        floats = lt[1]
        integer = integerGenerator(0, int(integer))
        floats = integerGenerator(0, int(floats))
        return str(integer) + '.' + str(floats)

def listGenerator():
    n = integerGenerator(1, 5)
    m = integerGenerator(1, 5)
    string = '['
    for i in range(n):
        string += '['
        for i in range(m):
            string += str(integerGenerator(1, 10)) + ','
        string = string[:-1]
        string += '],'
    string = string[:-1]
    string += ']'
    return string

def tupleGenerator():
    n = integerGenerator(1, 5)
    m = integerGenerator(1, 5)
    string = '('
    for i in range(n):
        string += '('
        for i in range(m):
            string += str(integerGenerator(1, 10)) + ','
        string = string[:-1]
        string += '),'
    string = string[:-1]
    string += ')'
    return string

def constGenerator():
    space = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    name = ''.join(random.choices(space, k=1))
    space += ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    name += ''.join(random.choices(space, k=random.randint(0, 4)))
    return name

def decryptConst(param, string, PARAM):
    
    if len(param.consts) == 0:
        output = param.const
    else: 
        id = random.randint(0, len(param.consts)-1)
        output = list(param.consts)[id]
    if output == 'float16' or output == 'float32' or \
        output == 'float64' or output == 'int16' or \
            output == 'int32' or output == 'int64' or \
                output == 'uint16' or output == 'uint32' or \
                    output == 'uint64':
        output = random.choices(['float', 'int', 'uint'], k=1)[0] + \
            random.choices(['16', '32', '64'], k=1)[0]

    elif 'llvm' == output or 'cuda' == output:
        output = 'llvm'
    elif 'cpu' == output or 'gpu' == output:
        output = 'cpu'
    string += param.pref + '\'\'\'' + output + '\'\'\'' + param.restname + ','
    
    return string

def decryptListTuple(param, string, PARAM, f, noBracket, rv):

    begin = ''
    end = ''
    if param.Type == 'list':
        begin = '['
        end = ']'
    else:
        if not noBracket:
            begin = '('
            end = ')'
    string += param.pref + begin
    if param.Type == 'tuple' \
        or param.Type == 'list' or \
        not param.mutable:
        
        for c in param.content:
            string = decrypt(c, PARAM, f, string=string, rv=rv) + ','
        
    else:
        string += listGenerator()
    string += end + param.restname + ','
    return string

def decryptDict(param, string, PARAM, f, rv):

    string += param.pref + '{'
    for key, value in zip(param.keyContents, param.valueContents):
        string = decrypt(key, PARAM, f, string=string, rv=rv)
        string += ':'
        string = decrypt(value, PARAM, f, string=string, rv=rv) + ','
    if param.keyContents:
        string = string[:-1]
    string += '}' + param.restname + ','
    return string

def decryptComp(param, string, PARAM, f, rv):
    string += param.pref + '('
    string = decrypt(param.left[0], PARAM, f, string=string, rv=rv)

    for i in range(len(param.right)):
        string += param.ops[i]
        string = decrypt(param.right[i], PARAM, f, string=string, rv=rv)
    string += ')' + param.restname + ','
    return string

def decryptBinop(param, string, PARAM, f, rv):
    string += param.pref + '('
    string = decrypt(param.left[0], PARAM, f, string=string, rv=rv)
    string += param.op
    string = decrypt(param.right[0], PARAM, f, string=string, rv=rv)
    string += ')'
    string += param.restname
    string += ','
    return string

def decryptUop(param, string, PARAM, f, rv):
    string += param.pref + '('
    string += param.op
    string = decrypt(param.operand[0], PARAM, f, string=string, rv=rv)
    string += ')'
    string += param.restname
    string += ','
    return string

def decryptVariable_if_varTocls(pvar, f, string, PARAM, rv):

    randit_ = random.randint(0, len(pvar.varTocls)-1)
    parentParam = list(pvar.varTocls)[randit_]
    
    for master in parentParam.masters:
        if master not in lazy and master not in funcPool:
            if rv and master.surround == PARAM.surround:
                string = generateFunc(master, f, False, True) + string
            else:
                generateFunc(master, f, False)
        else:
            if isinstance(parentParam.varobjects[0], pVar) and \
                parentParam not in clsPool:
                if rv and parentParam.surround == PARAM.surround:
                    string = generateAdjuncts(parentParam, f, master, True) + string
                else:
                    generateAdjuncts(parentParam, f, master)
            
            elif isinstance(parentParam.varobjects[0], pSubs) and \
                parentParam not in subsPool:
                if rv and parentParam.surround == PARAM.surround:
                    string = generateAdjuncts(parentParam, f, master, True) + string
                else:
                    generateAdjuncts(parentParam, f, master)
            
    
    '''
        a = fun()
        a[0] = 1
        b = a[0]
        b.c = 2
        fun3(b.c)

        which is 

        a = fun()
        a[0].c = 2
        fun3(a[0].c)
    The parent of "a[0].c" (in fun3(a[0].c)) is "a[0].c = 2", a subs
    '''
    if parentParam not in clsPool and parentParam not in subsPool:

        if isinstance(parentParam.varobjects[0], pVar):
            raise Exception(Cyan('parentParam, whose varobject\'s name is ' + \
                parentParam.varobjects[0].name + parentParam.varobjects[0].restname+\
                ' not in clsPool'))
        else:
            raise Exception(Cyan('parentParam, whose varobject\'s name is ' + \
                parentParam.varobjects[0].fullstr + parentParam.varobjects[0].restname+\
                ' not in clsPool'))

    if isinstance(parentParam.varobjects[0], pVar):

        lt = clsPool[parentParam]
        rn = lt[random.randint(0, len(lt)-1)]
        name = rn + pvar.restname
        string += pvar.pref + name + ','
        return string
    
    elif isinstance(parentParam.varobjects[0], pSubs):

        lt = subsPool[parentParam]
        rn = lt[random.randint(0, len(lt)-1)]
        name = rn + pvar.restname
        string += name + ','
        return string

def decryptVariable_if_varTofunc(PARAM, pvar, f, string, rv):
    
    leftname = None
    pfunc_ = None
    if isinstance(PARAM, pFunc):
        while True:
            randit_ = random.randint(0, len(pvar.varTofunc)-1)
            pfunc_ = list(pvar.varTofunc)[randit_]
            if pfunc_ != PARAM and \
                (PARAM not in pfunc_.parents or \
                    not random.randint(0, 10)):
                break

        if pfunc_ == None:
            raise Exception(Cyan('pfunc_ is none'))
        
        if pfunc_ not in lazy and pfunc_ not in funcPool:
            if rv and pfunc_.surround == PARAM.surround:
                string = generateFunc(pfunc_, f, False, True) + string
            else:
                generateFunc(pfunc_, f, False)

        if pfunc_ not in funcPool:

            raise Exception(Cyan(pfunc_.funcName + \
                    ' not in funcPool!' + \
                    ' And the pvar is ' + pvar.name + \
                        ' while the pfunc is ' + PARAM.funcName))
    else:
        randit_ = random.randint(0, len(pvar.varTofunc)-1)
        pfunc_ = list(pvar.varTofunc)[randit_]
        if pfunc_ not in lazy and pfunc_ not in funcPool:
            generateFunc(pfunc_, f, False)
        OTfunc = PARAM
        if pfunc_ not in funcPool:
            raise Exception(Cyan(pfunc_.funcName + \
                    ' not in funcPool!' + \
                    ' And the pvar is ' + pvar.name + \
                        ' while the OTparam type is ' + OTfunc.Type))

    lt = funcPool[pfunc_]

    length = len(lt)
    leftname = lt[random.randint(0, length-1)]
    string += pvar.pref + leftname + pvar.restname + ','
    return string

def decryptVariable(pvar, string, PARAM, f, rv):

    if pvar.varTofunc:
        return decryptVariable_if_varTofunc(PARAM, pvar, f, string, rv)
    
    elif pvar.varTocls:
        return decryptVariable_if_varTocls(pvar, f, string, PARAM, rv)

    else:
        
        if pvar.name in helperFuncDef:
            f.write(astunparse.unparse(helperFuncDef[pvar.name]))
        return string + pvar.pref + pvar.name + pvar.restname + ','
    
def decryptNumber(param, string):
    
    if random.randint(0, 1):

        string += param.pref + str(param.num) + param.restname + ','

    else:
        if isinstance(param.num, int):
            string += param.pref + str(integerGenerator(0, param.num)) + param.restname + ','

        elif isinstance(param.num, float):
            string += param.pref + str(floatGenerator(str(param.num))) + param.restname + ','
            
    return string

def decryptSubs(param, string, PARAM, f, rv):

    if param.subsTosubs:
        find = False
        for master in param.subsTosubs.masters:
            if master not in lazy and master not in funcPool:
                find = True 
                if rv and PARAM.surround == param.surround:
                    string = generateFunc(master, f, False, True) + string
                else:
                    generateFunc(master, f, False)
        if not find:
            if rv:
                string = generateSubs(param.subsTosubs, f, rv) + string
            else:
                generateSubs(param.subsTosubs, f)
        
        if param.subsTosubs not in subsPool:
            raise Exception(Cyan('param.subsTosubs: ' + str(param.subsTosubs)\
                + ' not in subsPool') + Green('param: ' + str(param)) + Blue('PARAM: ' + str(PARAM)))

        lt = subsPool[param.subsTosubs]
        string += param.pref + lt[random.randint(0, len(lt)-1)] + ','

    else:

        string += param.pref
        string = decrypt(param.prefix[0], PARAM, f, string=string, rv=rv)
        string += '['
        string = decrypt(param.content[0], PARAM, f, noBracket=True, string=string, rv=rv)
        if string[-1] == ',': string = string[:-1]
        string += ']' + param.restname + ','

    return string

def decryptSet(param, string, PARAM, f, rv):
    string += param.pref + '{'
    for ele in param.content:
        string = decrypt(ele, PARAM, f, string=string, rv=rv)
        string += ','
    
    if param.content:
        string = string[:-1]
    string += '}' + param.restname + ','
    return string

def decryptLambda(param, string, PARAM, f, rv):
    string += param.pref + 'lambda '
    for arg in param.args:
        string += arg.name + ','
    string = string[:-1] + ': '
    if not isinstance(param.body[0], pFunc):
        string = decrypt(param.body[0], PARAM, f, string=string, rv=rv)
    else:
        string += generateFunc(param.body[0], f, False, rv=rv, lamb=True)
    if string[-1] == '\n': string = string[:-1]
    return string + ','

def decrypt(param, PARAM, f, noBracket=False, rv=False, string=''):

    if param.Type == 'const':
        string = decryptConst(param, string, PARAM)
    
    elif param.Type == 'number':
        string = decryptNumber(param, string)
    
    elif param.Type == 'variable':
        string = decryptVariable(param, string, PARAM, f, rv)
    
    elif param.Type == 'keyword':
        string += param.keywordStr + '='
        randid = random.randint(0, len(param.keywordContent)-1)
        string = decrypt(param.keywordContent[randid], PARAM, f, string=string, rv=rv) + ','
    
    elif param.Type == 'list' or param.Type == 'tuple':
        string = decryptListTuple(param, string, PARAM, f, noBracket, rv)
    
    elif param.Type == 'dict':
        string = decryptDict(param, string, PARAM, f, rv)
    
    elif param.Type == 'binop':
        string = decryptBinop(param, string, PARAM, f, rv)
    
    elif param.Type == 'uop':
        string = decryptUop(param, string, PARAM, f, rv)

    elif param.Type == 'subscript':
        string = decryptSubs(param, string, PARAM, f, rv)

    elif param.Type == 'set':
        string = decryptSet(param, string, PARAM, f, rv)

    elif param.Type == 'none':
        string += 'None,'
    
    elif param.Type == 'compare':
        string = decryptComp(param, string, PARAM, f, rv)

    elif param.Type == 'slice':
        string += ':,'

    elif param.Type == 'lambda':
        string = decryptLambda(param, string, PARAM, f, rv)

    return string[:-1]

def generateIndent(indent):
    string = ''
    for _ in range(indent):
        string += '\t'
    return string

def generateFuncLeftPart_varTonothing(varobject, string):
    name = varNameGenerator(varPool)
    leftname = ''
    if not varobject.restname:
        leftname = name
        string += name + ','
    else:
        if varobject.varTofunc:
            randit_ = random.randint(0, len(varobject.varTofunc)-1)
            param_ = list(varobject.varTofunc)[randit_]
            leftnamesTuple = funcPool[param_]

            leftname = leftnamesTuple[\
                random.randint(0, len(leftnamesTuple)-1)]

            string += leftname + varobject.restname + ','

        else:
            leftname = name + varobject.restname
            string += name + varobject.restname + ','
    return string, leftname

def generateFuncLeftPart_varTocls(varobject, string, f, pfunc, rv):
    
    parentParams = list(varobject.varTocls)
    randit_ = random.randint(0, len(parentParams)-1)
    parentParam = parentParams[randit_]

    for master in parentParam.master:
        if master not in lazy and master not in funcPool:
            if rv and master.surround == pfunc.surround:
                string = generateFunc(master, f, False, True) + string
            else:
                generateFunc(master, f, False)

    if parentParam not in clsPool:
        raise Exception(Cyan('Not find ' + parentParam.name + \
            parentParam.restname + ' in clsPool'))

    lt = clsPool[parentParam]
    rn = lt[random.randint(0, len(lt)-1)]
    name = rn + varobject.restname
    leftname = name
    string += leftname + ','
    return string, leftname

def generateFuncLeftPart_varTofunc(varobject, string, f, pfunc, rv):

    funcList = list(varobject.varTofunc)
    func = funcList[random.randint(0, len(funcList)-1)]
    if func not in lazy and func not in funcPool:
        if func.surround == pfunc.surround and rv:
            string = generateFunc(func, f, False, True) + string
        else:
            generateFunc(func, f, False)
    lt = funcPool[func]
    length = len(lt)
    varname = lt[random.randint(0, length-1)]

    leftname = varname + varobject.restname
    string += leftname + ','
    return string, leftname

def generateFuncLeftPart_varTowith(varobject, string):

    pwith, withitem_id = list(varobject.varTowith)[0]
    if pwith not in withPool:
        raise Exception(Cyan(\
            'This with statement not in withPool while its '\
                + 'components are being attended'))
    
    withitem = pwith.withitem[withitem_id]
    item, asitem = withitem
    if asitem:
        leftname = asitem.name + varobject.restname
        string += leftname + ','
        return string, leftname
    else:
        leftname = item.name + varobject.restname
        string += leftname + ','
        return string, leftname

def generateFuncLeftPart(string, pfunc, breed, f, rv):

    leftname = ''

    if pfunc.varobjects:

        varobject = pfunc.varobjects[0]
           
        if not varobject.varTocls and \
            not varobject.varTofunc and \
                not varobject.varTowith:

            string, leftname = generateFuncLeftPart_varTonothing(varobject, string)
        
        elif varobject.varTocls:
            string, leftname = generateFuncLeftPart_varTocls(varobject, string, f, pfunc, rv)
        
        elif varobject.varTofunc:
            string, leftname = generateFuncLeftPart_varTofunc(varobject, string, f, pfunc, rv)
        
        elif varobject.varTowith:
            string, leftname = generateFuncLeftPart_varTowith(varobject, string)

        string = string[:-1]
        string += '='

    return string, leftname

def generateFuncRestrictedVarPart(pfunc, string, breed, f, rv):

    restrictedVarNew = ''

    if pfunc.restricted:

        restrictedVarNew = decrypt(pfunc.restricted, pfunc, f, rv=rv)
        string += restrictedVarNew

    return string, restrictedVarNew

def generateFuncNamePart(pfunc, string):

    funcName = ''
    if pfunc.restricted:
        funcName = ''
    else: 
        funcName = pfunc.funcName
        
        if pfunc.funcNameSuffix:
            funcName = funcName.split(pfunc.funcNameSuffix)[0]

    string += funcName + '('
    return string

def generateFuncParamPart(pfunc, string, f, rv):
    for param in pfunc.params:
        string = decrypt(param, pfunc, f, string=string, rv=rv) + ','

    if pfunc.params:
        string = string[:-1]
    string += ')'
    return string

def generateFuncSuffixPart(pfunc, string):
    
    if pfunc.suffix:
        suffix_ = pfunc.suffix.replace('*', '.')
        string += suffix_
    return string

def generateFuncRightPart(pfunc, string, breed, f, rv):
    
    string, restrictedVarNew = generateFuncRestrictedVarPart(pfunc, string, breed, f, rv)
    string = generateFuncNamePart(pfunc, string)
    string = generateFuncParamPart(pfunc, string, f, rv)
    string = generateFuncSuffixPart(pfunc, string)

    return string, restrictedVarNew

def deleteFuncObsoletePart(string):

    string = string.replace('.[', '[')
    return string

def fillIn_funcPool(pfunc, restrictedVarNew, leftname):

    if pfunc not in funcPool:
        if pfunc.Type == 'restrictedOnlyFunc':
            funcPool[pfunc] = (restrictedVarNew, )
        else:
            funcPool[pfunc] = (leftname, )
    else:
        if pfunc.Type == 'restrictedOnlyFunc':
            funcPool[pfunc] += (restrictedVarNew, )
        else:
            funcPool[pfunc] += (leftname, )

def fillIn_clsPool(param, leftname):
    if param not in clsPool:
        clsPool[param] = (leftname, )
    
    else:
        clsPool[param] += (leftname, )    

def fillIn_subsPool(param, leftname):
    if param not in subsPool:
        subsPool[param] = (leftname, )
    
    else:
        subsPool[param] += (leftname, ) 

def generateChildren(breed, param, f):

    if breed and param.children:
        for child in param.children:
            if not child.surround \
                or not param.surround \
                    or child.surround != param.surround:
                
                if param not in child.children or \
                    not random.randint(0, 10):
                    if isinstance(child, pFunc):
                        if child not in funcPool or not random.randint(0, 9):
                            generateFunc(child, f, breed)
                    
                    elif isinstance(child, pWith):
                        generateWith(child, f, breed)

def generateAdjuncts(param, f, master, rv=False):

    '''
    a = fun()
    a.b = 1
    a[0] = a.b
    a.b.c = a[0]
    '''

    '''
    a = fun()
    a.b = 1
    a.b.c = 1
    a[0] = a.b.c

    '''

    if param in lazy or param in clsPool or \
        param in subsPool or random.randint(0, 1):
        if rv: return ''
        return

    lazy.append(param)
    string = ''
    
    for mst in param.masters:
        if mst != master and mst not in funcPool:
            if mst.surround and param.surround and \
                mst.surround == param.surround:
                string = generateFunc(mst, f, False, True) + string
            else:
                generateFunc(mst, f, False)

    if isinstance(param.varobjects[0], pSubs):
        if rv:
            string = generateSubs(param, f, True) + string
        else:
            generateSubs(param, f)
    
    elif isinstance(param.varobjects[0], pVar):
        if rv:
            string = generateCls(param, f, master, True) + string
        else:
            generateCls(param, f, master)

    if rv:
        for child in param.children:
            if child not in subsPool and child not in clsPool:
                if child.surround == param.surround:
                    string += generateAdjuncts(child, f, master, True)
                else:
                    restAdjuncts.append((child, master))
        return string
    
    else:
        for child in param.children:     
            generateAdjuncts(child, f, master)

def generateFunc(pfunc, f, breed, rv=False, lamb=False):

    if isinstance(pfunc, pWith):
        generateWith(pfunc, f, breed)
        return

    if pfunc.surround and \
        pfunc.surround not in withPool:
        generateWith(pfunc.surround, f, breed)
        return
   

    ori_funcName = pfunc.funcName.split(pfunc.funcNameSuffix)[0] \
                    if pfunc.funcNameSuffix else pfunc.funcName

    if ori_funcName in helperFuncDef:
        func = helperFuncDef[ori_funcName]
        if func in funcDefParents:
            parents = funcDefParents[func]
            for parent in parents:
                f.write(astunparse.unparse(parent))

        f.write(astunparse.unparse(func))

    string = generateIndent(pfunc.indent)
    string, leftname = generateFuncLeftPart(string, pfunc, breed, f, rv)
    string, restrictedVarNew = generateFuncRightPart(pfunc, string, breed, f, rv)
    string = deleteFuncObsoletePart(string)
    string += '\n'
    if rv:
        fillIn_funcPool(pfunc, restrictedVarNew, leftname) 
        for adjunct in pfunc.adjuncts:
            if adjunct.surround == pfunc.surround:
                lazy.append(pfunc)
                string += generateAdjuncts(adjunct, f, pfunc, True)
                lazy.reverse()
                lazy.remove(pfunc)
                lazy.reverse()
            
            else:
                restAdjuncts.append((adjunct, pfunc))
        return string

    else:
        if lamb: 
            return string
        else:
            f.write(string)
            fillIn_funcPool(pfunc, restrictedVarNew, leftname) 

            for adjunct in pfunc.adjuncts:
                lazy.append(pfunc)
                generateAdjuncts(adjunct, f, pfunc)
                lazy.reverse()
                lazy.remove(pfunc)
                lazy.reverse()

            generateChildren(breed, pfunc, f)

def generateSubs(psubs, f, rv=False):

    '''
        generate the param string
        when the varobjects[0] is of pSubs class
    '''

    string = generateIndent(psubs.indent)
    

    '''
    Q: Why add this if statement? Could subscript on the left
    have subsTosubs"
    A: Yes. Check this example
        a = fun()
        a[0] = 1
        b = a[0]
        b.c = 2

    which is actually 
        a = fun()
        a[0] = 1
        a[0].c = 2

    where the "a[0]" in "a[0].c = 2" has subsTosubs
    '''

    if not psubs.varobjects[0].subsTosubs:
        psubsstring = decrypt(psubs.varobjects[0].prefix[0], psubs, f, rv=rv, string='')
        psubsstring += '['
        psubsstring = decrypt(psubs.varobjects[0].content[0], psubs, f, string=psubsstring, rv=rv)
        psubsstring += ']' + psubs.varobjects[0].restname
    
    else:
        lt = subsPool[psubs.varobjects[0].subsTosubs]
        psubsstring = lt[random.randint(0, len(lt)-1)] + \
            psubs.varobjects[0].restname 

    fillIn_subsPool(psubs, psubsstring)

    string += psubsstring
    string += '='
    string = decrypt(psubs, psubs, f, rv=rv, string=string)

    if rv: return string + '\n'

    f.write(string + '\n')

def generateWithItems(pwith):

    string = generateIndent(pwith.indent)
    string += 'with ' 
    for withitem in pwith.withitems:
        
        if withitem[0].varTofunc:
            pfunc = list(withitem[0].varTofunc)[0]
            if pfunc not in funcPool:
                raise Exception(Cyan(pfunc.funcName + ' not in funcPool!'))

            lt = funcPool[pfunc]
            length = len(lt)
            
            varname = lt[random.randint(0, length-1)]
            string += varname
        else:
            string += withitem[0].name

        if withitem[1]:
            if not isinstance(withitem[1], pVar):
                raise Exception(Cyan('Unexpected type of withitem[1]!'))
            string += ' as ' + withitem[1].name
        string += ','
    string = string[:-1]
    string += ':'
    return string

def generateWithBody(pwith, f, breed):
    
    string_ = ''
    for ele in pwith.body:
        if ele in funcPool or ele in withPool:
            continue

        if isinstance(ele, pFunc):
            string_ += generateFunc(ele, f, breed, True)

        elif isinstance(ele, pWith):
            string_ += generateWith(ele, f, breed, True)

    return string_

def generateWith(pwith, f, breed, rv=False):

    '''generate parents'''
    
    for parent in pwith.parents:
        if parent not in lazy and parent not in funcPool:
            generateFunc(parent, f, False)

    '''end'''

    withPool.add(pwith)
    
    string = generateWithItems(pwith)
    string += '\n'
    string += generateWithBody(pwith, f, breed)

    if rv: return string

    f.write(string + '\n')
    generateRestAdjuncts(f)
    generateWithChildren(breed, pwith, f)

def generateRestAdjuncts(f):
    for adjunct, pfunc in restAdjuncts:
        lazy.append(pfunc)
        generateAdjuncts(adjunct, f, pfunc)
        lazy.reverse()
        lazy.remove(pfunc)
        lazy.reverse() 

def generateWithChildren(breed, pwith, f):

    if breed:
        for ele in pwith.body:
            if isinstance(ele, pFunc):
                for child in ele.children:
                    if child not in funcPool:
                        generateFunc(child, f, breed)

            elif isinstance(ele, pWith):
                generateWithChildren(breed, ele, f)
            
def generateCls_varTofunc(varobject, f, param, rv):
    
    randit_ = random.randint(0, len(varobject.varTofunc)-1)
    pfunc = list(varobject.varTofunc)[randit_]
    string = ''
    if pfunc not in lazy and pfunc not in funcPool:
        if rv and param.surround == pfunc.surround:
            string += generateFunc(pfunc, f, False, True)
        else:
            generateFunc(pfunc, f, False)

    if pfunc not in funcPool:
        raise Exception(pfunc.funcName + \
            ' not in funcPool')
    else:
        lt = funcPool[pfunc]
        length = len(lt)
        varname = lt[random.randint(0, length-1)]
        string += generateIndent(param.indent) + varname
    return string

def generateCls_varTocls(varobject, f, master, param, rv):
    
    randit_ = random.randint(0, len(varobject.varTocls)-1)
    paramcls = list(varobject.varTocls)[randit_]
    string = ''
    if paramcls not in clsPool:
        if rv and paramcls.surround == param.surround:
            string += generateAdjuncts(paramcls, f, master, True)
        else:
            generateAdjuncts(paramcls, f, master, False)

    if paramcls not in clsPool:
        raise Exception(paramcls.name + paramcls.restname + \
            ' not in clsPool')
    else:
        lt = clsPool[paramcls]
        rn = lt[random.randint(0, len(lt)-1)]
        varname = rn 
        string += generateIndent(param.indent) + varname
    return string

def generateCls(param, f, master, rv=False):
        
    varname = ''
    varobject = param.varobjects[0]
    
    if varobject.varTofunc:
        varname = generateCls_varTofunc(varobject, f, param, rv)
    
    elif varobject.varTocls:
        varname = generateCls_varTocls(varobject, f, master, param, rv)

    else:
        varname = varobject.name
    varname += varobject.restname
    fillIn_clsPool(param, varname)
    string = varname + '='
    string = decrypt(param, param, f, string=string, rv=rv)
    if rv: return string + '\n'
    f.write(string + '\n')

def generate():

    f = open('byproduct/program.py', 'w')

    for im in importSet:
        f.write(im + '\n')
    f.write('\n')

    print(Magenta('len(ingredient) = ' + str(len(ingredient))))
    id = random.randint(0, len(ingredient)-1)
    print(Yellow('id = ' + str(id)))
    if isinstance(ingredient[id], pFunc):
        print(Yellow('ingredient = ' + str(ingredient[id].funcName)))
    if isinstance(ingredient[id], pFunc):
        generateFunc(ingredient[id], f, True)

    elif isinstance(ingredient[id], pWith):
        generateWith(ingredient[id], f, True)

    else:
        raise Exception('Unexpected element of ingredient')
        
    f.close()

