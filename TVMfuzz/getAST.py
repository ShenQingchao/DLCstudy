import ast
import os
from TVMfuzz.colors import *
from TVMfuzz.analyzeSyntax import dealWithStatement, dealWithImport
from TVMfuzz.ASTutils import *
import random 
from TVMfuzz.elements import *
import copy

class NodeTransformer(ast.NodeTransformer):                

    def visit_ClassDef(self, node):
        helperFuncDef[node.name] = node
        funcDefs.append(node)

    def visit_FunctionDef(self, FunctionDef, func=None):

        copy = False
        if FunctionDef.args.args:
            copy = True
        else:
            for ele in FunctionDef.body:
                if isinstance(ele, ast.Return):
                    copy = True
                    break
        if FunctionDef.name not in forbiddenFuncDef:
            helperFuncDef[FunctionDef.name] = FunctionDef
            tp = ()
            if func and func in helperStatDef_local:
                tp = helperStatDef_local[func]
            funcDefParents[FunctionDef] = tuple(helperStatDef_global) + \
                                          tuple(funcDefs) + \
                                          tp            
            funcDefs.append(FunctionDef)
        if copy:
            functionDefNames.add(FunctionDef.name)

        elif not random.randint(0, 14):

            funcID = int(os.getenv('funcID'))
            funcID += 1
            os.environ['isFunc'] = 'True'
            os.environ['funcID'] = str(funcID)
            function_body = FunctionDef.body
            for function_element in function_body:

                if isinstance(function_element, ast.Assign):
                    AssignNode(function_element, func=FunctionDef)
                elif isinstance(function_element, ast.Expr):
                    self.visit_Expr(function_element)
                elif isinstance(function_element, ast.With):
                    self.visit_With(function_element, func=FunctionDef)
                elif isinstance(function_element, ast.FunctionDef):
                    self.visit_FunctionDef(function_element, func=FunctionDef)
                elif isinstance(function_element, ast.ClassDef):
                    self.visit_ClassDef(function_element)

    def visit_WithItems(self, With, surround=None, indent=0):

        items = With.items
        param = pWith()
        for item in items:

            param1 = None
            param2 = None
            if hasattr(item, 'context_expr'):
                param1 = recognizeMultiAssignment(item.context_expr, indent=indent)
                if isinstance(param1, pFunc):
                    randomname = varNameGenerator(varnamesRead)
                    pfunc = pFunc(funcName=param1.funcName,
                                params=param1.params,
                                suffix=param1.suffix, 
                                Type='function',
                                restricted=param1.restricted,
                                indent=indent)
                    if pfunc.restricted:
                        pfunc.add_Type('restrictedFunc')
                    pfunc.add_surround(surround)
                    pfunc.add_child(param)
                    vparam = pVar(randomname)
                    param1 = copy.deepcopy(vparam)
                    dealWithStatement(param=pfunc, varobjects=[vparam])
                    param.add_parent(pfunc)
                    param1.update_varTofunc_ele(pfunc)

                elif isinstance(param1, pVar):
                    pass

                else:
                    raise Exception(Cyan('with context_expr\'s type is not handled: ' \
                            + str(param1)))
            if item.optional_vars:
                param2 = recognizeMultiAssignment(item.optional_vars, indent=indent)
            param.add_withitem((param1, param2))
            param.add_surround(surround)
            param.add_indent(indent)

        return param

    def visit_WithBody(self, With, param, indent, func):
        for ele in With.body:
            if isinstance(ele, ast.Expr):
                self.visit_Expr(ele, param, indent+1)
            elif isinstance(ele, ast.With):
                self.visit_With(ele, param, indent+1)
            elif isinstance(ele, ast.Assign):
                AssignNode(ele, param, indent+1, func=func)

    def visit_With(self, With, surround=None, indent=0, func=None):
        param = self.visit_WithItems(With, surround=surround, indent=indent)
        dealWithStatement(param=param)
        self.visit_WithBody(With, param, indent, func)

    def visit_Import(self, Import):
        for name in Import.names:
            if hasattr(name, 'asname') and name.asname:
                dealWithImport('import', 
                               importWhat=name.name, 
                               asWhat=name.asname)
            else:
                dealWithImport('import', 
                                importWhat=name.name)
    
    def visit_ImportFrom(self, ImportFrom):
        for name in ImportFrom.names:
            if hasattr(name, 'asname') and name.asname:
                dealWithImport('fromImport', 
                               fromWhat=ImportFrom.module,
                               importWhat=name.name, 
                               asWhat=name.asname)
            else:
                dealWithImport('fromImport', 
                               fromWhat=ImportFrom.module,
                               importWhat=name.name)
    
    def visit_Assign(self, Assign):
        AssignNode(Assign)
    
    def visit_Expr(self, Expr, surround=None, indent=0):
        if isinstance(Expr.value, ast.Call):
            param = recognizeMultiAssignment(value=Expr.value, 
                                             indent=indent,
                                             surround=surround)
            if not isinstance(param, pFunc):
                raise Exception('Type error! Expect pFunc but receive ' + str(type(param)))
            if not param.restricted:
                dealWithStatement(param=param)
            else:
                dealWithStatement(param=param)
    
    def visit_If(self, node):
        pass

    def visit_While(self, node):
        pass
    
    def visit_For(self, node):
        pass
