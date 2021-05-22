import ast
from TVMfuzz.elements import *
import random
from TVMfuzz.syntax import *
from TVMfuzz.analyzeSyntax import dealWithStatement
from TVMfuzz.colors import *
from TVMfuzz.utils import varNameGenerator
import copy

'''nestplus components'''
def getAllElementsFromAttrCallSubsName(value):
    
    # import astunparse
    # print(Green(astunparse.unparse(value)))

    rcur = []
    while True:
        rcur.append(value)
        if isinstance(value, ast.Call):
            value = value.func
        else:
            if not isinstance(value, ast.Name) and \
                not isinstance(value, ast.Constant):
               
                value = value.value
            else:
                break

    return rcur

def buildFullString(rcur, indent, surround):

    fullstr = ''
    len_rcur = len(rcur)
    cnt = 0
    for ele in rcur[::-1]:
        cnt += 1
        if isinstance(ele, ast.Name):
            fullstr = buildNameString(ele, fullstr)

        elif isinstance(ele, ast.Attribute):
            fullstr = buildAttributeString(ele, fullstr)

        elif isinstance(ele, ast.BinOp) or isinstance(ele, ast.UnaryOp):
            param = recognizeMultiAssignment(ele, indent=indent)
            rn = varNameGenerator(varnamesRead)
            varobject = pVar(rn)
            dealWithStatement(param=param, varobjects=[varobject])
            fullstr += rn

        elif isinstance(ele, ast.Subscript):
            if cnt < len_rcur:
                fullstr = buildSubscriptString(ele, fullstr, indent)
            else:
                return buildSubscriptString(ele, fullstr, indent, True)

        elif isinstance(ele, ast.Call):
            if cnt < len_rcur:
                fullstr = buildCallString(ele, fullstr, indent, surround)
            else:
                return buildCallString(ele, fullstr, indent, surround, True)
        
        elif isinstance(ele, ast.Constant):
            fullstr += '\'\'\'' + ele.value + '\'\'\''

    return fullstr    

def buildCallString(ele, fullstr, indent, surround, rv=False):

    params = fillInParams(ele.args, 
                        ele.keywords, 
                        indent, 
                        surround)

    pfunc = pFunc(funcName=fullstr,
                    Type='function',
                    indent=indent,
                    surround=surround,
                    params=params)
    
    if rv:
        return pfunc

    name_func = varNameGenerator(varnamesRead)
    varobject_func = pVar(name_func)

    dealWithStatement(param=pfunc, varobjects=[varobject_func])
    
    fullstr = name_func

    return fullstr

def buildNameString(ele, fullstr):
    return fullstr+ele.id

def buildAttributeString(ele, fullstr):
    return fullstr+'.'+ele.attr

def buildSubscriptString(ele, fullstr, indent, judge=False):

    name = varNameGenerator(varnamesRead)
    varobject = pVar(name)
    psubs = pSubs()
    psubs.add_prefix(pVar(fullstr))
    slice = ele.slice
    rv = recognizeMultiAssignment(slice, outsideSlice=True)

    if isinstance(rv, pVar):
        fullstr += '[' + rv.name + ']' 
        varnamesRead.add(rv.name)
        psubs.add_content(rv)
    
    elif isinstance(rv, pNumber):
        fullstr += '[' + str(rv.num) + ']'
        psubs.add_content(rv)
    
    elif isinstance(rv, pConst):
        fullstr += '[\'' + str(rv.const) + '\']'
        psubs.add_content(rv)
    
    elif isinstance(rv, pBinop) or isinstance(rv, pUop):
        rn = varNameGenerator(varnamesRead)
        varobject = pVar(rn)
        dealWithStatement(param=rv, varobjects=[varobject])
        psubs.add_content(varobject)
        fullstr += '[' + rn + ']'

    elif isinstance(rv, pTuple):
        '''
            a[:, 2] = ...
        '''
        psubs.add_content(rv)
        fullstr += '['
        for ele in rv.content:
            if isinstance(ele, pConst):
                fullstr += ele.const + ','
            elif isinstance(ele, pNumber):
                fullstr += str(ele.num) + ','
            elif isinstance(ele, pVar):
                fullstr += ele.name + ','
            elif isinstance(ele, pSlice):
                fullstr += ':,'
        
        if rv.content:
            fullstr = fullstr[:-1]
        fullstr += ']'

    else:
        rn = varNameGenerator(varnamesRead)
        pvar = pVar(rn)
        dealWithStatement(param=rv, varobjects=[pvar])
        fullstr += '[' + rn + ']'
        psubs.add_content(pvar)

    psubs.add_fullstr(fullstr)
    psubs.add_indent(indent)
    if judge:
        return psubs
    
    dealWithStatement(param=psubs, varobjects=[varobject])
    fullstr = name
    return fullstr

def nestplus(value, indent, surround):

    rcur = getAllElementsFromAttrCallSubsName(value)
    
    return buildFullString(rcur, indent, surround)

'''end'''

def fillInParams(args_, keywords_, indent, surround):

    params = []
    if args_:
        for arg in args_:
            params.append(recognizeMultiAssignment(
                                            arg,
                                            outsideTuple=False, 
                                            outsideFunction=True, 
                                            indent=indent, 
                                            surround=surround))

    if keywords_:
        for keyw in keywords_:
            
            if not keyw.arg:
                '''
                    In the following situation
                    mod.set_input(**params)
                '''
                
                pa = recognizeMultiAssignment(
                                        keyw.value,
                                        outsideTuple=False, 
                                        outsideFunction=True, 
                                        indent=indent, 
                                        surround=surround)
                pa.pref = '**'
                params.append(pa)

            else:
                param = pKeyword()
                param.add_keyWordStr(keyw.arg)
                value = keyw.value
                param.add_keywordContent(recognizeMultiAssignment(
                                                        value, 
                                                        outsideFunction=True, 
                                                        indent=indent,
                                                        surround=surround))
                params.append(param)
    return params 

def judgeMutable(param):
    
    if param.Type == 'list' or param.Type == 'tuple':
        for c in param.content:
            judgeMutable(c)
    elif param.Type == 'dict' or param.Type == 'const' or param.Type == 'variable':
        global mutable
        mutable = False
        return
    elif param.Type == 'number':
        return
    elif param.Type == 'keyword':
        judgeMutable(param.keywordContent[0])

'''recognizeMultiAssignment's components'''
def recognizeNameAttr(value, 
                        indent,
                        surround):

    name = nestplus(value, indent, surround)
    if name == None:
        raise Exception(Cyan('Expect string but receive None'))
    param = pVar(name)
    param.add_indent(indent)
    return param

def recognizeSubs(value, indent, surround):

    return nestplus(value, indent, surround)
    
def recognizeConst(value, indent):

    str_ = value.value
    param = None
    if isinstance(str_, str):
        param = pConst(str_)
        param.add_indent(indent)
    elif isinstance(str_, int) or isinstance(str_, float):
        param = pNumber(str_)
        param.add_indent(indent)
    else:
        param = pNone()
        param.add_indent(indent)

    return param

def recognizeCall(value, 
                  indent,
                  outsideFunction,
                  outsideList,
                  outsideDict,
                  insideTuple,
                  outCalculation,
                  outsideSet,
                  surround):
    
    pfunc = nestplus(value, indent, surround)
    pfunc.add_indent(indent)

    if outsideFunction or \
        outsideList or \
            outsideDict or \
                insideTuple or \
                    outCalculation or \
                        outsideSet:
        
        pfunc.add_surround(surround)
        name = varNameGenerator(varnamesRead)
        varobject = pVar(name)
        
        dealWithStatement(param=pfunc, varobjects=[varobject])

        return copy.deepcopy(varobject)

    return pfunc

def recognizeKey(key, indent, param, surround):
    
    rv = recognizeMultiAssignment(key, 
                                  outsideDict=True, 
                                  indent=indent, 
                                  surround=surround)
    
    param.add_keyContents(rv)

def recognizeValue(v,  indent, param, surround):

    rv = recognizeMultiAssignment(v, 
                                  outsideDict=True, 
                                  indent=indent,
                                  surround=surround)

    param.add_valueContents(rv)

def recognizeDict(value, indent, surround):
    
    param = pDict()
    param.add_indent(indent)
    for key, v in zip(value.keys, value.values):

        recognizeKey(key, indent, param, surround)

        recognizeValue(v, indent, param, surround)
        
    return param

def recognizeSet(value, indent, surround):

    param = pSet()
    param.add_indent(indent)
    
    for elt in value.elts:
        rv = recognizeMultiAssignment(elt, 
                                      indent=indent, 
                                      surround=surround,
                                      outsideSet=True)
        param.add_content(rv)
    
    return param

def recognizeList(value,  indent, surround):

    param = pList()
    param.add_indent(indent)
    for ele in value.elts:
        rv = recognizeMultiAssignment(ele, 
                                      outsideList=True, 
                                      indent=indent,
                                      surround=surround)

        param.add_content(rv)

    judgeMutable(param)
    global mutable
    param.mutable = mutable
    mutable = True
    return param

def recognizeTupleInsideTuple(value,  indent, param, surround):
    
    for ele in value.elts:
        rv = recognizeMultiAssignment(ele, 
                                      insideTuple=True, 
                                      indent=indent,
                                      surround=surround)
 
        param.add_content(rv)

def recognizeIndependentTuple(value, indent, surround):
    
    params = []
    for ele in value.elts:
        params.append(recognizeMultiAssignment(ele, 
                                               outsideTuple=True, 
                                               indent=indent,
                                               surround=surround))
    return params

def recognizeTupleInsideFuncListDictTupleSet(value, indent, param, surround):
    
    for ele in value.elts:
        rv = recognizeMultiAssignment(ele, 
                                      insideTuple=True, 
                                      indent=indent, 
                                      surround=surround)

        param.add_content(rv)

def recognizeNotTupleInsideTuple(outsideFunction,
                                 outsideList, 
                                 outsideDict, 
                                 outsideTuple, 
                                 outsideSet,
                                 insideTuple,
                                 outsideSlice,
                                 outCalculation,
                                 value, 
                                 indent, 
                                 param, 
                                 surround):

    if not outsideFunction and not outsideList and not outsideDict \
        and not outsideTuple and not outsideSet and not insideTuple \
        and not outsideSlice and not outCalculation:

        return recognizeIndependentTuple(value, indent, surround)

    else:

        recognizeTupleInsideFuncListDictTupleSet(value, indent, param, surround)
        return param 
        
def recognizeTuple(outsideTuple, 
                   outsideFunction, 
                   outsideList, 
                   outsideDict,
                   outsideSet, 
                   insideTuple,
                   outsideSlice,
                   outCalculation,
                   indent,
                   value,
                   surround):
    param = pTuple()
    param.add_indent(indent)
    if outsideTuple:
        recognizeTupleInsideTuple(value,  indent, param, surround)
        
    else:
        param = recognizeNotTupleInsideTuple(outsideFunction,
                                            outsideList, 
                                            outsideDict, 
                                            outsideTuple, 
                                            outsideSet,
                                            insideTuple,
                                            outsideSlice,
                                            outCalculation,
                                            value, 
                                            indent, 
                                            param, 
                                            surround)
    return param

def recogizeBinOpString(value, param):
    op = value.op
    if isinstance(op, ast.Add): param.op = ' + '
    elif isinstance(op, ast.Sub): param.op = ' - '
    elif isinstance(op, ast.Mult): param.op = ' * '
    elif isinstance(op, ast.Div): param.op = ' / '
    elif isinstance(op, ast.FloorDiv): param.op = ' // ' 
    elif isinstance(op, ast.Mod): param.op = ' % ' 
    elif isinstance(op, ast.Pow): param.op = ' ** ' 
    elif isinstance(op, ast.LShift): param.op = ' << ' 
    elif isinstance(op, ast.RShift): param.op = ' >> ' 
    elif isinstance(op, ast.BitOr): param.op = ' | ' 
    elif isinstance(op, ast.BitXor): param.op = ' ^ ' 
    elif isinstance(op, ast.BitAnd): param.op = ' & '
    elif isinstance(op, ast.MatMult): param.op = ' @ '

def recognizeBinOpLeftPart(value,  indent, param, surround):

    rv = recognizeMultiAssignment(value.left, 
                                  outCalculation=True, 
                                  indent=indent,
                                  surround=surround)
    param.add_left(rv)

def recognizeBinOpRightPart(value,  indent, param, surround):

    rv = recognizeMultiAssignment(value.right, 
                                  outCalculation=True, 
                                  indent=indent,
                                  surround=surround)

    param.add_right(rv)

def recognizeCompOp(value, param):
    ops = value.ops

    for op in ops:
        if isinstance(op, ast.Eq): param.add_op(' == ')
        elif isinstance(op, ast.NotEq): param.add_op(' != ')
        elif isinstance(op, ast.Lt): param.add_op(' < ')
        elif isinstance(op, ast.LtE): param.add_op(' <= ')
        elif isinstance(op, ast.Gt): param.add_op(' > ')
        elif isinstance(op, ast.GtE): param.add_op(' >= ')
        elif isinstance(op, ast.Is): param.add_op(' is ')
        elif isinstance(op, ast.IsNot): param.add_op(' is not ')
        elif isinstance(op, ast.In): param.add_op(' in ')
        elif isinstance(op, ast.NotIn): param.add_op(' not in ')

def recognizeCompLeftPart(value, indent, param, surround):
    
    rv = recognizeMultiAssignment(value.left, 
                                  outCalculation=True, 
                                  indent=indent,
                                  surround=surround)
    param.add_left(rv)

def recognizeCompRightPart(value, indent, param, surround):

    for comparator in value.comparators:

        rv = recognizeMultiAssignment(comparator, 
                                    outCalculation=True, 
                                    indent=indent,
                                    surround=surround)

        param.add_right(rv)

def recognizeComp(value, indent, surround, i=None):

    param = pComp()
    param.add_indent(indent)
    recognizeCompOp(value, param)
    recognizeCompLeftPart(value, indent, param, surround)
    recognizeCompRightPart(value, indent, param, surround)
    return param

def recognizeLambda(value, indent, surround):

    param = pLambda()
    param.add_indent(indent)
    for arg in value.args.args:
        param.add_arg(pVar(arg.arg))
    param.add_body(recognizeMultiAssignment(value.body, indent=indent, surround=surround))
    # import astunparse
    # print(Blue(astunparse.unparse(value)))    
    # param.add_value(value)
    return param

def recognizeBinOp(value, indent, surround):
    
    param = pBinop()
    param.add_indent(indent)
    recogizeBinOpString(value, param)
    recognizeBinOpLeftPart(value, indent, param, surround)
    recognizeBinOpRightPart(value, indent, param, surround)
    return param

def recognizeUopString(value, param):
    op = value.op 
    if isinstance(op, ast.Invert): param.op = '~'
    elif isinstance(op, ast.Not): param.op = 'not '
    elif isinstance(op, ast.UAdd): param.op = '+' # +1
    elif isinstance(op, ast.USub): param.op = '-' # -1

def recognizeUop(value, indent, surround):

    param = pUop()
    param.add_indent(indent)
    recognizeUopString(value, param)

    rv = recognizeMultiAssignment(value.operand, 
                                  outCalculation=True, 
                                  indent=indent,
                                  surround=surround)

    param.add_operand(rv)
    return param

def recognizeMultiAssignment(value, 
                             outCalculation=False, 
                             outsideTuple=False, 
                             insideTuple=False, 
                             outsideFunction=False, 
                             outsideList=False, 
                             outsideDict=False,
                             outsideSet=False,
                             outsideSlice=False,
                             indent=0,
                             surround=None):


    if isinstance(value, ast.Name) or \
       isinstance(value, ast.Attribute):

        return recognizeNameAttr(value, 
                                indent,
                                surround)
    
    elif isinstance(value, ast.Subscript):
        
        return recognizeSubs(value, indent, surround)

    elif isinstance(value, ast.Constant):
        
        return recognizeConst(value, indent)

    elif isinstance(value, ast.Call): 
        # import astunparse
        # print(Blue(astunparse.unparse(value)))
        return recognizeCall(value, 
                             indent,
                             outsideFunction,
                             outsideList,
                             outsideDict,
                             insideTuple,
                             outCalculation,
                             outsideSet,
                             surround)
            
    elif isinstance(value, ast.Dict):

        return recognizeDict(value,  indent, surround)

    elif isinstance(value, ast.Set):

        return recognizeSet(value, indent, surround)

    elif isinstance(value, ast.List):
        
        return recognizeList(value,  indent, surround)
    
    elif isinstance(value, ast.Tuple):

        return recognizeTuple(outsideTuple, 
                            outsideFunction, 
                            outsideList, 
                            outsideDict, 
                            outsideSet,
                            insideTuple,
                            outsideSlice,
                            outCalculation,
                            indent,
                            value,
                            surround)
        
    elif isinstance(value, ast.BinOp):

        return recognizeBinOp(value,  indent, surround)
    
    elif isinstance(value, ast.UnaryOp):
        
        return recognizeUop(value,  indent, surround)

    elif isinstance(value, ast.Compare):
 
        return recognizeComp(value, indent, surround)

    elif isinstance(value, ast.Starred):

        param = recognizeMultiAssignment(value.value, 
                             outCalculation, 
                             outsideTuple, 
                             insideTuple, 
                             outsideFunction, 
                             outsideList, 
                             outsideDict,
                             outsideSet,
                             outsideSlice,
                             indent,
                             surround)
        param.pref = '*'
        return param
    
    elif isinstance(value, ast.Slice):
        
        param = pSlice()
        return param

    elif isinstance(value, ast.Lambda):

        return recognizeLambda(value, indent, surround)

    else:
        # pass
        raise Exception(Cyan('We never handle this ast Type: ' + str(type(value))))

'''end'''



'''interpreter'''
def interpreterForFunction(rn, ln, indent, surround):
    '''
    May contain bugs!!!
    
    Now we cannot handle the situation where variables and functions both appear 
    in the right-hand side, such as "a, b, c = c, fun()". Because we do not know
    the number of fun()'s returned value. In this case, We can do nothing but 
    hope the above form will never shows up in the testing programs. In other
    words, if the right-hand side includes a function, then we tacitly approve
    that the function shows at the end.
    '''

    varobjects = []
    if isinstance(ln, list):
        for i in ln:
            varobjects.append(i)
    else:
        varobjects.append(ln)
    if rn.restricted:
        rn.add_Type('restrictedFunc')
    rn.add_indent(indent)
    rn.add_surround(surround)
    dealWithStatement(param=rn, varobjects=varobjects)

def interpreter(ln, rn, surround=None, indent=0):

    '''
    If ln and rn are both collections(e.g. tuple/list), then we should take apart the collections and get
    the "ln = rn" relationship for all single elements contained in the collections.
    '''

    if not isinstance(rn, pFunc):
        
        # rn.add_surround(surround)
        if rn.Type == 'variable':
            rn.add_indent(indent)
        
        varobjects = []
        if isinstance(ln, list):
            for i in ln:
                varobjects.append(i)
        else:
            varobjects.append(ln)
        rn.add_surround(surround)
        # print(Green(str(rn)))
        dealWithStatement(param=rn, varobjects=varobjects)

    else:
        
        interpreterForFunction(rn, ln, indent, surround)

'''end'''
 
'''Assign handler'''
def assignNodeLeftHand(element, indent):

    lparams = []
    for target in element.targets:
        lps = recognizeMultiAssignment(target, indent=indent)
        if not isinstance(lps, list):
            lparams.append(lps)
        else:
            lparams += lps

    return lparams

def assignNodeRightHand(element, indent, surround):

    rparams = []
    rps = recognizeMultiAssignment(element.value, 
                                   indent=indent,
                                   surround=surround)
    if not isinstance(rps, list):
        rparams.append(rps)
    else:
        rparams += rps
    return rparams

def assignNodeReadyForInterpreter(lenleft, 
                                  lenright, 
                                  lparams, 
                                  rparams, 
                                  surround, 
                                  indent):
    if lenleft == 1 and lenright > lenleft:
        ''' 
            In this situation, right-side is a tuple and it's
            assigned to the variable on the left-hand side.
            But TVMfuzz miscomprehend it as a list of params
            but not one param with type tuple
        '''

        ln = lparams[0]
        rn = pTuple()
        for ele in rparams:
            rn.add_content(ele)
        varnamesRead.add(ln.name)
        interpreter(ln, rn, surround=surround, indent=indent)

    else:
        for i in range(lenright):
            if i == lenright-1 and i != lenleft-1:
                '''
                Target at the situation where rightnames includes one function and varnames is longer
                than rightnames
                '''
                # if rparams[i].Type != 'function':
                #     raise Exception(
                #         'Middle function with more than one returned value! ' + rparams[i].Type)
                ln, rn = lparams[i:], rparams[i]
            else:
                ln, rn = lparams[i], rparams[i]
            if isinstance(ln, list):
                for i in ln:
                    # if isinstance(i, pTuple):
                    #     print(Magenta(str(i)))
                    varnamesRead.add(i.name)
            else:
                if isinstance(ln, pVar):
                    varnamesRead.add(ln.name)
            interpreter(ln, rn, surround=surround, indent=indent)

def AssignNode(element, surround=None, indent=0, func=None):

    if not func:
        helperStatDef_global.append(element)
    else:
        if func in helperStatDef_local:
            helperStatDef_local[func] += (element, )
        else:
            helperStatDef_local[func] = (element, )

    if not isinstance(surround, Param) and surround != None:
        raise Exception(Cyan('Type error! Expect Param but receive ' + str(type(surround))))

    '''left-hand side'''
    lparams = assignNodeLeftHand(element, indent)

    '''right-hand side'''
    rparams = assignNodeRightHand(element, indent, surround)
    '''deal'''
    assignNodeReadyForInterpreter(len(lparams), 
                                  len(rparams), 
                                  lparams, 
                                  rparams, 
                                  surround, 
                                  indent)
    

'''end'''