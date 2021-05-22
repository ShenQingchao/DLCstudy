from TVMfuzz.utils import varNameGenerator
from TVMfuzz.colors import *
from TVMfuzz.syntax import *
from TVMfuzz.elements import *
import copy

st_id = 0
withid = 0

def dealWithImport(type, fromWhat=None, importWhat=None, asWhat = None):
                            
    if type == 'import' and fromWhat != None  or \
        type == 'fromImport' and fromWhat == None:
        raise Exception(Cyan('Incorrect importClass initiation.'))
    
    if type == 'import':
        fullname = 'import ' + importWhat + \
                        (' as ' + asWhat if asWhat != None else '')
            
    else:
        fullname = 'from ' + fromWhat + ' import ' + importWhat + \
                        (' as ' + asWhat if asWhat != None else '')

    importSet.add(fullname)


import os

funcID_ = os.getenv('funcID')
fileID_ = os.getenv('fileID')
isFunc_ = bool(os.getenv('isFunc'))
mark = '>>>'
markGlobal = '>>>'

if isFunc_:
    mark += fileID_ + '>>>' + funcID_
    markGlobal += fileID_
else:
    mark += fileID_
    markGlobal += fileID_

def In_varTowith_IfNotPolysyllabic(params, ind, varname):

    pwith, withitem_id, st_id = varTowith[varname]
    params[ind].update_varTowith_ele((pwith, withitem_id))

def In_varTofuncst_IfNotPolysyllabic(param, params, ind, varname, paramType):

    param_, st_id = varTofuncst[varname]
    
    if paramType == 'function' or \
        paramType == 'with':

        param.add_parent(param_)
        param_.add_child(param)

    elif paramType == 'records':
        if isinstance(param, pVar):
            params[ind].add_master(param_)
            params[ind].shouldBeAdjunct = True
        else:
            param.add_master(param_)
            param.shouldBeAdjunct = True

    elif paramType == 'cls' or paramType == 'subs':
        if isinstance(param, pVar):
            params[ind].add_master(param_)
            param_.add_adjunct(params[ind])
        else:
            param.add_master(param_)
            param_.add_adjunct(param)

    params[ind].update_varTofunc_ele(param_)

def In_records_IfNotPolysyllabic(varname, param, params, ind, paramType):
    
    restname = params[ind].restname
    parentParam, st_id = records[varname]
    parentParam = copy.copy(parentParam)
    pref = params[ind].pref
    surround = params[ind].surround
    params[ind] = parentParam
    params[ind].pref = pref
    params[ind].add_surround(surround)
    params[ind].add_restname(parentParam.restname+restname)
    # if paramType == 'records':
    #     replaceAndFindParentsOfParams(params, ind, param, paramType)
    if paramType == 'cls' or paramType == 'subs':

        if isinstance(param, pVar):
            for parent in parentParam.parents:
                parent.add_child(params[ind])

            for master in parentParam.masters:
                params[ind].add_master(master)

            if parentParam.shouldBeAdjunct:
                for master in parentParam.masters:
                    master.add_adjunct(params[ind])

        else:
            for parent in parentParam.parents:
                parent.add_child(param)
            
            for master in parentParam.masters:
                param.add_master(master)

            if parentParam.shouldBeAdjunct:
                for master in parentParam.masters:
                    master.add_adjunct(param)
    
    elif paramType == 'function' or paramType == 'with':
        for master in parentParam.masters:
            param.add_parent(master)
            master.add_child(param)
        
def In_clsInstanceToParam_IfNotPolysyllabic(param, params, ind, varname, paramType):

    parentParam, st_id = clsInstanceToParam[varname]

    if paramType == 'records':
        if isinstance(param, pVar):
            params[ind].add_parent(parentParam)
            params[ind].update_masters(parentParam.masters)
        else:
            param.add_parent(parentParam)
            param.update_masters(parentParam.masters)
    
    elif paramType == 'cls' or paramType == 'subs':
        if isinstance(param, pVar):
            params[ind].add_parent(parentParam)
            parentParam.add_child(params[ind])
            params[ind].update_masters(parentParam.masters)
        else:
            param.add_parent(parentParam)
            parentParam.add_child(param)
            param.update_masters(parentParam.masters)
    
    elif paramType == 'function' or paramType == 'with':
        for master in parentParam.masters:
            master.add_child(param)
            param.add_parent(master)

    params[ind].update_varTocls_ele(parentParam)

def max3(a, b, c):
    return max(max(a, b), c)

def max4(a, b, c, d):
    return max(a, max3(b, c, d))

def buildRelationshipIfNotPolysyllabic(pres, param, params, ind, paramType):
    
    pre = pres
    find = False
    varTofuncst_id = -1
    clsInstanceToParam_id = -1
    records_id = -1
    with_id = -1

    for mark_ in [mark, markGlobal]:
        
        varname = pre + mark_

        if varname in varTofuncst:
            varTofuncst_id = varTofuncst[varname][-1]

        if varname in clsInstanceToParam:
            clsInstanceToParam_id = clsInstanceToParam[varname][-1]

        if varname in records:
            records_id = records[varname][-1]

        if varname in varTowith:
            with_id = varTowith[varname][-1]

        if varTofuncst_id != -1 or clsInstanceToParam_id != -1 or \
            records_id != -1 or with_id != -1:
            find = True
        
        maxi = max4(varTofuncst_id, clsInstanceToParam_id, records_id, with_id)

        if find:
            if maxi == varTofuncst_id:
                In_varTofuncst_IfNotPolysyllabic(param, params, ind, varname, paramType)
            
            elif maxi == clsInstanceToParam_id:
                In_clsInstanceToParam_IfNotPolysyllabic(param, params, ind, varname, paramType)
            
            elif maxi == records_id:
                In_records_IfNotPolysyllabic(varname, param, params, ind, paramType)

            elif maxi == with_id:
                In_varTowith_IfNotPolysyllabic(params, ind, varname)

            break
    
    # if not find:
    #     print(Cyan('Seems like an unreferenced variable: ' + pres))
        # raise Exception(
        #     Cyan('Unreferenced variable: ' + pres))

def constitutePres(pres):
    pre = ''
    preslist = pres.split('.')
    pres = []
    for i in range(len(preslist)):
        ele = preslist[i]
        if pre == '':
            pre = ele 
        else:
            pre += '.' + ele 
        pres.append(pre)
    return pres

def In_varTowith_IfPolysyllabic(params, pres, pre, mark_, ind):

    pwith, withitem_id, st_id = varTowith[pre+mark_]
    params[ind].update_varTofunc_ele(pwith)
    fullname = pres[len(pres)-1]
    restname = ''
    if pre != fullname: 
        restname = fullname[len(pre):]

    params[ind].add_restname(restname)
    params[ind].add_name(pre)

def In_varTofuncst_IfPolysyllabic(param, params, pres, pre, mark_, ind, paramType):
    
    parentParam, st_id = varTofuncst[pre+mark_]
    
    if paramType == 'function' or paramType == 'with':
        param.add_parent(parentParam)
        parentParam.add_child(param)
    
    elif paramType == 'records':
        if isinstance(param, pVar):
            params[ind].add_master(parentParam)
            params[ind].shouldBeAdjunct = True
        else:
            param.add_master(parentParam)
            param.shouldBeAdjunct = True
    
    elif paramType == 'cls' or paramType == 'subs':

        if isinstance(param, pVar):
            params[ind].add_master(parentParam)
            parentParam.add_adjunct(params[ind])
        else:
            param.add_master(parentParam)
            parentParam.add_adjunct(param)
    
    params[ind].update_varTofunc_ele(parentParam)
    fullname = pres[len(pres)-1]
    restname = ''
    if pre != fullname: 
        restname = fullname[len(pre):]

    params[ind].add_restname(restname)
    params[ind].add_name(pre)

def In_clsInstanceToParam_IfPolysyllabic(param, params, pres, pre, mark_, ind, paramType):
    
    parentParam, st_id = clsInstanceToParam[pre+mark_]
    fullname = pres[len(pres) - 1]
    restname = ''
    if pre != fullname:
        restname = fullname[len(pre):]
        
    params[ind].add_restname(restname)
    params[ind].add_name(pre)
    params[ind].update_varTocls_ele(parentParam)
    if paramType == 'cls' or paramType == 'subs':
        if isinstance(param, pVar):
            params[ind].add_parent(parentParam)
            parentParam.add_child(params[ind])
            params[ind].update_masters(parentParam.masters)
        else:
            param.add_parent(parentParam)
            parentParam.add_child(param)
            param.update_masters(parentParam.masters)

    elif paramType == 'records':
        if isinstance(param, pVar):
            params[ind].add_parent(parentParam)
            params[ind].update_masters(parentParam.masters)
        else:
            param.add_parent(parentParam)
            param.update_masters(parentParam.masters)

    elif paramType == 'function' or paramType == 'with':
        for master in parentParam.masters:
            master.add_child(param)
            param.add_parent(master)

def In_records_IfPolysyllabic(param, params, pres, pre, mark_, ind, paramType):

    fullname = pres[len(pres)-1]
    restname = ''
    if pre != fullname:
        restname = fullname[len(pre):]

    parentParam, st_id = records[pre+mark_]
    pref = params[ind].pref
    surround = params[ind].surround
    parentParam = copy.copy(parentParam)
    params[ind] = parentParam
    params[ind].pref = pref
    params[ind].add_surround(surround)
    ''' an example for restname handling
        a = fun()
        b = fun2()
        d = a.c
        x = d.a
    '''

    params[ind].add_restname(parentParam.restname + restname)

    if paramType == 'cls' or paramType == 'subs':
        if isinstance(param, pVar):
            for parent in parentParam.parents:
                parent.add_child(params[ind])

            for master in parentParam.masters:
                params[ind].add_master(master)
            
            if parentParam.shouldBeAdjunct:
                for master in parentParam.masters:
                    master.add_adjunct(params[ind])
        else:
            for parent in parentParam.parents:
                parent.add_child(param)
            
            for master in parentParam.masters:
                param.add_master(master)

            if parentParam.shouldBeAdjunct:
                for master in parentParam.masters:
                    master.add_adjunct(param)
    
    elif paramType == 'function' or paramType == 'with':
        for master in parentParam.masters:
            master.add_child(param)
            param.add_parent(master)

def buildRelationshipIfPolysyllabic(pres, param, params, ind, paramType):
    
    find = False
    pres = constitutePres(pres)

    varTofuncst_id = -1
    clsInstanceToParam_id = -1
    records_id = -1
    with_id = -1

    for pre in pres[::-1]:
        for mark_ in [mark, markGlobal]:
            
            if pre+mark_ in varTofuncst:
                varTofuncst_id = varTofuncst[pre+mark_][-1]
                
            if pre+mark_ in clsInstanceToParam:
                clsInstanceToParam_id = clsInstanceToParam[pre+mark_][-1]

            if pre+mark_ in records:
                records_id = records[pre+mark_][-1]

            if pre+mark_ in varTowith:
                with_id = varTowith[pre+mark_][-1]

            if varTofuncst_id != -1 or clsInstanceToParam_id != -1 or \
                records_id != -1 or with_id != -1:
                find = True

            maxi = max4(varTofuncst_id, clsInstanceToParam_id, records_id, with_id)

            if find:
                if maxi == varTofuncst_id:
                    In_varTofuncst_IfPolysyllabic(param, 
                            params, pres, pre, mark_, ind, paramType)
                
                elif maxi == clsInstanceToParam_id:
                    In_clsInstanceToParam_IfPolysyllabic(param, 
                            params, pres, pre, mark_, ind, paramType)
                
                elif maxi == records_id: 
                    In_records_IfPolysyllabic(param, 
                            params, pres, pre, mark_, ind, paramType)

                elif maxi == with_id:
                    In_varTowith_IfPolysyllabic(params, pres, pre, mark_, ind)

                break
        if find:
            break

    # if not find and pres[-1] not in functionDefNames:
    #     print(Cyan('Seems like there is an unreferenced variable: ' + params[ind].name))
        #     raise Exception(Cyan('Unreferenced variable: ' + params[ind].name))

def buildRelationshipVar(params, ind, param, paramType):
    
    pres = params[ind].name
    if '.' not in pres:
        buildRelationshipIfNotPolysyllabic(pres, param, params, ind, paramType)
        
    else:
        buildRelationshipIfPolysyllabic(pres, param, params, ind, paramType)

def buildRelationshipSubs(params, ind, param, paramType):
    
    if params[ind].fullstr+mark in fullstrTopsubs:
        parentParam, st_id = fullstrTopsubs[params[ind].fullstr+mark]

        if paramType == 'records':
            if isinstance(param, pVar):
                params[ind].add_parent(parentParam)
                params[ind].update_masters(parentParam.masters)
            else:
                param.add_parent(parentParam)
                param.update_masters(parentParam.masters)

        elif paramType == 'cls' or paramType == 'subs':
            if isinstance(param, pVar):
                params[ind].add_parent(parentParam)
                parentParam.add_child(params[ind])
                params[ind].update_masters(parentParam.masters)
            else:
                param.add_parent(parentParam)
                parentParam.add_child(param)
                param.update_masters(parentParam.masters)
        
        elif paramType == 'function' or paramType == 'with':
            for master in parentParam.masters:
                master.add_child(param)
                param.add_parent(master)

        params[ind].update_subsTosubs_ele(parentParam)
    
    else:
        replaceAndFindParentsOfParams(params[ind].prefix, 0, param, paramType)
        replaceAndFindParentsOfParams(params[ind].content, 0, param, paramType)

def replaceAndFindParentsOfParams(params, ind, param, paramType):

    if params[ind].Type == 'variable':
        buildRelationshipVar(params, ind, param, paramType)

    elif params[ind].Type == 'subscript':

        buildRelationshipSubs(params, ind, param, paramType)

    elif params[ind].Type == 'tuple' or params[ind].Type == 'list':
        
        for i in range(len(params[ind].content)):
            replaceAndFindParentsOfParams(params[ind].content, i, param, paramType)

    elif params[ind].Type == 'dict':

        for i in range(len(params[ind].valueContents)):
            replaceAndFindParentsOfParams(params[ind].valueContents, i, param, paramType)

        for i in range(len(params[ind].keyContents)):
            replaceAndFindParentsOfParams(params[ind].keyContents, i, param, paramType)

    elif params[ind].Type == 'set':

        for i in range(len(params[ind].content)):
            replaceAndFindParentsOfParams(params[ind].content, i, param, paramType)

    elif params[ind].Type == 'keyword':
        replaceAndFindParentsOfParams(params[ind].keywordContent, 0, param, paramType)

    elif params[ind].Type == 'binop':
        replaceAndFindParentsOfParams(params[ind].left, 0, param, paramType)      
        replaceAndFindParentsOfParams(params[ind].right, 0, param, paramType)
    
    elif params[ind].Type == 'uop':
        replaceAndFindParentsOfParams(params[ind].operand, 0, param, paramType)

    elif params[ind].Type == 'compare':
        replaceAndFindParentsOfParams(params[ind].left, 0, param, paramType) 
        for i in range(len(params[ind].right)):     
            replaceAndFindParentsOfParams(params[ind].right, i, param, paramType)
    
    elif params[ind].Type == 'lambda':
        if not isinstance(params[ind].body[0], pFunc):
            replaceAndFindParentsOfParams(params[ind].body, 0, param, paramType)
        else:
            for i in range(len(params[ind].body[0].params)):
                replaceAndFindParentsOfParams(params[ind].body[0].params, i, param, 'function') 

def generateFullFuncName(Type, funcName, restrictedVar, suffix):
    
    keyname = ''
    if Type == 'function': keyname += funcName
    elif Type == 'onlyFunc': keyname += funcName
    elif Type == 'restrictedFunc':
        keyname += restrictedVar.name + restrictedVar.restname
    elif Type == 'restrictedOnlyFunc':
        keyname += restrictedVar.name + restrictedVar.restname
    
    return keyname

def handleRestricted_in_varTowith(param, pre, pres, varname):
    if param.Type == 'function':
        param.Type = 'restrictedFunc'

    elif param.Type == 'onlyFunc':
        param.Type == 'restrictedOnlyFunc'
    
    param.add_restricted(pVar(pre))
    fullname = pres[len(pres) - 1]
    restname = ''
    if pre != fullname:
        restname = fullname[len(pre):]

    param.restricted.add_restname(restname) 
    param.restricted.update_varTofunc_ele(parentParam)


def handleRestricted_in_varTofuncst(param, pre, pres, varname):
    
    if param.Type == 'function':
        param.Type = 'restrictedFunc'

    elif param.Type == 'onlyFunc':
        param.Type == 'restrictedOnlyFunc'
    
    parentParam = varTofuncst[varname][0]
    param.add_parent(parentParam)
    parentParam.add_child(param)
    # restricted here is of pVar
    param.add_restricted(pVar(pre))

    fullname = pres[len(pres) - 1]
    restname = ''
    if pre != fullname:
        restname = fullname[len(pre):]

    param.restricted.add_restname(restname) 
    param.restricted.update_varTofunc_ele(parentParam)

def handleRestricted_in_clsInstanceToParam(param, varname, pre, pres):
    
    if param.Type == 'function':
        param.Type = 'restrictedFunc'

    elif param.Type == 'onlyFunc':
        param.Type == 'restrictedOnlyFunc'
    
    parentParam = clsInstanceToParam[varname][0]
    
    for master in parentParam.masters:
        master.add_child(param)
        param.add_parent(master)

    param.add_restricted(pVar(pre))

    # restricted here may be not of pVar
    param.restricted.update_varTocls_ele(parentParam)

    fullname = pres[len(pres) - 1]
    restname = ''
    if pre != fullname:
        restname = fullname[len(pre):]

    param.restricted.add_restname(restname)

def handleRestricted_in_records(param, pre, pres, varname):
    
    fullname = pres[len(pres) - 1]
    restname = ''
    if pre != fullname:
        restname = fullname[len(pre):]

    records_copy, st_id = copy.copy(records[varname])
    param.add_restricted(records_copy)
    param.restricted.add_restname(restname)

def handleRestricted(param):

    find = False
    varTofuncst_id = -1
    records_id = -1
    clsInstanceToParam_id = -1
    with_id = -1

    pres = constitutePres(param.funcName)

    for pre in pres[::-1]:
        for mark_ in [mark, markGlobal]:
            
            varname = pre+mark_
            if varname in varTofuncst:
                varTofuncst_id = varTofuncst[varname][-1]

            elif varname in records:
                records_id = records[varname][-1]

            elif varname in clsInstanceToParam:
                clsInstanceToParam_id = clsInstanceToParam[varname][-1]

            elif varname in varTowith:
                with_id = varTowith[varname][-1]

            if records_id != -1 or varTofuncst_id != -1 or \
                clsInstanceToParam_id != -1 or with_id != -1:
                find = True 

            maxi = max4(records_id, varTofuncst_id, clsInstanceToParam_id, with_id)
            
            if find:
                if maxi == records_id:
                    handleRestricted_in_records(param, pre, pres, varname)
                    
                elif maxi == varTofuncst_id:
                    handleRestricted_in_varTofuncst(param, pre, pres, varname)
                
                elif maxi == clsInstanceToParam_id:
                    handleRestricted_in_clsInstanceToParam(param, varname, pre, pres)
                
                break
        if find:
            break

    # return param.Type, param.restrictedVar

def handle_restname_name(varobject,
                         pres,
                         pre):

    varobject.add_name(pre)
    fullname = pres[len(pres) - 1]
    restname = fullname[len(pre):]
    varobject.add_restname(restname)

def buildPres(varobject):

    if isinstance(varobject, pSubs):
        varobject = varobject.var

    preslist = varobject.name.split('.')
    pre = ''
    pres = []
    for i in range(len(preslist)):
        ele = preslist[i]
        if pre == '':
            pre = ele 
        else:
            pre += '.' + ele 
        pres.append(pre)
    return pres

def findin_varTofuncst(varobject, 
                        param, 
                        pres, 
                        pre,
                        mark_,
                        paramType):
    
    pfunc, st_id = varTofuncst[pre+mark_]
    if pres:
        handle_restname_name(varobject,
                            pres,
                            pre)

    varobject.update_varTofunc_ele(pfunc)
    if paramType != 'subs-content' and paramType != 'subs-prefix':
        param.add_varobject(varobject)
    
    if paramType == 'cls' or paramType == 'subs-prefix' \
        or paramType == 'subs-content':
        param.add_master(pfunc)
        pfunc.add_adjunct(param)
    
    elif paramType == 'function':

        param.add_parent(pfunc)
        pfunc.add_child(param)

def findin_varTowith(varobject, 
                    param, 
                    pres, 
                    pre,
                    mark_,
                    paramType):

    pwith, withitem_id, st_id = varTowith[pre+mark_]
    if pres:
        handle_restname_name(varobject,
                            pres,
                            pre)
    if paramType != 'subs-content' and paramType != 'subs-prefix':
        param.add_varobject(varobject)
    varobject.update_varTowith_ele((pwith, withitem_id))

def findin_clsInstanceToParam(key, 
                              pre, 
                              pres,
                              param,
                              varobject,
                              paramType):

    

    paramcls, st_id = clsInstanceToParam[key]

    if pres:
        handle_restname_name(varobject,
                            pres,
                            pre)

    if paramType != 'subs-content' and paramType != 'subs-prefix':
        param.add_varobject(varobject)
    
    varobject.update_varTocls_ele(paramcls)

    if paramType == 'cls'\
        or paramType == 'subs-prefix'\
        or paramType == 'subs-content':
        
        param.add_parent(paramcls)
        paramcls.add_child(param)
        param.update_masters(param.masters)
    
    elif paramType == 'function':
        
        for master in paramcls.masters:
            param.add_parent(master)
            master.add_child(param)
    
def findin_records(varobjects,
                   ind,
                   param,
                   pres,
                   pre,
                   mark_,
                   paramType):

    record_param, st_id = records[pre+mark_]
    record_param = copy.copy(record_param)
    
    fullname = pres[len(pres)-1] if pres else ''
    restname = fullname[len(pre):] if pres else ''
    varobjects[ind] = record_param
    varobjects[ind].add_restname(record_param.restname+restname)
    
    if paramType != 'subs-content' and paramType != 'subs-prefix':
        param.add_varobject(varobjects[ind])

    if paramType == 'cls' or paramType == 'subs-content' \
        or paramType == 'subs-prefix':
        for parent in record_param.parents:
            parent.add_child(param)
        
        for master in record_param.masters:
            param.add_master(master)

        if record_param.shouldBeAdjunct:
            for master in record_param.masters:
                master.add_adjunct(param)
        
    elif paramType == 'function':
        for master in record_param.masters:
            param.add_parent(master)
            master.add_child(param) 

def FindParentsOfVarobjectsIfNotPolysyllabic(param, varobjects, ind, paramType):
    find = False
    varTofuncst_id = -1
    clsInstanceToParam_id = -1
    records_id = -1
    with_id = -1

    pre = varobjects[ind].name

    for mark_ in [mark, markGlobal]:    
            
        if pre+mark_ in varTofuncst:
            varTofuncst_id = varTofuncst[pre+mark_][-1]

        if pre+mark_ in clsInstanceToParam:
            clsInstanceToParam_id = clsInstanceToParam[pre+mark_][-1]

        if pre+mark_ in records:
            records_id = records[pre+mark_][-1]
        
        if pre+mark_ in varTowith:
            with_id = varTowith[pre+mark_][-1]

        if varTofuncst_id != -1 or clsInstanceToParam_id != -1 or \
            records_id != -1 or with_id != -1:
            find = True
        
        maxi = max4(varTofuncst_id, clsInstanceToParam_id, records_id, with_id)

        if find:
            if maxi == varTofuncst_id:
                findin_varTofuncst(varobjects[ind],
                                param, 
                                None, 
                                pre,
                                mark_,
                                paramType)

            elif maxi == clsInstanceToParam_id:
                findin_clsInstanceToParam(pre+mark_,
                                        pre,
                                        None,
                                        param,
                                        varobjects[ind],
                                        paramType)
            
            elif maxi == records_id:
                findin_records(varobjects,
                               ind,
                                param,
                                None,
                                pre,
                                mark_,
                                paramType)
            
            elif maxi == with_id:
                findin_varTowith(varobjects[ind],
                                param, 
                                None, 
                                pre,
                                mark_,
                                paramType)

            break

def FindParentsOfVarobjectsIfPolysyllabic(param, varobjects, ind, paramType):
    
    pres = buildPres(varobjects[ind])
    find = False
    varTofuncst_id = -1
    clsInstanceToParam_id = -1
    records_id = -1
    with_id = -1

    for pre in pres[:-1][::-1]:
        for mark_ in [mark, markGlobal]:    
            
            if pre+mark_ in varTofuncst:
                varTofuncst_id = varTofuncst[pre+mark_][-1]

            if pre+mark_ in clsInstanceToParam:
                clsInstanceToParam_id = clsInstanceToParam[pre+mark_][-1]

            if pre+mark_ in records:
                records_id = records[pre+mark_][-1]
            
            if pre+mark_ in varTowith:
                with_id = varTowith[pre+mark_][-1]
            
            if varTofuncst_id != -1 or clsInstanceToParam_id != -1 or \
                records_id != -1 or with_id != -1:
                find = True
            
            maxi = max4(varTofuncst_id, clsInstanceToParam_id, records_id, with_id)

            if find:
                if maxi == varTofuncst_id:
                    findin_varTofuncst(varobjects[ind], 
                                    param, 
                                    pres, 
                                    pre,
                                    mark_,
                                    paramType)

                elif maxi == clsInstanceToParam_id:
                    findin_clsInstanceToParam(pre+mark_,
                                            pre,
                                            pres,
                                            param,
                                            varobjects[ind],
                                            paramType)
                
                elif maxi == records_id:
                    findin_records(varobjects,
                                    ind, 
                                    param,
                                    pres,
                                    pre,
                                    mark_,
                                    paramType)
                
                elif maxi == with_id:
                    findin_varTowith(varobjects[ind], 
                                    param, 
                                    pres, 
                                    pre,
                                    mark_,
                                    paramType)

                break
        if find: 
            break

    if not find:
        param.add_varobject(varobjects[ind])

    # return param_

def FindParentsOfVarobjects(param, varobjects, paramType):
    
    '''
    varnames which are on the leftside of a function statment cannnot be randomly generated 
    during generation period in some special situation, such as:

    a = fun()
    a.b = fun2()

    Then during generation, if we treate a.b as a whole varname and generate a random variable 
    name as a substitution for a.b, then the relationship between a and a.b will be broken
    To make things simpler, let me show an example after generation period:

    A1BXd = fun()
    Xod1X = fun2()

    This generated function is wrong, isn't it?
    The expected program should be 

    A1BXd = fun()
    A1BXd.b = fun2()

    That's why I write out the below code snippet to handle this special situation

    '''

    # varobjects = []
    if varobjects:
        for ind in range(len(varobjects)):
            
            name = varobjects[ind].name if isinstance(varobjects[ind], pVar) \
                else varobjects[ind].prefix[0].name

            if '.' not in name:
                if paramType == 'subs-prefix' or paramType == 'subs-content':
                    FindParentsOfVarobjectsIfNotPolysyllabic(param, varobjects, ind, paramType)
                else:
                    param.add_varobject(varobjects[ind])
            else:
                FindParentsOfVarobjectsIfPolysyllabic(param, varobjects, ind, paramType)
    # param.update_varobjectsList()
    

def handleRepetition(lengh, params_, params, param_, param):

    for parent in param.parents:
        parent.children.remove(param)

    for i in range(lengh):    

        if params_[i].Type == 'const' and params[i].Type == 'const':
            params_[i].add_consts_ele(params[i].const)

        elif params_[i].Type == 'keyword' and params[i].Type == 'keyword'\
            and params_[i].keywordStr == params[i].keywordStr:
            find = False 

            for kc in params_[i].keywordContent:
                
                if kc.Type == 'const' and params[i].keywordContent[0].Type == 'const':
                    kc.consts.add(params[i].keywordContent[0].const)
                    find = True
            
            if not find:
                params_[i].add_keywordContent(params[i].keywordContent[0])
                 
                     
        elif params_[i].Type == 'variable' and params[i].Type == 'variable':
            # params[i],varTofunc only contains one element

            if params[i].varTofunc:
                parentParam = list(params[i].varTofunc)[0]

                findParentParam = False
                for ele in params_[i].varTofunc:
                    if ele == parentParam:
                        findParentParam = True
                        break

                if not findParentParam:
                    params_[i].update_varTofunc_set(params[i].varTofunc)
                    param_.add_parent(parentParam)
                    parentParam.add_child(param_)
        

def recordNewStatementIfMetBefore(param):
    
    funcName = param.funcName
    params = param.params
    param_ = funcNameTopFunc[funcName]
    params_ = param_.params
    len1 = len(params_)
    len2 = len(params)

    if len1 == len2:
        handleRepetition(len1, params_, params, param_, param)
        return param_

    return param

def recordNewStatementIfNotMetBefore(param):

    params = param.params
    funcName = param.funcName
    cnt = 0
    for param_ in params:
        
        if param_.Type == 'const':
            param_.consts.add(param_.const)
        elif param_.Type == 'keyword' and param_.keywordContent[-1].Type == 'const':
            param_.keywordContent[-1].consts.add(param_.keywordContent[-1].const)
        
        cnt += 1

    funcNameTopFunc[funcName] = param
    ingredient.append(param)

def recordNewStatement(param):
    
    if param.funcName in funcNameTopFunc: 
        param_ = recordNewStatementIfMetBefore(param)  # here !!!
        return param_, True
        
    else: 
        recordNewStatementIfNotMetBefore(param)
        return param, False

def updateVarTofuncst(varobjects, param, param_funcName_in_funcNameTopFunc):

    global st_id 
    if param.Type == 'restrictedOnlyFunc':
        
        if param_funcName_in_funcNameTopFunc:
            varTofuncst[param.restrictedVar.name+param.restrictedVar.restname+mark] \
                = (funcNameTopFunc[param.funcName], st_id)
        else:
            varTofuncst[param.restrictedVar.name+param.restrictedVar.restname+mark] \
                = (param, st_id)

    if varobjects:
        # cnt = 0
        # for varobject in varobjects:
        
        varname = varobjects[0].name

        if not param_funcName_in_funcNameTopFunc:
            varTofuncst[varname+mark] = (param, st_id)
        else: 
            varTofuncst[varname+mark] = \
                (funcNameTopFunc[param.funcName], st_id)

            # cnt += 1

# def meetTaboo(param):
#     if isinstance(param, pFunc) and param.funcName in funcDef:
#         return True
    
#     if isinstance(param, pFunc):
#         for tb in taboo:
#             if tb in param.funcName:
#                 return True
    
#     return False

def handleSurround(param):
    if param.surround:
        param.surround.add_body(param) 

def handlefuncNameandSuffix(param, varobjects):
    
    fullname = generateFullFuncName(param.Type, 
                                    param.funcName, 
                                    param.restricted, 
                                    param.suffix)
    numberOfparams = len(param.params)
    numberOfvarnames = len(varobjects) if varobjects else 0
    surround_id = withid if param.surround else 0
    hasLambda = False
    lambda_id = 0
    for ele in param.params:
        if isinstance(ele, pLambda):
            hasLambda = True
    if hasLambda:
        if fullname in funcTolambda:
            lambda_id = funcTolambda[fullname] 
            funcTolambda[fullname] = lambda_id + 1
        else:
            funcTolambda[fullname] = 2
            lambda_id = 1

    fullnameSuffix = '_' + str(numberOfparams) + '_' + str(numberOfvarnames) +\
                        '_' + str(surround_id) + '_' + str(lambda_id)
    param.add_funcName(fullname+fullnameSuffix)
    param.add_funcNameSuffix(fullnameSuffix)

def handle_pSubs_onTheLeft(param, varobjects):

    if isinstance(param, pFunc):
        name = varNameGenerator(varnamesRead)
        pvar = pVar(name)
        dealWithStatement(param, varobjects=[pvar])
        param = copy.deepcopy(pvar)

    if len(varobjects) > 1:
        raise Exception(Cyan(\
            'varobjects shouldn\'t have more than 1 varobject' ))
    
    fullstrTopsubs[varobjects[0].fullstr+mark] = (param, st_id)

    paramlist = [param]
    param.add_varobject(varobjects[0])
    replaceAndFindParentsOfParams(paramlist, 0, param, 'subs')
    if isinstance(param, pVar):
        param = paramlist[0]
        if not param.varobjects:
            param.add_varobject(varobjects[0])

    prefixlist = [varobjects[0].prefix[0]]
    FindParentsOfVarobjects(param, prefixlist, 'subs-prefix')
    varobjects[0].prefix[0] = prefixlist[0]
    
    if isinstance(varobjects[0].content[0], pVar):
        contentlist = [varobjects[0].content[0]]
        FindParentsOfVarobjects(param, contentlist, 'subs-content')
        varobjects[0].content[0] = contentlist[0]
    
def handle_pVar_onTheLeft(param, varobjects):

    if isinstance(param, pFunc):
        name = varNameGenerator(varnamesRead)
        pvar = pVar(name)
        dealWithStatement(param, varobjects=[pvar])
        param = copy.deepcopy(pvar)

    if len(varobjects) > 1:
        raise Exception(Cyan(\
            'varobjects shouldn\'t have more than 1 varobject' ))

    clsInstanceToParam[varobjects[0].name+mark] = (param, st_id)

    paramlist = [param]
    replaceAndFindParentsOfParams(paramlist, 0, param, 'cls')
    if isinstance(param, pVar):
        param = paramlist[0]
    FindParentsOfVarobjects(param, varobjects, 'cls')

def decompose_multi_varobjects(len_varobjects, param, varobjects):

    name = varNameGenerator(varnamesRead)
    pvar = pVar(name)
    dealWithStatement(param, varobjects=[pvar])

    if isinstance(param, pFunc):
        for i in range(len_varobjects):
            varobject = varobjects[i]
            psubs = pSubs()
            psubs.add_prefix(copy.deepcopy(pvar))
            psubs.add_content(pNumber(i))
            psubs.add_fullstr(name + '[' + str(i) + ']')
            dealWithStatement(psubs, [varobject])
    
    else:
        for i in range(len_varobjects):
            varobject = varobjects[i]
            dealWithStatement(param, [varobject])

def handle_pFunc(param, varobjects=None):

    '''
        handle the closure situation like
        a = fun(2) /*a is actually a closure*/
        b = a(1)

        restrictedFunction may be closure
        e.g. a = fun() /*a is closure*/
            b = a(1)
            pfunc wrapping a(1) is 
            restrictedFunction when passing
            but is actually closure
    '''
    handleRestricted(param)
    
    handlefuncNameandSuffix(param, varobjects)

    if varobjects:
        FindParentsOfVarobjects(param, varobjects, 'function')

    for i in range(len(param.params)):
        replaceAndFindParentsOfParams(param.params, i, param, 'function')    

    handleSurround(param)

    param_, \
        param_funcName_in_funcNameTopFunc \
            = recordNewStatement(param) 

    updateVarTofuncst(varobjects, param_, param_funcName_in_funcNameTopFunc)

def handle_pWith(param, varobjects):
    
    if varobjects:
        raise Exception(Cyan(\
            'varobjects should be None when param is pWith instance'))

    cnt = 0
    for item, asitem in param.withitems:
        if not item.varTofunc:
            paramlist = [item]
            replaceAndFindParentsOfParams(paramlist, 0, param, 'with')
            item = paramlist[0]

        if asitem: varTowith[asitem.name+mark] = (param, cnt, st_id)
        else: varTowith[item.name+mark] = (param, cnt, st_id)
        cnt += 1
    param.set_id(withid)
    ingredient.append(param)

def dealWithStatement(param, varobjects=None):
    
    if varobjects:
        len_varobjects = len(varobjects)
        if len_varobjects > 1:
            decompose_multi_varobjects(len_varobjects, param, varobjects)
            return 

    global st_id, withid
    st_id += 1
    withid += 1

    if isinstance(param, pWith):
        handle_pWith(param, varobjects)

    elif varobjects == None:
        handle_pFunc(param)

    elif isinstance(varobjects[0], pSubs): 
        handle_pSubs_onTheLeft(param, varobjects)

    elif isinstance(varobjects[0], pVar) and \
            '.' in varobjects[0].name:

        handle_pVar_onTheLeft(param, varobjects)

    elif isinstance(param, pFunc):
        handle_pFunc(param, varobjects)

    else:

        if len(varobjects) > 1:
            raise Exception(Cyan(\
                'varobjects shouldn\'t have more than 1 varobject' ))
 
        if not isinstance(param, pNumber) and \
            not isinstance(param, pConst):
            
            paramlist = [param]
            replaceAndFindParentsOfParams(paramlist, 0, param, 'records')
            
            if isinstance(param, pVar):
                param = paramlist[0]

        records[varobjects[0].name+mark] = (param, st_id)