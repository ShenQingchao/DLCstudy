
'''ASTutils.py'''
varnamesRead = set()
mutable = True

'''generation.py'''

funcPool = {}
# funcNumber = {}
varPool = set()
withPool = set()
clsPool = {}
subsPool = {}
lazy = []
restAdjuncts = []
# recordedFunc = []

'''analyzeSyntax'''
importSet = set()
funcNameTopFunc = {}
# funcNames = set()
constants = set()
records = {}

id = 0

varTofuncst = {}
# funcDef = set()

varTowith = {}

taboo = ['gpu']
ingredient = []

clsInstanceToParam = {}
fullstrTopsubs = {}


functionDefNames = set(['relay.multiply',
                        'relay.divide',
                        'relay.add',
                        'relay.subtract',
                        'relay.less',
                        'relay.greater',
                        'relay.less_equal',
                        'relay.greater_equal',
                        'relay.equal',
                        'relay.not_equal'])

funcTolambda = {}

'''getAST'''

helperFuncDef = {}
# helperStatDef = {}
# FuncDef_parent = set()
helperStatDef_global = []
helperStatDef_local = {}
funcDefParents = {}
forbiddenFuncDef = ['random_bsr_matrix']
funcDefs = []


'''autorun'''

message = {}
message['0.7'] = [
    '''
    Traceback (most recent call last):
    File "/home/lisa/TVMfuzz/buggyFile/1.py", line 7, in <module>
        xqvpP=tvm.IRModule.from_expr(pDL7X)
    File "/home/lisa/tvm-0.7/python/tvm/ir/module.py", line 237, in from_expr
        return _ffi_api.Module_FromExpr(expr, funcs, defs)
    File "/home/lisa/tvm-0.7/python/tvm/_ffi/_ctypes/packed_func.py", line 237, in __call__
        raise get_last_ffi_error()
    tvm._ffi.base.TVMError: Traceback (most recent call last):
    [bt] (8) /home/lisa/tvm-0.7/build/libtvm.so(tvm::RelayExpr tvm::relay::TypeInferencer::Resolver::AttachCheckedType<tvm::relay::FunctionNode>(tvm::relay::FunctionNode const*)+0x1be) [0x7f52df55d8ee]
    [bt] (7) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::ExprMutator::VisitExpr_(tvm::relay::FunctionNode const*)+0x382) [0x7f52df63a8f2]
    [bt] (6) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::ExprMutator::VisitExpr(tvm::RelayExpr const&)+0x96) [0x7f52df63ce06]
    [bt] (5) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>::VisitExpr(tvm::RelayExpr const&)+0x76) [0x7f52df642ce6]
    [bt] (4) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>::InitVTable()::{lambda(tvm::runtime::ObjectRef const&, tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>*)#3}::_FUN(tvm::runtime::ObjectRef const&, tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>*)+0x2c) [0x7f52df4e139c]
    [bt] (3) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeInferencer::Resolver::VisitExpr_(tvm::relay::VarNode const*)+0x87) [0x7f52df5604f7]
    [bt] (2) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeInferencer::Resolver::VisitVar(tvm::relay::Var const&)+0xe2) [0x7f52df5602c2]
    [bt] (1) /home/lisa/tvm-0.7/build/libtvm.so(tvm::RelayExpr tvm::relay::TypeInferencer::Resolver::AttachCheckedType<tvm::relay::VarNode>(tvm::relay::VarNode const*)+0x1ab) [0x7f52df55ad2b]
    [bt] (0) /home/lisa/tvm-0.7/build/libtvm.so(+0x27a2988) [0x7f52df552988]
    File "/home/lisa/tvm-0.7/src/relay/transforms/type_infer.cc", line 617
    TVMError: Check failed: checked_type.as<IncompleteTypeNode>() == nullptr: Cannot resolve type of Var(x) at (nullptr)
    ''',

    '''
    [14:44:23] /home/lisa/tvm-0.7/src/printer/doc.cc:55: text node: ' an internal invariant was violated while typechecking your program [14:44:23] /home/lisa/tvm-0.7/src/relay/op/tensor/transform.cc:2367: Check failed: data->shape.size() != 0 (0 vs. 0) : Input shape cannot be empty
    Stack trace:
    [bt] (0) /home/lisa/tvm-0.7/build/libtvm.so(+0x25245e8) [0x7f8062d885e8]
    [bt] (1) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::SplitRel(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)+0x458) [0x7f8062da0a38]
    [bt] (2) /home/lisa/tvm-0.7/build/libtvm.so(tvm::runtime::TypedPackedFunc<bool (tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>::AssignTypedLambda<bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>(bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&))::{lambda(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*)#1}::operator()(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*) const+0x518) [0x7f806276eeb8]
    [bt] (3) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeSolver::Solve()+0x4cd) [0x7f8062e8978d]
    [bt] (4) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeInferencer::Infer(tvm::RelayExpr)+0x5c) [0x7f8063007bec]
    [bt] (5) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::InferType(tvm::relay::Function const&, tvm::IRModule const&, tvm::GlobalVar const&)+0x3a2) [0x7f8063008972]
    [bt] (6) /home/lisa/tvm-0.7/build/libtvm.so(tvm::RunTypeCheck(tvm::IRModule const&, tvm::GlobalVar const&, tvm::relay::Function)+0x5f6) [0x7f80626ee7e6]
    [bt] (7) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModuleNode::Add(tvm::GlobalVar const&, tvm::BaseFunc const&, bool)+0xd7) [0x7f80626eee37]
    [bt] (8) /home/lisa/tvm-0.7/build/libtvm.so(+0x1e8f091) [0x7f80626f3091]

    ; ' should not has tab or newline.
    Traceback (most recent call last):
        File "/home/lisa/TVMfuzz/buggyFile/5.py", line 18, in <module>
        EeNPI['main']=QLiMS
        File "/home/lisa/tvm-0.7/python/tvm/ir/module.py", line 75, in __setitem__
        return self._add(var, val)
        File "/home/lisa/tvm-0.7/python/tvm/ir/module.py", line 84, in _add
        _ffi_api.Module_Add(self, var, val, update)
        File "/home/lisa/tvm-0.7/python/tvm/_ffi/_ctypes/packed_func.py", line 237, in __call__
        raise get_last_ffi_error()
        tvm._ffi.base.TVMError: Traceback (most recent call last):
        [bt] (8) /home/lisa/tvm-0.7/build/libtvm.so(TVMFuncCall+0x63) [0x7f80631dcd63]
        [bt] (7) /home/lisa/tvm-0.7/build/libtvm.so(+0x1e8fed8) [0x7f80626f3ed8]
        [bt] (6) /home/lisa/tvm-0.7/build/libtvm.so(+0x1e8f091) [0x7f80626f3091]
        [bt] (5) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModuleNode::Add(tvm::GlobalVar const&, tvm::BaseFunc const&, bool)+0xd7) [0x7f80626eee37]
        [bt] (4) /home/lisa/tvm-0.7/build/libtvm.so(tvm::RunTypeCheck(tvm::IRModule const&, tvm::GlobalVar const&, tvm::relay::Function)+0x5f6) [0x7f80626ee7e6]
        [bt] (3) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::InferType(tvm::relay::Function const&, tvm::IRModule const&, tvm::GlobalVar const&)+0x3a2) [0x7f8063008972]
        [bt] (2) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeInferencer::Infer(tvm::RelayExpr)+0x78) [0x7f8063007c08]
        [bt] (1) /home/lisa/tvm-0.7/build/libtvm.so(tvm::ErrorReporter::RenderErrors(tvm::IRModule const&, bool)+0x2098) [0x7f80626da288]
        [bt] (0) /home/lisa/tvm-0.7/build/libtvm.so(dmlc::LogMessageFatal::~LogMessageFatal()+0x80) [0x7f80625ddb60]
        [bt] (8) /home/lisa/tvm-0.7/build/libtvm.so(+0x1e8f091) [0x7f80626f3091]
        [bt] (7) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModuleNode::Add(tvm::GlobalVar const&, tvm::BaseFunc const&, bool)+0xd7) [0x7f80626eee37]
        [bt] (6) /home/lisa/tvm-0.7/build/libtvm.so(tvm::RunTypeCheck(tvm::IRModule const&, tvm::GlobalVar const&, tvm::relay::Function)+0x5f6) [0x7f80626ee7e6]
        [bt] (5) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::InferType(tvm::relay::Function const&, tvm::IRModule const&, tvm::GlobalVar const&)+0x3a2) [0x7f8063008972]
        [bt] (4) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeInferencer::Infer(tvm::RelayExpr)+0x5c) [0x7f8063007bec]
        [bt] (3) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeSolver::Solve()+0x4cd) [0x7f8062e8978d]
        [bt] (2) /home/lisa/tvm-0.7/build/libtvm.so(tvm::runtime::TypedPackedFunc<bool (tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>::AssignTypedLambda<bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>(bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&))::{lambda(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*)#1}::operator()(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*) const+0x518) [0x7f806276eeb8]
        [bt] (1) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::SplitRel(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)+0x458) [0x7f8062da0a38]
        [bt] (0) /home/lisa/tvm-0.7/build/libtvm.so(+0x25245e8) [0x7f8062d885e8]
        File "/home/lisa/tvm-0.7/src/ir/error.cc", line 132
        TVMError:
        Error(s) have occurred. The program has been annotated with them:

        In `main`:
        #[version = "0.0.5"]
        fn (%y2: uint64) {
        split(%y2, indices_or_sections=3) an internal invariant was violated while typechecking your program [14:44:23] /home/lisa/tvm-0.7/src/relay/op/tensor/transform.cc:2367: Check failed: data->shape.size() != 0 (0 vs. 0) : Input shape cannot be empty
        ;
    }
    ''',

    '''
    Traceback (most recent call last):
    File "/home/lisa/TVMfuzz/buggyFile/6.py", line 155, in <module>
        rdg9G[fAhiQ]=su5yc
    File "/home/lisa/tvm-0.7/python/tvm/ir/module.py", line 75, in __setitem__
        return self._add(var, val)
    File "/home/lisa/tvm-0.7/python/tvm/ir/module.py", line 89, in _add
        _ffi_api.Module_AddDef(self, var, val, update)
    File "/home/lisa/tvm-0.7/python/tvm/_ffi/_ctypes/packed_func.py", line 237, in __call__
        raise get_last_ffi_error()
    tvm._ffi.base.TVMError: Traceback (most recent call last):
    [bt] (4) /home/lisa/tvm-0.7/build/libtvm.so(TVMFuncCall+0x63) [0x7fb9d92b6d63]
    [bt] (3) /home/lisa/tvm-0.7/build/libtvm.so(tvm::runtime::TypedPackedFunc<void (tvm::IRModule, tvm::GlobalTypeVar const&, tvm::TypeData const&, bool)>::AssignTypedLambda<tvm::runtime::Registry::set_body_method<tvm::IRModule, tvm::IRModuleNode, void, tvm::GlobalTypeVar const&, tvm::TypeData const&, bool, void>(void (tvm::IRModuleNode::*)(tvm::GlobalTypeVar const&, tvm::TypeData const&, bool))::{lambda(tvm::IRModule, tvm::GlobalTypeVar const&, tvm::TypeData const&, bool)#1}>(tvm::runtime::Registry::set_body_method<tvm::IRModule, tvm::IRModuleNode, void, tvm::GlobalTypeVar const&, tvm::TypeData const&, bool, void>(void (tvm::IRModuleNode::*)(tvm::GlobalTypeVar const&, tvm::TypeData const&, bool))::{lambda(tvm::IRModule, tvm::GlobalTypeVar const&, tvm::TypeData const&, bool)#1})::{lambda(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*)#1}::operator()(tvm::runtime::TVMArgs const, tvm::runtime::TVMRetValue) const+0x2a4) [0x7fb9d87d9c34]
    [bt] (2) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModuleNode::AddTypeDef(tvm::GlobalTypeVar const&, tvm::TypeData const&, bool)+0x2b) [0x7fb9d87cc6cb]
    [bt] (1) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModuleNode::AddTypeDefUnchecked(tvm::GlobalTypeVar const&, tvm::TypeData const&, bool)+0x1f5) [0x7fb9d87cc445]
    [bt] (0) /home/lisa/tvm-0.7/build/libtvm.so(+0x1e885b8) [0x7fb9d87c65b8]
    File "/home/lisa/tvm-0.7/src/ir/module.cc", line 260
    TVMError: Check failed: global_type_var_map_.count(var->name_hint) == 0: Duplicate global type definition name gtv
    ''',

    '''
    [09:03:12] /home/lisa/tvm-0.7/src/printer/doc.cc:55: text node: ' an internal invariant was violated while typechecking your program [09:03:12] /home/lisa/tvm-0.7/src/relay/op/tensor/transform.cc:1623: Check failed: reporter->Assert(seq_lengths->shape[0] == data->shape[batch_axis]): For reverse_sequnece seq_lengths size should match with dimension of batch axis, but got dimension of batch_axis = 4, and seq_length size = 5
    Stack trace:
    [bt] (0) /home/lisa/tvm-0.7/build/libtvm.so(+0x25245e8) [0x7f428f6b95e8]
    [bt] (1) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::ReverseSequenceRel(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)+0x59d) [0x7f428f6c46cd]
    [bt] (2) /home/lisa/tvm-0.7/build/libtvm.so(tvm::runtime::TypedPackedFunc<bool (tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>::AssignTypedLambda<bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>(bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&))::{lambda(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*)#1}::operator()(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*) const+0x518) [0x7f428f09feb8]
    [bt] (3) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeSolver::Solve()+0x4cd) [0x7f428f7ba78d]
    [bt] (4) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeInferencer::Infer(tvm::RelayExpr)+0x5c) [0x7f428f938bec]
    [bt] (5) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::InferType(tvm::relay::Function const&, tvm::IRModule const&, tvm::GlobalVar const&)+0x3a2) [0x7f428f939972]
    [bt] (6) /home/lisa/tvm-0.7/build/libtvm.so(tvm::RunTypeCheck(tvm::IRModule const&, tvm::GlobalVar const&, tvm::relay::Function)+0x5f6) [0x7f428f01f7e6]
    [bt] (7) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModuleNode::Add(tvm::GlobalVar const&, tvm::BaseFunc const&, bool)+0xd7) [0x7f428f01fe37]
    [bt] (8) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModule::FromExpr(tvm::RelayExpr const&, tvm::Map<tvm::GlobalVar, tvm::BaseFunc, void, void> const&, tvm::Map<tvm::GlobalTypeVar, tvm::TypeData, void, void> const&)+0x4ac) [0x7f428f02312c]

    ; ' should not has tab or newline.
    ''',

    '''
    [09:03:24] /home/lisa/tvm-0.7/src/printer/doc.cc:55: text node: ' an internal invariant was violated while typechecking your program [09:03:24] /home/lisa/tvm-0.7/src/relay/op/type_relations.cc:107: Check failed: t0->dtype == t1->dtype (int16 vs. float32) :
    Stack trace:
    [bt] (0) /home/lisa/tvm-0.7/build/libtvm.so(dmlc::LogMessageFatal::~LogMessageFatal()+0x80) [0x7f94c1cf4b60]
    [bt] (1) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::BroadcastRel(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)+0x30f) [0x7f94c251f8ef]
    [bt] (2) /home/lisa/tvm-0.7/build/libtvm.so(tvm::runtime::TypedPackedFunc<bool (tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>::AssignTypedLambda<bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>(bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&))::{lambda(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*)#1}::operator()(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*) const+0x518) [0x7f94c1e85eb8]
    [bt] (3) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeSolver::Solve()+0x4cd) [0x7f94c25a078d]
    [bt] (4) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeInferencer::Infer(tvm::RelayExpr)+0x5c) [0x7f94c271ebec]
    [bt] (5) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::InferType(tvm::relay::Function const&, tvm::IRModule const&, tvm::GlobalVar const&)+0x3a2) [0x7f94c271f972]
    [bt] (6) /home/lisa/tvm-0.7/build/libtvm.so(tvm::RunTypeCheck(tvm::IRModule const&, tvm::GlobalVar const&, tvm::relay::Function)+0x5f6) [0x7f94c1e057e6]
    [bt] (7) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModuleNode::Add(tvm::GlobalVar const&, tvm::BaseFunc const&, bool)+0xd7) [0x7f94c1e05e37]
    [bt] (8) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModule::FromExpr(tvm::RelayExpr const&, tvm::Map<tvm::GlobalVar, tvm::BaseFunc, void, void> const&, tvm::Map<tvm::GlobalTypeVar, tvm::TypeData, void, void> const&)+0x4ac) [0x7f94c1e0912c]
    ; ' should not has tab or newline.
    [09:03:24] /home/lisa/tvm-0.7/src/printer/doc.cc:55: text node: ' an internal invariant was violated while typechecking your program [09:03:24] /home/lisa/tvm-0.7/src/relay/op/type_relations.cc:123: Check failed: t0->dtype == t1->dtype (int16 vs. float32) :
    Stack trace:
    [bt] (0) /home/lisa/tvm-0.7/build/libtvm.so(dmlc::LogMessageFatal::~LogMessageFatal()+0x80) [0x7f94c1cf4b60]
    [bt] (1) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::BroadcastCompRel(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)+0x30f) [0x7f94c251e53f]
    [bt] (2) /home/lisa/tvm-0.7/build/libtvm.so(tvm::runtime::TypedPackedFunc<bool (tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>::AssignTypedLambda<bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>(bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&))::{lambda(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*)#1}::operator()(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*) const+0x518) [0x7f94c1e85eb8]
    [bt] (3) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeSolver::Solve()+0x4cd) [0x7f94c25a078d]
    [bt] (4) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeInferencer::Infer(tvm::RelayExpr)+0x5c) [0x7f94c271ebec]
    [bt] (5) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::InferType(tvm::relay::Function const&, tvm::IRModule const&, tvm::GlobalVar const&)+0x3a2) [0x7f94c271f972]
    [bt] (6) /home/lisa/tvm-0.7/build/libtvm.so(tvm::RunTypeCheck(tvm::IRModule const&, tvm::GlobalVar const&, tvm::relay::Function)+0x5f6) [0x7f94c1e057e6]
    [bt] (7) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModuleNode::Add(tvm::GlobalVar const&, tvm::BaseFunc const&, bool)+0xd7) [0x7f94c1e05e37]
    [bt] (8) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModule::FromExpr(tvm::RelayExpr const&, tvm::Map<tvm::GlobalVar, tvm::BaseFunc, void, void> const&, tvm::Map<tvm::GlobalTypeVar, tvm::TypeData, void, void> const&)+0x4ac) [0x7f94c1e0912c]
    ''',

    '''
    Traceback (most recent call last):
        File "/home/lisa/TVMfuzz/buggyFile2/../buggyFile/11.py", line 158, in <module>
            nJek4=run_opt_pass(aPzKb,[FMA8X,])
        File "/home/lisa/TVMfuzz/buggyFile2/../buggyFile/11.py", line 153, in run_opt_pass
            mod = tvm.IRModule.from_expr(expr)
        File "/home/lisa/tvm-0.7/python/tvm/ir/module.py", line 237, in from_expr
            return _ffi_api.Module_FromExpr(expr, funcs, defs)
        File "/home/lisa/tvm-0.7/python/tvm/_ffi/_ctypes/packed_func.py", line 237, in __call__
            raise get_last_ffi_error()
        tvm._ffi.base.TVMError: Traceback (most recent call last):
        [bt] (8) /home/lisa/tvm-0.7/build/libtvm.so(TVMFuncCall+0x63) [0x7f22caadcd63]
        [bt] (7) /home/lisa/tvm-0.7/build/libtvm.so(+0x1e932e8) [0x7f22c9ff72e8]
        [bt] (6) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModule::FromExpr(tvm::RelayExpr const&, tvm::Map<tvm::GlobalVar, tvm::BaseFunc, void, void> const&, tvm::Map<tvm::GlobalTypeVar, tvm::TypeData, void, void> const&)+0x4ac) [0x7f22c9ff212c]
        [bt] (5) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModuleNode::Add(tvm::GlobalVar const&, tvm::BaseFunc const&, bool)+0xd7) [0x7f22c9feee37]
        [bt] (4) /home/lisa/tvm-0.7/build/libtvm.so(tvm::RunTypeCheck(tvm::IRModule const&, tvm::GlobalVar const&, tvm::relay::Function)+0x5f6) [0x7f22c9fee7e6]
        [bt] (3) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::InferType(tvm::relay::Function const&, tvm::IRModule const&, tvm::GlobalVar const&)+0x3a2) [0x7f22ca908972]
        [bt] (2) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeInferencer::Infer(tvm::RelayExpr)+0x78) [0x7f22ca907c08]
        [bt] (1) /home/lisa/tvm-0.7/build/libtvm.so(tvm::ErrorReporter::RenderErrors(tvm::IRModule const&, bool)+0x2098) [0x7f22c9fda288]
        [bt] (0) /home/lisa/tvm-0.7/build/libtvm.so(dmlc::LogMessageFatal::~LogMessageFatal()+0x80) [0x7f22c9eddb60]
        File "/home/lisa/tvm-0.7/src/ir/error.cc", line 132
        TVMError:
        Error(s) have occurred. The program has been annotated with them:

        In `main`:
        #[version = "0.0.5"]
        fn (%x0: uint64, %x) {
        if (%x0) {
            add(3, %x)
        } else {
            3
        }
    }
    ''',

    '''
    Traceback (most recent call last):
    File "/home/lisa/TVMfuzz/buggyFile2/../buggyFile/12.py", line 169, in <module>
        MgtyN=run_infer_type(DKq4w)
    File "/home/lisa/TVMfuzz/buggyFile2/../buggyFile/12.py", line 152, in run_infer_type
        mod = tvm.IRModule.from_expr(expr)
    File "/home/lisa/tvm-0.7/python/tvm/ir/module.py", line 237, in from_expr
        return _ffi_api.Module_FromExpr(expr, funcs, defs)
    File "/home/lisa/tvm-0.7/python/tvm/_ffi/_ctypes/packed_func.py", line 237, in __call__
        raise get_last_ffi_error()
    tvm._ffi.base.TVMError: Traceback (most recent call last):
    [bt] (8) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeInferencer::Resolver::VisitExpr_(tvm::relay::FunctionNode const*)+0x22) [0x7f8a6ce29cc2]
    [bt] (7) /home/lisa/tvm-0.7/build/libtvm.so(tvm::RelayExpr tvm::relay::TypeInferencer::Resolver::AttachCheckedType<tvm::relay::FunctionNode>(tvm::relay::FunctionNode const*)+0x1be) [0x7f8a6ce298ee]
    [bt] (6) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::ExprMutator::VisitExpr_(tvm::relay::FunctionNode const*)+0x55f) [0x7f8a6cf06acf]
    [bt] (5) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::ExprMutator::VisitExpr(tvm::RelayExpr const&)+0x96) [0x7f8a6cf08e06]
    [bt] (4) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>::VisitExpr(tvm::RelayExpr const&)+0x76) [0x7f8a6cf0ece6]
    [bt] (3) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>::InitVTable()::{lambda(tvm::runtime::ObjectRef const&, tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>*)#6}::_FUN(tvm::runtime::ObjectRef const&, tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>*)+0x2c) [0x7f8a6cdad48c]
    [bt] (2) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeInferencer::Resolver::VisitExpr_(tvm::relay::CallNode const*)+0x22) [0x7f8a6ce29702]
    [bt] (1) /home/lisa/tvm-0.7/build/libtvm.so(tvm::RelayExpr tvm::relay::TypeInferencer::Resolver::AttachCheckedType<tvm::relay::CallNode>(tvm::relay::CallNode const*)+0x1ad) [0x7f8a6ce291cd]
    [bt] (0) /home/lisa/tvm-0.7/build/libtvm.so(+0x27a2988) [0x7f8a6ce1e988]
    File "/home/lisa/tvm-0.7/src/relay/transforms/type_infer.cc", line 617
    TVMError: Check failed: checked_type.as<IncompleteTypeNode>() == nullptr: Cannot resolve type of CallNode(Op(image.resize3d), [Var(x0, ty=TupleTypeNode([]))], relay.attrs.Resize3dAttrs(0x55f633b94398), []) at (nullptr)
    ''',

    '''
    Traceback (most recent call last):
    File "/home/lisa/TVMfuzz/buggyFile2/6.py", line 173, in <module>
        F8ExZ=make_nat_expr(EHXnr,3)
    File "/home/lisa/tvm-0.7/python/tvm/relay/testing/nat.py", line 182, in make_nat_expr
        ret = prelude.z()
    AttributeError: 'Prelude' object has no attribute 'z'
    ''',

    '''
    Traceback (most recent call last):
        File "/home/lisa/TVMfuzz/buggyFile2/9.py", line 37, in <module>
            hz8Ce[WY1iX]=xmkLE
        File "/home/lisa/tvm-0.7/python/tvm/ir/module.py", line 75, in __setitem__
            return self._add(var, val)
        File "/home/lisa/tvm-0.7/python/tvm/ir/module.py", line 84, in _add
            _ffi_api.Module_Add(self, var, val, update)
        File "/home/lisa/tvm-0.7/python/tvm/_ffi/_ctypes/packed_func.py", line 237, in __call__
            raise get_last_ffi_error()
    tvm._ffi.base.TVMError: Traceback (most recent call last):
        [bt] (8) /home/lisa/tvm-0.7/build/libtvm.so(TVMFuncCall+0x63) [0x7f09eda38d63]
        [bt] (7) /home/lisa/tvm-0.7/build/libtvm.so(+0x1e8fed8) [0x7f09ecf4fed8]
        [bt] (6) /home/lisa/tvm-0.7/build/libtvm.so(+0x1e8f091) [0x7f09ecf4f091]
        [bt] (5) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModuleNode::Add(tvm::GlobalVar const&, tvm::BaseFunc const&, bool)+0xd7) [0x7f09ecf4ae37]
        [bt] (4) /home/lisa/tvm-0.7/build/libtvm.so(tvm::RunTypeCheck(tvm::IRModule const&, tvm::GlobalVar const&, tvm::relay::Function)+0x5f6) [0x7f09ecf4a7e6]
        [bt] (3) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::InferType(tvm::relay::Function const&, tvm::IRModule const&, tvm::GlobalVar const&)+0x3a2) [0x7f09ed864972]
        [bt] (2) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeInferencer::Infer(tvm::RelayExpr)+0x78) [0x7f09ed863c08]
        [bt] (1) /home/lisa/tvm-0.7/build/libtvm.so(tvm::ErrorReporter::RenderErrors(tvm::IRModule const&, bool)+0x2098) [0x7f09ecf36288]
        [bt] (0) /home/lisa/tvm-0.7/build/libtvm.so(dmlc::LogMessageFatal::~LogMessageFatal()+0x80) [0x7f09ece39b60]
    File "/home/lisa/tvm-0.7/src/ir/error.cc", line 132
    TVMError:
    Error(s) have occurred. The program has been annotated with them:

    In `f`:
    #[version = "0.0.5"]
    fn [t](%a: t) -> t {
    @f(1)
    } unable to unify: `int32` and `t`;
    ''',

    '''
    Traceback (most recent call last):
    File "/home/lisa/TVMfuzz/buggyFile2/39.py", line 128, in <module>
        check_kind(EK3h8)
    File "/home/lisa/tvm-0.7/python/tvm/relay/analysis/analysis.py", line 106, in check_kind
        return _ffi_api.check_kind(t)
    File "/home/lisa/tvm-0.7/python/tvm/_ffi/_ctypes/packed_func.py", line 237, in __call__
        raise get_last_ffi_error()
    tvm._ffi.base.TVMError: TVMError: Incorrect kind for a type call function. Type GlobalTypeVar(v1, 0) inside TypeCallNode(GlobalTypeVar(v1, 0), []) is of kind 0 but was expected to be 5
    ''',

    '''
    [10:03:33] /home/lisa/tvm-0.7/src/printer/doc.cc:55: text node: ' an internal invariant was violated while typechecking your program [10:03:33] /home/lisa/tvm-0.7/src/relay/op/nn/convolution.h:204: Check failed: reporter->AssertEQ(param->kernel_size[0], wshape[2]) && reporter->AssertEQ(param->kernel_size[1], wshape[3]): Conv2D: shape of weight is inconsistent with kernel_size,  kernel_size=[3, 3] wshape=[32, 1, 3, 0]
    Stack trace:
        [bt] (0) /home/lisa/tvm-0.7/build/libtvm.so(+0x2419d28) [0x7f2de0c65d28]
        [bt] (1) /home/lisa/tvm-0.7/build/libtvm.so(bool tvm::relay::Conv2DRel<tvm::relay::Conv2DAttrs>(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)+0x13a7) [0x7f2de0c909f7]
        [bt] (2) /home/lisa/tvm-0.7/build/libtvm.so(tvm::runtime::TypedPackedFunc<bool (tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>::AssignTypedLambda<bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>(bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&))::{lambda(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*)#1}::operator()(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*) const+0x518) [0x7f2de0756eb8]
        [bt] (3) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeSolver::Solve()+0x4cd) [0x7f2de0e7178d]
        [bt] (4) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeInferencer::Infer(tvm::RelayExpr)+0x5c) [0x7f2de0fefbec]
        [bt] (5) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::InferType(tvm::relay::Function const&, tvm::IRModule const&, tvm::GlobalVar const&)+0x3a2) [0x7f2de0ff0972]
        [bt] (6) /home/lisa/tvm-0.7/build/libtvm.so(tvm::RunTypeCheck(tvm::IRModule const&, tvm::GlobalVar const&, tvm::relay::Function)+0x5f6) [0x7f2de06d67e6]
        [bt] (7) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModuleNode::Add(tvm::GlobalVar const&, tvm::BaseFunc const&, bool)+0xd7) [0x7f2de06d6e37]
        [bt] (8) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModule::FromExpr(tvm::RelayExpr const&, tvm::Map<tvm::GlobalVar, tvm::BaseFunc, void, void> const&, tvm::Map<tvm::GlobalTypeVar, tvm::TypeData, void, void> const&)+0x4ac) [0x7f2de06da12c]

    ; ' should not has tab or newline.
    Traceback (most recent call last):
    File "/home/lisa/TVMfuzz/buggyFile2/37.py", line 192, in <module>
        RjZTd=annotated(\'\'\'int32\'\'\',(1,32,0,10,),(32,1,3,0,))
    File "/home/lisa/TVMfuzz/buggyFile2/37.py", line 190, in annotated
        mod = tvm.IRModule.from_expr(f)
    File "/home/lisa/tvm-0.7/python/tvm/ir/module.py", line 237, in from_expr
        return _ffi_api.Module_FromExpr(expr, funcs, defs)
    File "/home/lisa/tvm-0.7/python/tvm/_ffi/_ctypes/packed_func.py", line 237, in __call__
        raise get_last_ffi_error()
    tvm._ffi.base.TVMError: Traceback (most recent call last):
        [bt] (8) /home/lisa/tvm-0.7/build/libtvm.so(TVMFuncCall+0x63) [0x7f2de11c4d63]
        [bt] (7) /home/lisa/tvm-0.7/build/libtvm.so(+0x1e932e8) [0x7f2de06df2e8]
        [bt] (6) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModule::FromExpr(tvm::RelayExpr const&, tvm::Map<tvm::GlobalVar, tvm::BaseFunc, void, void> const&, tvm::Map<tvm::GlobalTypeVar, tvm::TypeData, void, void> const&)+0x4ac) [0x7f2de06da12c]
        [bt] (5) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModuleNode::Add(tvm::GlobalVar const&, tvm::BaseFunc const&, bool)+0xd7) [0x7f2de06d6e37]
        [bt] (4) /home/lisa/tvm-0.7/build/libtvm.so(tvm::RunTypeCheck(tvm::IRModule const&, tvm::GlobalVar const&, tvm::relay::Function)+0x5f6) [0x7f2de06d67e6]
        [bt] (3) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::InferType(tvm::relay::Function const&, tvm::IRModule const&, tvm::GlobalVar const&)+0x3a2) [0x7f2de0ff0972]
        [bt] (2) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeInferencer::Infer(tvm::RelayExpr)+0x78) [0x7f2de0fefc08]
        [bt] (1) /home/lisa/tvm-0.7/build/libtvm.so(tvm::ErrorReporter::RenderErrors(tvm::IRModule const&, bool)+0x2098) [0x7f2de06c2288]
        [bt] (0) /home/lisa/tvm-0.7/build/libtvm.so(dmlc::LogMessageFatal::~LogMessageFatal()+0x80) [0x7f2de05c5b60]
        [bt] (8) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModule::FromExpr(tvm::RelayExpr const&, tvm::Map<tvm::GlobalVar, tvm::BaseFunc, void, void> const&, tvm::Map<tvm::GlobalTypeVar, tvm::TypeData, void, void> const&)+0x4ac) [0x7f2de06da12c]
        [bt] (7) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModuleNode::Add(tvm::GlobalVar const&, tvm::BaseFunc const&, bool)+0xd7) [0x7f2de06d6e37]
        [bt] (6) /home/lisa/tvm-0.7/build/libtvm.so(tvm::RunTypeCheck(tvm::IRModule const&, tvm::GlobalVar const&, tvm::relay::Function)+0x5f6) [0x7f2de06d67e6]
        [bt] (5) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::InferType(tvm::relay::Function const&, tvm::IRModule const&, tvm::GlobalVar const&)+0x3a2) [0x7f2de0ff0972]
        [bt] (4) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeInferencer::Infer(tvm::RelayExpr)+0x5c) [0x7f2de0fefbec]
        [bt] (3) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeSolver::Solve()+0x4cd) [0x7f2de0e7178d]
        [bt] (2) /home/lisa/tvm-0.7/build/libtvm.so(tvm::runtime::TypedPackedFunc<bool (tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>::AssignTypedLambda<bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>(bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&))::{lambda(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*)#1}::operator()(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*) const+0x518) [0x7f2de0756eb8]
        [bt] (1) /home/lisa/tvm-0.7/build/libtvm.so(bool tvm::relay::Conv2DRel<tvm::relay::Conv2DAttrs>(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)+0x13a7) [0x7f2de0c909f7]
        [bt] (0) /home/lisa/tvm-0.7/build/libtvm.so(+0x2419d28) [0x7f2de0c65d28]
        File "/home/lisa/tvm-0.7/src/ir/error.cc", line 132
    TVMError:
    Error(s) have occurred. The program has been annotated with them:

    In `main`:
    #[version = "0.0.5"]
    fn (%data: Tensor[(1, 32, 0, 10), int32], %weight1: Tensor[(32, 1, 3, 0), int32]) {
        %0 = nn.conv2d(%data, %weight1, padding=[1, 1, 1, 1], groups=32, kernel_size=[3, 3]) an internal invariant was violated while typechecking your program [10:03:33] /home/lisa/tvm-0.7/src/relay/op/nn/convolution.h:204: Check failed: reporter->AssertEQ(param->kernel_size[0], wshape[2]) && reporter->AssertEQ(param->kernel_size[1], wshape[3]): Conv2D: shape of weight is inconsistent with kernel_size,  kernel_size=[3, 3] wshape=[32, 1, 3, 0]
        ; ;
        %1 = nn.conv2d(%0, %weight1, padding=[1, 1, 1, 1], groups=32, kernel_size=[3, 3]);
        add(%0, %1)
    }
    ''',

    '''
    [10:13:58] /home/lisa/tvm-0.7/src/printer/doc.cc:55: text node: ' an internal invariant was violated while typechecking your program [10:13:58] /home/lisa/tvm-0.7/src/relay/op/tensor/transform.cc:1452: Check failed: val->value > 0 (0 vs. 0) : Tile reps value should always be larger than 0, but get: 0
    Stack trace:
        [bt] (0) /home/lisa/tvm-0.7/build/libtvm.so(+0x25245e8) [0x7f68cce7c5e8]
        [bt] (1) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TileRel(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)+0x6a1) [0x7f68cce86881]
        [bt] (2) /home/lisa/tvm-0.7/build/libtvm.so(tvm::runtime::TypedPackedFunc<bool (tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>::AssignTypedLambda<bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>(bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&))::{lambda(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*)#1}::operator()(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*) const+0x518) [0x7f68cc862eb8]
        [bt] (3) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeSolver::Solve()+0x4cd) [0x7f68ccf7d78d]
        [bt] (4) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeInferencer::Infer(tvm::RelayExpr)+0x5c) [0x7f68cd0fbbec]
        [bt] (5) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::InferType(tvm::relay::Function const&, tvm::IRModule const&, tvm::GlobalVar const&)+0x3a2) [0x7f68cd0fc972]
        [bt] (6) /home/lisa/tvm-0.7/build/libtvm.so(tvm::RunTypeCheck(tvm::IRModule const&, tvm::GlobalVar const&, tvm::relay::Function)+0x5f6) [0x7f68cc7e27e6]
        [bt] (7) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModuleNode::Add(tvm::GlobalVar const&, tvm::BaseFunc const&, bool)+0xd7) [0x7f68cc7e2e37]
        [bt] (8) /home/lisa/tvm-0.7/build/libtvm.so(+0x1e8f091) [0x7f68cc7e7091]

    ; ' should not has tab or newline.
    Traceback (most recent call last):
        File "/home/lisa/TVMfuzz/buggyFile2/32.py", line 705, in <module>
            verify_tile((2,3,4,),(3,0,1,))
        File "/home/lisa/TVMfuzz/buggyFile2/32.py", line 703, in verify_tile
            op_res = intrp.evaluate(func)(x_data)
        File "/home/lisa/tvm-0.7/python/tvm/relay/backend/interpreter.py", line 178, in evaluate
            return self._make_executor(expr)
        File "/home/lisa/tvm-0.7/python/tvm/relay/build_module.py", line 365, in _make_executor
            self.mod["main"] = expr
        File "/home/lisa/tvm-0.7/python/tvm/ir/module.py", line 75, in __setitem__
            return self._add(var, val)
        File "/home/lisa/tvm-0.7/python/tvm/ir/module.py", line 84, in _add
            _ffi_api.Module_Add(self, var, val, update)
        File "/home/lisa/tvm-0.7/python/tvm/_ffi/_ctypes/packed_func.py", line 237, in __call__
            raise get_last_ffi_error()
    tvm._ffi.base.TVMError: Traceback (most recent call last):
        [bt] (8) /home/lisa/tvm-0.7/build/libtvm.so(TVMFuncCall+0x63) [0x7f68cd2d0d63]
        [bt] (7) /home/lisa/tvm-0.7/build/libtvm.so(+0x1e8fed8) [0x7f68cc7e7ed8]
        [bt] (6) /home/lisa/tvm-0.7/build/libtvm.so(+0x1e8f091) [0x7f68cc7e7091]
        [bt] (5) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModuleNode::Add(tvm::GlobalVar const&, tvm::BaseFunc const&, bool)+0xd7) [0x7f68cc7e2e37]
        [bt] (4) /home/lisa/tvm-0.7/build/libtvm.so(tvm::RunTypeCheck(tvm::IRModule const&, tvm::GlobalVar const&, tvm::relay::Function)+0x5f6) [0x7f68cc7e27e6]
        [bt] (3) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::InferType(tvm::relay::Function const&, tvm::IRModule const&, tvm::GlobalVar const&)+0x3a2) [0x7f68cd0fc972]
        [bt] (2) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeInferencer::Infer(tvm::RelayExpr)+0x78) [0x7f68cd0fbc08]
        [bt] (1) /home/lisa/tvm-0.7/build/libtvm.so(tvm::ErrorReporter::RenderErrors(tvm::IRModule const&, bool)+0x2098) [0x7f68cc7ce288]
        [bt] (0) /home/lisa/tvm-0.7/build/libtvm.so(dmlc::LogMessageFatal::~LogMessageFatal()+0x80) [0x7f68cc6d1b60]
        [bt] (8) /home/lisa/tvm-0.7/build/libtvm.so(+0x1e8f091) [0x7f68cc7e7091]
        [bt] (7) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModuleNode::Add(tvm::GlobalVar const&, tvm::BaseFunc const&, bool)+0xd7) [0x7f68cc7e2e37]
        [bt] (6) /home/lisa/tvm-0.7/build/libtvm.so(tvm::RunTypeCheck(tvm::IRModule const&, tvm::GlobalVar const&, tvm::relay::Function)+0x5f6) [0x7f68cc7e27e6]
        [bt] (5) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::InferType(tvm::relay::Function const&, tvm::IRModule const&, tvm::GlobalVar const&)+0x3a2) [0x7f68cd0fc972]
        [bt] (4) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeInferencer::Infer(tvm::RelayExpr)+0x5c) [0x7f68cd0fbbec]
        [bt] (3) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeSolver::Solve()+0x4cd) [0x7f68ccf7d78d]
        [bt] (2) /home/lisa/tvm-0.7/build/libtvm.so(tvm::runtime::TypedPackedFunc<bool (tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>::AssignTypedLambda<bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>(bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&))::{lambda(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*)#1}::operator()(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*) const+0x518) [0x7f68cc862eb8]
        [bt] (1) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TileRel(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)+0x6a1) [0x7f68cce86881]
        [bt] (0) /home/lisa/tvm-0.7/build/libtvm.so(+0x25245e8) [0x7f68cce7c5e8]
    File "/home/lisa/tvm-0.7/src/ir/error.cc", line 132
    TVMError:
    Error(s) have occurred. The program has been annotated with them:

    In `main`:
        #[version = "0.0.5"]
        fn (%x: Tensor[(2, 3, 4), float32]) {
        tile(%x, reps=[3, 0, 1]) an internal invariant was violated while typechecking your program [10:13:58] /home/lisa/tvm-0.7/src/relay/op/tensor/transform.cc:1452: Check failed: val->value > 0 (0 vs. 0) : Tile reps value should always be larger than 0, but get: 0
        ;
    }
    ''',

    '''
    [10:48:52] /home/lisa/tvm-0.7/src/printer/doc.cc:55: text node: ' an internal invariant was violated while typechecking your program [10:48:52] /home/lisa/tvm-0.7/src/relay/qnn/op/quantize.cc:49: Check failed: input_dtype == DataType::Float(32): Input type should be one of float32 but was int32
    Stack trace:
        [bt] (0) /home/lisa/tvm-0.7/build/libtvm.so(+0x28ccf68) [0x7f65bc0d8f68]
        [bt] (1) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::qnn::QuantizeRel(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)+0x211) [0x7f65bc0d9b41]
        [bt] (2) /home/lisa/tvm-0.7/build/libtvm.so(tvm::runtime::TypedPackedFunc<bool (tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>::AssignTypedLambda<bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>(bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&))::{lambda(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*)#1}::operator()(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*) const+0x518) [0x7f65bb716eb8]
        [bt] (3) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeSolver::Solve()+0x4cd) [0x7f65bbe3178d]
        [bt] (4) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeInferencer::Infer(tvm::RelayExpr)+0x5c) [0x7f65bbfafbec]
        [bt] (5) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::InferType(tvm::relay::Function const&, tvm::IRModule const&, tvm::GlobalVar const&)+0x3a2) [0x7f65bbfb0972]
        [bt] (6) /home/lisa/tvm-0.7/build/libtvm.so(tvm::RunTypeCheck(tvm::IRModule const&, tvm::GlobalVar const&, tvm::relay::Function)+0x5f6) [0x7f65bb6967e6]
        [bt] (7) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModuleNode::Add(tvm::GlobalVar const&, tvm::BaseFunc const&, bool)+0xd7) [0x7f65bb696e37]
        [bt] (8) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModule::FromExpr(tvm::RelayExpr const&, tvm::Map<tvm::GlobalVar, tvm::BaseFunc, void, void> const&, tvm::Map<tvm::GlobalTypeVar, tvm::TypeData, void, void> const&)+0x4ac) [0x7f65bb69a12c]

    ; ' should not has tab or newline.
    Traceback (most recent call last):
        File "/home/lisa/TVMfuzz/buggyFile2/26.py", line 153, in <module>
            quantize_test_driver(in_dtype=\'\'\'int32\'\'\',quant_args={\'\'\'out_zero_point\'\'\':UBKqL,\'\'\'out_scale\'\'\':wunQz},axis=0,out_dtype=\'\'\'uint8\'\'\',in_data=vIWjt,verify_output_data=vIWjt)
        File "/home/lisa/TVMfuzz/buggyFile2/26.py", line 141, in quantize_test_driver
            mod = tvm.IRModule.from_expr(mod)
        File "/home/lisa/tvm-0.7/python/tvm/ir/module.py", line 237, in from_expr
            return _ffi_api.Module_FromExpr(expr, funcs, defs)
        File "/home/lisa/tvm-0.7/python/tvm/_ffi/_ctypes/packed_func.py", line 237, in __call__
            raise get_last_ffi_error()
    tvm._ffi.base.TVMError: Traceback (most recent call last):
        [bt] (8) /home/lisa/tvm-0.7/build/libtvm.so(TVMFuncCall+0x63) [0x7f65bc184d63]
        [bt] (7) /home/lisa/tvm-0.7/build/libtvm.so(+0x1e932e8) [0x7f65bb69f2e8]
        [bt] (6) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModule::FromExpr(tvm::RelayExpr const&, tvm::Map<tvm::GlobalVar, tvm::BaseFunc, void, void> const&, tvm::Map<tvm::GlobalTypeVar, tvm::TypeData, void, void> const&)+0x4ac) [0x7f65bb69a12c]
        [bt] (5) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModuleNode::Add(tvm::GlobalVar const&, tvm::BaseFunc const&, bool)+0xd7) [0x7f65bb696e37]
        [bt] (4) /home/lisa/tvm-0.7/build/libtvm.so(tvm::RunTypeCheck(tvm::IRModule const&, tvm::GlobalVar const&, tvm::relay::Function)+0x5f6) [0x7f65bb6967e6]
        [bt] (3) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::InferType(tvm::relay::Function const&, tvm::IRModule const&, tvm::GlobalVar const&)+0x3a2) [0x7f65bbfb0972]
        [bt] (2) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeInferencer::Infer(tvm::RelayExpr)+0x78) [0x7f65bbfafc08]
        [bt] (1) /home/lisa/tvm-0.7/build/libtvm.so(tvm::ErrorReporter::RenderErrors(tvm::IRModule const&, bool)+0x2098) [0x7f65bb682288]
        [bt] (0) /home/lisa/tvm-0.7/build/libtvm.so(dmlc::LogMessageFatal::~LogMessageFatal()+0x80) [0x7f65bb585b60]
        [bt] (8) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModule::FromExpr(tvm::RelayExpr const&, tvm::Map<tvm::GlobalVar, tvm::BaseFunc, void, void> const&, tvm::Map<tvm::GlobalTypeVar, tvm::TypeData, void, void> const&)+0x4ac) [0x7f65bb69a12c]
        [bt] (7) /home/lisa/tvm-0.7/build/libtvm.so(tvm::IRModuleNode::Add(tvm::GlobalVar const&, tvm::BaseFunc const&, bool)+0xd7) [0x7f65bb696e37]
        [bt] (6) /home/lisa/tvm-0.7/build/libtvm.so(tvm::RunTypeCheck(tvm::IRModule const&, tvm::GlobalVar const&, tvm::relay::Function)+0x5f6) [0x7f65bb6967e6]
        [bt] (5) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::InferType(tvm::relay::Function const&, tvm::IRModule const&, tvm::GlobalVar const&)+0x3a2) [0x7f65bbfb0972]
        [bt] (4) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeInferencer::Infer(tvm::RelayExpr)+0x5c) [0x7f65bbfafbec]
        [bt] (3) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeSolver::Solve()+0x4cd) [0x7f65bbe3178d]
        [bt] (2) /home/lisa/tvm-0.7/build/libtvm.so(tvm::runtime::TypedPackedFunc<bool (tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>::AssignTypedLambda<bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>(bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&))::{lambda(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*)#1}::operator()(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*) const+0x518) [0x7f65bb716eb8]
        [bt] (1) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::qnn::QuantizeRel(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)+0x211) [0x7f65bc0d9b41]
        [bt] (0) /home/lisa/tvm-0.7/build/libtvm.so(+0x28ccf68) [0x7f65bc0d8f68]
    File "/home/lisa/tvm-0.7/src/ir/error.cc", line 132
    TVMError:
    Error(s) have occurred. The program has been annotated with them:

    In `main`:
    #[version = "0.0.5"]
        fn (%input_data: Tensor[(5, 2), int32]) {
        qnn.quantize(%input_data, meta[relay.Constant][0], meta[relay.Constant][1], out_dtype="uint8", axis=0) an internal invariant was violated while typechecking your program [10:48:52] /home/lisa/tvm-0.7/src/relay/qnn/op/quantize.cc:49: Check failed: input_dtype == DataType::Float(32): Input type should be one of float32 but was int32
        ;
    }
    /* For debugging purposes the metadata section has been omitted.
    * If you would like to see the full metadata section you can set the
    * option to `True` when invoking `astext`.
    */
    ''',

    '''
    file:10:18: parse error: a type definition with the name `List` was previously defined
                    type List[A] {
        ~~~~~~~~~~~~~~~~~^~~~~~~~~
    file:11:13: parse error: a constructor with the name `Cons` was previously defined
                    Cons(A, List[A]),
        ~~~~~~~~~~~~^~~~~~~~~~~~~~~~~
    ''',

    '''
    Traceback (most recent call last):
    File "/home/lisa/TVMfuzz/buggyFile2/7.py", line 3728, in <module>
        LZ2cL=KEkqH.partition(mcksQ)
    File "/home/lisa/tvm-0.7/python/tvm/relay/dataflow_pattern/__init__.py", line 171, in partition
        return partition(self, expr, attrs, check)
    File "/home/lisa/tvm-0.7/python/tvm/relay/dataflow_pattern/__init__.py", line 802, in partition
        return ffi.partition(pattern, expr, attrs, check)
    File "/home/lisa/tvm-0.7/python/tvm/_ffi/_ctypes/packed_func.py", line 237, in __call__
        raise get_last_ffi_error()
    tvm._ffi.base.TVMError: Traceback (most recent call last):
        [bt] (8) /home/lisa/tvm-0.7/build/libtvm.so(tvm::RelayExpr tvm::relay::TypeInferencer::Resolver::AttachCheckedType<tvm::relay::FunctionNode>(tvm::relay::FunctionNode const*)+0x1be) [0x7f6e77fce8ee]
        [bt] (7) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::ExprMutator::VisitExpr_(tvm::relay::FunctionNode const*)+0x382) [0x7f6e780ab8f2]
        [bt] (6) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::ExprMutator::VisitExpr(tvm::RelayExpr const&)+0x96) [0x7f6e780ade06]
        [bt] (5) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>::VisitExpr(tvm::RelayExpr const&)+0x76) [0x7f6e780b3ce6]
        [bt] (4) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>::InitVTable()::{lambda(tvm::runtime::ObjectRef const&, tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>*)#3}::_FUN(tvm::runtime::ObjectRef const&, tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>*)+0x2c) [0x7f6e77f5239c]
        [bt] (3) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeInferencer::Resolver::VisitExpr_(tvm::relay::VarNode const*)+0x87) [0x7f6e77fd14f7]
        [bt] (2) /home/lisa/tvm-0.7/build/libtvm.so(tvm::relay::TypeInferencer::Resolver::VisitVar(tvm::relay::Var const&)+0xe2) [0x7f6e77fd12c2]
        [bt] (1) /home/lisa/tvm-0.7/build/libtvm.so(tvm::RelayExpr tvm::relay::TypeInferencer::Resolver::AttachCheckedType<tvm::relay::VarNode>(tvm::relay::VarNode const*)+0x1ab) [0x7f6e77fcbd2b]
        [bt] (0) /home/lisa/tvm-0.7/build/libtvm.so(+0x27a2988) [0x7f6e77fc3988]
    File "/home/lisa/tvm-0.7/src/relay/transforms/type_infer.cc", line 617
    TVMError: Check failed: checked_type.as<IncompleteTypeNode>() == nullptr: Cannot resolve type of Var(weight) at (nullptr)
    ''',
]

message['0.8'] = [ 

    '''
    Traceback (most recent call last):
    File "/home/lisa/TVMfuzz/byproduct/../buggyFile/7.py", line 2236, in <module>
        m7tRI=run_opt_pass(IVUfN,rolTI)
    File "/home/lisa/TVMfuzz/byproduct/../buggyFile/7.py", line 2230, in run_opt_pass
        mod = opt_pass(mod)
    File "/home/lisa/tvm/python/tvm/ir/transform.py", line 127, in __call__
        return _ffi_transform_api.RunPass(self, mod)
    File "/home/lisa/tvm/python/tvm/_ffi/_ctypes/packed_func.py", line 237, in __call__
        raise get_last_ffi_error()
    tvm._ffi.base.TVMError: Traceback (most recent call last):
    [bt] (8) /home/lisa/tvm/build/libtvm.so(tvm::relay::ExprMutator::VisitExpr(tvm::RelayExpr const&)+0x96) [0x7f7255c78b96]
    [bt] (7) /home/lisa/tvm/build/libtvm.so(tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>::VisitExpr(tvm::RelayExpr const&)+0x76) [0x7f7255c7ea46]
    [bt] (6) /home/lisa/tvm/build/libtvm.so(tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>::InitVTable()::{lambda(tvm::runtime::ObjectRef const&, tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>*)#6}::_FUN(tvm::runtime::ObjectRef const&, tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>*)+0x2c) [0x7f7255b0b3ec]
    [bt] (5) /home/lisa/tvm/build/libtvm.so(tvm::relay::MixedModeMutator::VisitExpr_(tvm::relay::CallNode const*)+0x9e) [0x7f7255a80f6e]
    [bt] (4) /home/lisa/tvm/build/libtvm.so(tvm::relay::ForwardRewriter::Rewrite_(tvm::relay::CallNode const*, tvm::RelayExpr const&)+0xf97) [0x7f7255ade7e7]
    [bt] (3) /home/lisa/tvm/build/libtvm.so(tvm::runtime::TypedPackedFunc<tvm::RelayExpr (tvm::relay::Call const&, tvm::runtime::Array<tvm::RelayExpr, void> const&, tvm::runtime::ObjectRef const&)>::AssignTypedLambda<tvm::RelayExpr (*)(tvm::relay::Call const&, tvm::runtime::Array<tvm::RelayExpr, void> const&, tvm::runtime::ObjectRef const&)>(tvm::RelayExpr (*)(tvm::relay::Call const&, tvm::runtime::Array<tvm::RelayExpr, void> const&, tvm::runtime::ObjectRef const&))::{lambda(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*)#1}::operator()(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*) const+0x349) [0x7f7255a2c389]
    [bt] (2) /home/lisa/tvm/build/libtvm.so(tvm::RelayExpr tvm::relay::LayoutRewriter<tvm::relay::alter_op_layout::AlterTransformMemorizer>(tvm::relay::Call const&, tvm::runtime::Array<tvm::RelayExpr, void> const&, tvm::runtime::ObjectRef const&)+0xcd5) [0x7f7255a344e5]
    [bt] (1) /home/lisa/tvm/build/libtvm.so(tvm::RelayExprNode::checked_type() const+0x157) [0x7f72559aa5e7]
    [bt] (0) /home/lisa/tvm/build/libtvm.so(+0x2702338) [0x7f72559a8338]
    File "/home/lisa/tvm/include/tvm/ir/expr.h", line 476
    TVMError:
    ---------------------------------------------------------------
    An internal invariant was violated during the execution of TVM.
    Please read TVM's error reporting guidelines.
    More details can be found here: https://discuss.tvm.ai/t/error-reporting/7793.
    ---------------------------------------------------------------
    Check failed: checked_type_.defined() == false: internal error: the type checker has not populated the checked_type field for Var(x, ty=TensorType([1, 56, 56, 64], float32))
    ''',
    
    '''
    Traceback (most recent call last):
    File "/home/lisa/TVMfuzz/buggyFile2/1.py", line 152, in <module>
        AG624=to_cps(C9trW[\'\'\'main\'\'\'],mod=C9trW)
    File "/home/lisa/tvm/python/tvm/relay/transform/transform.py", line 840, in to_cps
        return _ffi_api.to_cps(func, use_mod)
    File "/home/lisa/tvm/python/tvm/_ffi/_ctypes/packed_func.py", line 237, in __call__
        raise get_last_ffi_error()
    tvm._ffi.base.TVMError: Traceback (most recent call last):
    [bt] (8) /home/lisa/tvm/build/libtvm.so(tvm::relay::ToCPS(tvm::relay::Function const&, tvm::IRModule const&, std::unordered_map<tvm::GlobalVar, tvm::GlobalVar, tvm::runtime::ObjectPtrHash, tvm::runtime::ObjectPtrEqual, std::allocator<std::pair<tvm::GlobalVar const, tvm::GlobalVar> > >*)+0x17e) [0x7f583782855e]
    [bt] (7) /home/lisa/tvm/build/libtvm.so(tvm::relay::ExprVisitor::VisitExpr(tvm::RelayExpr const&)+0x8b) [0x7f583792a5db]
    [bt] (6) /home/lisa/tvm/build/libtvm.so(tvm::relay::ExprFunctor<void (tvm::RelayExpr const&)>::VisitExpr(tvm::RelayExpr const&)+0x6f) [0x7f58378d705f]
    [bt] (5) /home/lisa/tvm/build/libtvm.so(tvm::relay::ExprVisitor::VisitExpr_(tvm::relay::FunctionNode const*)+0xba) [0x7f583792693a]
    [bt] (4) /home/lisa/tvm/build/libtvm.so(tvm::relay::ExprVisitor::VisitExpr(tvm::RelayExpr const&)+0x8b) [0x7f583792a5db]
    [bt] (3) /home/lisa/tvm/build/libtvm.so(tvm::relay::ExprFunctor<void (tvm::RelayExpr const&)>::VisitExpr(tvm::RelayExpr const&)+0x6f) [0x7f58378d705f]
    [bt] (2) /home/lisa/tvm/build/libtvm.so(+0x28d00de) [0x7f58378290de]
    [bt] (1) /home/lisa/tvm/build/libtvm.so(tvm::RelayExprNode::checked_type() const+0x157) [0x7f583765d5e7]
    [bt] (0) /home/lisa/tvm/build/libtvm.so(+0x2702338) [0x7f583765b338]
    File "/home/lisa/tvm/include/tvm/ir/expr.h", line 476
    TVMError:
    ---------------------------------------------------------------
    An internal invariant was violated during the execution of TVM.
    Please read TVM's error reporting guidelines.
    More details can be found here: https://discuss.tvm.ai/t/error-reporting/7793.
    ---------------------------------------------------------------
    Check failed: checked_type_.defined() == false: internal error: the type checker has not populated the checked_type field for Var(data, ty=TensorType([1, 17, 56, 38], float32))
    ''',

    '''
    Traceback (most recent call last):
    File "/home/lisa/TVMfuzz/buggyFile2/../buggyFile/11.py", line 158, in <module>
        nJek4=run_opt_pass(aPzKb,[FMA8X,])
    File "/home/lisa/TVMfuzz/buggyFile2/../buggyFile/11.py", line 154, in run_opt_pass
        mod = opt_pass(mod)
    TypeError: 'list' object is not callable
    ''',

    '''
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    Traceback (most recent call last):
        File "/home/lisa/TVMfuzz/buggyFile/12.py", line 169, in <module>
        MgtyN=run_infer_type(DKq4w)
        File "/home/lisa/TVMfuzz/buggyFile/12.py", line 153, in run_infer_type
        mod = transform.InferType()(mod)
        File "/home/lisa/tvm/python/tvm/ir/transform.py", line 127, in __call__
        return _ffi_transform_api.RunPass(self, mod)
        File "/home/lisa/tvm/python/tvm/_ffi/_ctypes/packed_func.py", line 237, in __call__
        raise get_last_ffi_error()
    tvm.error.DiagnosticError: Traceback (most recent call last):
        [bt] (6) /home/lisa/tvm/build/libtvm.so(TVMFuncCall+0x63) [0x7f01235242a3]
        [bt] (5) /home/lisa/tvm/build/libtvm.so(+0x1f39ed4) [0x7f012298aed4]
        [bt] (4) /home/lisa/tvm/build/libtvm.so(tvm::transform::ModulePassNode::operator()(tvm::IRModule, tvm::transform::PassContext const&) const+0x1d4) [0x7f012298a534]
        [bt] (3) /home/lisa/tvm/build/libtvm.so(+0x28dd442) [0x7f012332e442]
        [bt] (2) /home/lisa/tvm/build/libtvm.so(+0x28dc3c7) [0x7f012332d3c7]
        [bt] (1) /home/lisa/tvm/build/libtvm.so(tvm::DiagnosticContext::Render()+0x231) [0x7f012293b4f1]
        [bt] (0) /home/lisa/tvm/build/libtvm.so(+0x1eea0e8) [0x7f012293b0e8]
    File "/home/lisa/tvm/src/ir/diagnostic.cc", line 105
    DiagnosticError: one or more error diagnostics were emitted, please check diagnostic render for output.
    ''',

    '''
    Traceback (most recent call last):
    File "/home/lisa/TVMfuzz/buggyFile2/4.py", line 1968, in <module>
        ayUbk=run_opt_pass(cqCZg,g8VBv)
    File "/home/lisa/TVMfuzz/buggyFile2/4.py", line 1962, in run_opt_pass
        mod = opt_pass(mod)
    File "/home/lisa/tvm/python/tvm/ir/transform.py", line 127, in __call__
        return _ffi_transform_api.RunPass(self, mod)
    File "/home/lisa/tvm/python/tvm/_ffi/_ctypes/packed_func.py", line 237, in __call__
        raise get_last_ffi_error()
    tvm._ffi.base.TVMError: Traceback (most recent call last):
        [bt] (8) /home/lisa/tvm/build/libtvm.so(tvm::relay::ExprMutator::VisitExpr(tvm::RelayExpr const&)+0x96) [0x7feba3fadb96]
        [bt] (7) /home/lisa/tvm/build/libtvm.so(tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>::VisitExpr(tvm::RelayExpr const&)+0x76) [0x7feba3fb3a46]
        [bt] (6) /home/lisa/tvm/build/libtvm.so(tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>::InitVTable()::{lambda(tvm::runtime::ObjectRef const&, tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>*)#6}::_FUN(tvm::runtime::ObjectRef const&, tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>*)+0x2c) [0x7feba3e403ec]
        [bt] (5) /home/lisa/tvm/build/libtvm.so(tvm::relay::MixedModeMutator::VisitExpr_(tvm::relay::CallNode const*)+0x9e) [0x7feba3db5f6e]
        [bt] (4) /home/lisa/tvm/build/libtvm.so(tvm::relay::ForwardRewriter::Rewrite_(tvm::relay::CallNode const*, tvm::RelayExpr const&)+0xf97) [0x7feba3e137e7]
        [bt] (3) /home/lisa/tvm/build/libtvm.so(tvm::runtime::TypedPackedFunc<tvm::RelayExpr (tvm::relay::Call const&, tvm::runtime::Array<tvm::RelayExpr, void> const&, tvm::runtime::ObjectRef const&)>::AssignTypedLambda<tvm::RelayExpr (*)(tvm::relay::Call const&, tvm::runtime::Array<tvm::RelayExpr, void> const&, tvm::runtime::ObjectRef const&)>(tvm::RelayExpr (*)(tvm::relay::Call const&, tvm::runtime::Array<tvm::RelayExpr, void> const&, tvm::runtime::ObjectRef const&))::{lambda(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*)#1}::operator()(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*) const+0x349) [0x7feba3d61389]
        [bt] (2) /home/lisa/tvm/build/libtvm.so(tvm::RelayExpr tvm::relay::LayoutRewriter<tvm::relay::alter_op_layout::AlterTransformMemorizer>(tvm::relay::Call const&, tvm::runtime::Array<tvm::RelayExpr, void> const&, tvm::runtime::ObjectRef const&)+0xcd5) [0x7feba3d694e5]
        [bt] (1) /home/lisa/tvm/build/libtvm.so(tvm::RelayExprNode::checked_type() const+0x157) [0x7feba3cdf5e7]
        [bt] (0) /home/lisa/tvm/build/libtvm.so(+0x2702338) [0x7feba3cdd338]
        File "/home/lisa/tvm/include/tvm/ir/expr.h", line 476
    TVMError:
    ---------------------------------------------------------------
    An internal invariant was violated during the execution of TVM.
    Please read TVM's error reporting guidelines.
    More details can be found here: https://discuss.tvm.ai/t/error-reporting/7793.
    ---------------------------------------------------------------
    Check failed: checked_type_.defined() == false: internal error: the type checker has not populated the checked_type field for Var(x, ty=TensorType([1, 56, 56, 64], float32))
    ''',
    
    '''
    Traceback (most recent call last):
        File "/home/lisa/TVMfuzz/buggyFile2/6.py", line 173, in <module>
            F8ExZ=make_nat_expr(EHXnr,3)
        File "/home/lisa/tvm/python/tvm/relay/testing/nat.py", line 60, in make_nat_expr
            _, z, s = prelude.mod.get_type("nat")
        File "/home/lisa/tvm/python/tvm/ir/module.py", line 215, in get_type
            ty_var = self.get_global_type_var(name)
        File "/home/lisa/tvm/python/tvm/ir/module.py", line 193, in get_global_type_var
            return _ffi_api.Module_GetGlobalTypeVar(self, name)
        File "/home/lisa/tvm/python/tvm/_ffi/_ctypes/packed_func.py", line 237, in __call__
            raise get_last_ffi_error()
    tvm._ffi.base.TVMError: Traceback (most recent call last):
        [bt] (3) /home/lisa/tvm/build/libtvm.so(TVMFuncCall+0x63) [0x7f64c6c912a3]
        [bt] (2) /home/lisa/tvm/build/libtvm.so(std::_Function_handler<void (tvm::runtime::TVMArgs, tvm::runtime::TVMRetValue*), tvm::runtime::TypedPackedFunc<tvm::GlobalTypeVar (tvm::IRModule, tvm::runtime::String const&)>::AssignTypedLambda<tvm::runtime::Registry::set_body_method<tvm::IRModule, tvm::IRModuleNode, tvm::GlobalTypeVar, tvm::runtime::String const&, void>(tvm::GlobalTypeVar (tvm::IRModuleNode::*)(tvm::runtime::String const&) const)::{lambda(tvm::IRModule, tvm::runtime::String const&)#1}>(tvm::runtime::Registry::set_body_method<tvm::IRModule, tvm::IRModuleNode, tvm::GlobalTypeVar, tvm::runtime::String const&, void>(tvm::GlobalTypeVar (tvm::IRModuleNode::*)(tvm::runtime::String const&) const)::{lambda(tvm::IRModule, tvm::runtime::String const&)#1})::{lambda(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*)#1}>::_M_invoke(std::_Any_data const&, tvm::runtime::TVMArgs&&, tvm::runtime::TVMRetValue*&&)+0x1f0) [0x7f64c60df730]
        [bt] (1) /home/lisa/tvm/build/libtvm.so(tvm::IRModuleNode::GetGlobalTypeVar(tvm::runtime::String const&) const+0x139) [0x7f64c60ccd99]
        [bt] (0) /home/lisa/tvm/build/libtvm.so(+0x1f0e068) [0x7f64c60cc068]
        File "/home/lisa/tvm/src/ir/module.cc", line 156
    TVMError:
    ---------------------------------------------------------------
    An internal invariant was violated during the execution of TVM.
    Please read TVM's error reporting guidelines.
    More details can be found here: https://discuss.tvm.ai/t/error-reporting/7793.
    ---------------------------------------------------------------
        Check failed: it != global_type_var_map_.end() == false: Cannot find global type var nat in the Module
    ''',

    '''
    The Relay type checker is unable to show the following types match.
    In particular `int32` does not match `t`
    note: run with `TVM_BACKTRACE=1` environment variable to display a backtrace.
    ''',

    '''
    The Relay type checker is unable to show the following types match.
    In particular `ref(meta[IncompleteType][0])
    ` does not match `fn [c, c](c) -> c`
    The Relay type checker is unable to show the following types match.
    In particular `ref(meta[IncompleteType][0])
    ` does not match `fn [c, c](c) -> c`
    The Relay type checker is unable to show the following types match.
    In particular `ref(meta[IncompleteType][0])
    ` does not match `fn [c, c](c) -> c`
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    Traceback (most recent call last):
    File "/home/lisa/TVMfuzz/buggyFile2/2.py", line 171, in <module>
        tkIeS=run_opt_pass(AsPBS,Ac5bE)
    File "/home/lisa/TVMfuzz/buggyFile2/2.py", line 158, in run_opt_pass
        mod = seq(mod)
    File "/home/lisa/tvm/python/tvm/ir/transform.py", line 127, in __call__
        return _ffi_transform_api.RunPass(self, mod)
    File "/home/lisa/tvm/python/tvm/_ffi/_ctypes/packed_func.py", line 237, in __call__
        raise get_last_ffi_error()
    tvm.error.DiagnosticError: Traceback (most recent call last):
    [bt] (7) /home/lisa/tvm/build/libtvm.so(TVMFuncCall+0x63) [0x7fef562362a3]
    [bt] (6) /home/lisa/tvm/build/libtvm.so(+0x1f39ed4) [0x7fef5569ced4]
    [bt] (5) /home/lisa/tvm/build/libtvm.so(tvm::transform::SequentialNode::operator()(tvm::IRModule, tvm::transform::PassContext const&) const+0x32f) [0x7fef556993af]
    [bt] (4) /home/lisa/tvm/build/libtvm.so(tvm::transform::ModulePassNode::operator()(tvm::IRModule, tvm::transform::PassContext const&) const+0x1d4) [0x7fef5569c534]
    [bt] (3) /home/lisa/tvm/build/libtvm.so(+0x28dd442) [0x7fef56040442]
    [bt] (2) /home/lisa/tvm/build/libtvm.so(+0x28dc3c7) [0x7fef5603f3c7]
    [bt] (1) /home/lisa/tvm/build/libtvm.so(tvm::DiagnosticContext::Render()+0x231) [0x7fef5564d4f1]
    [bt] (0) /home/lisa/tvm/build/libtvm.so(+0x1eea0e8) [0x7fef5564d0e8]
    File "/home/lisa/tvm/src/ir/diagnostic.cc", line 105
    DiagnosticError: one or more error diagnostics were emitted, please check diagnostic render for output.
    ''',

    '''
    Traceback (most recent call last):
    File "/home/lisa/TVMfuzz/buggyFile2/39.py", line 128, in <module>
        check_kind(EK3h8)
    File "/home/lisa/tvm/python/tvm/relay/analysis/analysis.py", line 106, in check_kind
        return _ffi_api.check_kind(t)
    File "/home/lisa/tvm/python/tvm/_ffi/_ctypes/packed_func.py", line 237, in __call__
        raise get_last_ffi_error()
    tvm._ffi.base.TVMError: Traceback (most recent call last):
        [bt] (6) /home/lisa/tvm/build/libtvm.so(TVMFuncCall+0x63) [0x7f40a7b022a3]
        [bt] (5) /home/lisa/tvm/build/libtvm.so(+0x27292b8) [0x7f40a77582b8]
        [bt] (4) /home/lisa/tvm/build/libtvm.so(+0x272905e) [0x7f40a775805e]
        [bt] (3) /home/lisa/tvm/build/libtvm.so(tvm::relay::KindCheck(tvm::Type const&, tvm::IRModule const&, tvm::runtime::Optional<tvm::DiagnosticContext>)+0xb9) [0x7f40a7757989]
        [bt] (2) /home/lisa/tvm/build/libtvm.so(tvm::relay::KindChecker::VisitType_(tvm::TypeCallNode const*)+0x10a) [0x7f40a775ef9a]
        [bt] (1) /home/lisa/tvm/build/libtvm.so(tvm::relay::KindChecker::CheckKindMatches(tvm::Type const&, tvm::Type const&, tvm::TypeKind, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)+0x61c) [0x7f40a775c3ac]
        [bt] (0) /home/lisa/tvm/build/libtvm.so(+0x2728878) [0x7f40a7757878]
        File "/home/lisa/tvm/src/relay/analysis/kind_check.cc", line 54
    TVMError: Incorrect kind for a type call function. Type GlobalTypeVar(v1, 0) inside TypeCallNode(GlobalTypeVar(v1, 0), []) is of kind 0 but was expected to be 5
    ''',

    '''
    Traceback (most recent call last):
    File "/home/lisa/TVMfuzz/buggyFile2/38.py", line 1366, in <module>
        IsoSU=run_opt_pass(cfBFv,vOeTP)
    File "/home/lisa/TVMfuzz/buggyFile2/38.py", line 1361, in run_opt_pass
        mod = opt_pass(mod)
    File "/home/lisa/tvm/python/tvm/ir/transform.py", line 127, in __call__
        return _ffi_transform_api.RunPass(self, mod)
    File "/home/lisa/tvm/python/tvm/_ffi/_ctypes/packed_func.py", line 237, in __call__
        raise get_last_ffi_error()
    tvm._ffi.base.TVMError: Traceback (most recent call last):
        [bt] (8) /home/lisa/tvm/build/libtvm.so(tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>::InitVTable()::{lambda(tvm::runtime::ObjectRef const&, tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>*)#5}::_FUN(tvm::runtime::ObjectRef const&, tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>*)+0x2c) [0x7f3fe87e739c]
        [bt] (7) /home/lisa/tvm/build/libtvm.so(tvm::relay::ExprMutator::VisitExpr_(tvm::relay::FunctionNode const*)+0x55f) [0x7f3fe89527ff]
        [bt] (6) /home/lisa/tvm/build/libtvm.so(tvm::relay::MixedModeMutator::VisitExpr(tvm::RelayExpr const&)+0x1b1) [0x7f3fe8954211]
        [bt] (5) /home/lisa/tvm/build/libtvm.so(tvm::relay::MixedModeMutator::VisitLeaf(tvm::RelayExpr const&)+0x47) [0x7f3fe8953447]
        [bt] (4) /home/lisa/tvm/build/libtvm.so(tvm::relay::PostOrderRewriter::DispatchVisitExpr(tvm::RelayExpr const&)+0xff) [0x7f3fe895ad2f]
        [bt] (3) /home/lisa/tvm/build/libtvm.so(tvm::relay::ExprRewriter::InitVTable()::{lambda(tvm::runtime::ObjectRef const&, tvm::relay::ExprRewriter*, tvm::RelayExpr const&)#6}::_FUN(tvm::runtime::ObjectRef const&, tvm::relay::ExprRewriter*, tvm::RelayExpr const&)+0x2c) [0x7f3fe86a6bec]
        [bt] (2) /home/lisa/tvm/build/libtvm.so(tvm::relay::legalize::Legalizer::Rewrite_(tvm::relay::CallNode const*, tvm::RelayExpr const&)+0x7a0) [0x7f3fe87f2e60]
        [bt] (1) /home/lisa/tvm/build/libtvm.so(tvm::RelayExprNode::checked_type() const+0x157) [0x7f3fe86865e7]
        [bt] (0) /home/lisa/tvm/build/libtvm.so(+0x2702338) [0x7f3fe8684338]
    File "/home/lisa/tvm/include/tvm/ir/expr.h", line 476
    TVMError:
    ---------------------------------------------------------------
    An internal invariant was violated during the execution of TVM.
    Please read TVM's error reporting guidelines.
    More details can be found here: https://discuss.tvm.ai/t/error-reporting/7793.
    ---------------------------------------------------------------
        Check failed: checked_type_.defined() == false: internal error: the type checker has not populated the checked_type field for Var(x, ty=TensorType([1, 500, 500, 64], float32))
    ''',

    '''
    Traceback (most recent call last):
        File "/home/lisa/TVMfuzz/buggyFile2/32.py", line 705, in <module>
            verify_tile((2,3,4,),(3,0,1,))
        File "/home/lisa/TVMfuzz/buggyFile2/32.py", line 703, in verify_tile
            op_res = intrp.evaluate(func)(x_data)
        File "/home/lisa/tvm/python/tvm/relay/backend/interpreter.py", line 178, in evaluate
            return self._make_executor(expr)
        File "/home/lisa/tvm/python/tvm/relay/build_module.py", line 382, in _make_executor
            self.mod = InferType()(self.mod)
        File "/home/lisa/tvm/python/tvm/ir/transform.py", line 127, in __call__
            return _ffi_transform_api.RunPass(self, mod)
        File "/home/lisa/tvm/python/tvm/_ffi/_ctypes/packed_func.py", line 237, in __call__
            raise get_last_ffi_error()
    tvm._ffi.base.TVMError: Traceback (most recent call last):
        [bt] (7) /home/lisa/tvm/build/libtvm.so(TVMFuncCall+0x63) [0x7f7e810992a3]
        [bt] (6) /home/lisa/tvm/build/libtvm.so(+0x1f39ed4) [0x7f7e804ffed4]
        [bt] (5) /home/lisa/tvm/build/libtvm.so(tvm::transform::ModulePassNode::operator()(tvm::IRModule, tvm::transform::PassContext const&) const+0x1d4) [0x7f7e804ff534]
        [bt] (4) /home/lisa/tvm/build/libtvm.so(+0x28dd442) [0x7f7e80ea3442]
        [bt] (3) /home/lisa/tvm/build/libtvm.so(+0x28dc358) [0x7f7e80ea2358]
        [bt] (2) /home/lisa/tvm/build/libtvm.so(tvm::relay::TypeInferencer::Infer(tvm::GlobalVar, tvm::relay::Function)+0x75) [0x7f7e80ea1a45]
        [bt] (1) /home/lisa/tvm/build/libtvm.so(+0x1bdc8b1) [0x7f7e801a28b1]
        [bt] (0) /home/lisa/tvm/build/libtvm.so(+0x27418f8) [0x7f7e80d078f8]
        [bt] (8) /home/lisa/tvm/build/libtvm.so(+0x1f39ed4) [0x7f7e804ffed4]
        [bt] (7) /home/lisa/tvm/build/libtvm.so(tvm::transform::ModulePassNode::operator()(tvm::IRModule, tvm::transform::PassContext const&) const+0x1d4) [0x7f7e804ff534]
        [bt] (6) /home/lisa/tvm/build/libtvm.so(+0x28dd442) [0x7f7e80ea3442]
        [bt] (5) /home/lisa/tvm/build/libtvm.so(+0x28dc358) [0x7f7e80ea2358]
        [bt] (4) /home/lisa/tvm/build/libtvm.so(tvm::relay::TypeInferencer::Infer(tvm::GlobalVar, tvm::relay::Function)+0x75) [0x7f7e80ea1a45]
        [bt] (3) /home/lisa/tvm/build/libtvm.so(tvm::relay::TypeSolver::Solve()+0x45c) [0x7f7e80d0a2ec]
        [bt] (2) /home/lisa/tvm/build/libtvm.so(tvm::runtime::TypedPackedFunc<bool (tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>::AssignTypedLambda<bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>(bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&))::{lambda(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*)#1}::operator()(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*) const+0x557) [0x7f7e8055a747]
        [bt] (1) /home/lisa/tvm/build/libtvm.so(tvm::relay::TileRel(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)+0x72c) [0x7f7e80bfe0dc]
        [bt] (0) /home/lisa/tvm/build/libtvm.so(+0x262b918) [0x7f7e80bf1918]
    File "/home/lisa/tvm/src/relay/analysis/type_solver.cc", line 622
    TVMError:
    ---------------------------------------------------------------
    An internal invariant was violated during the execution of TVM.
    Please read TVM's error reporting guidelines.
    More details can be found here: https://discuss.tvm.ai/t/error-reporting/7793.
    ---------------------------------------------------------------
        Check failed: false == false: [10:14:03] /home/lisa/tvm/src/relay/op/tensor/transform.cc:1622:
    ---------------------------------------------------------------
    An internal invariant was violated during the execution of TVM.
    Please read TVM's error reporting guidelines.
    More details can be found here: https://discuss.tvm.ai/t/error-reporting/7793.
    ---------------------------------------------------------------

        Check failed: val->value > 0 (0 vs. 0) : Tile reps value should always be larger than 0, but get: 0
    ''',

    '''
    Traceback (most recent call last):
    File "/home/lisa/TVMfuzz/buggyFile2/26.py", line 153, in <module>
        quantize_test_driver(in_dtype=\'\'\'int32\'\'\',quant_args={\'\'\'out_zero_point\'\'\':UBKqL,\'\'\'out_scale\'\'\':wunQz},axis=0,out_dtype=\'\'\'uint8\'\'\',in_data=vIWjt,verify_output_data=vIWjt)
    File "/home/lisa/TVMfuzz/buggyFile2/26.py", line 143, in quantize_test_driver
        (graph, lib, params) = relay.build(mod, 'llvm', params=None)
    File "/home/lisa/tvm/python/tvm/relay/build_module.py", line 275, in build
        graph_json, mod, params = bld_mod.build(mod, target, target_host, params)
    File "/home/lisa/tvm/python/tvm/relay/build_module.py", line 138, in build
        self._build(mod, target, target_host)
    File "/home/lisa/tvm/python/tvm/_ffi/_ctypes/packed_func.py", line 237, in __call__
        raise get_last_ffi_error()
    tvm._ffi.base.TVMError: Traceback (most recent call last):
        [bt] (8) /home/lisa/tvm/build/libtvm.so(tvm::transform::Pass::operator()(tvm::IRModule) const+0x67) [0x7f9f6abf6ed7]
        [bt] (7) /home/lisa/tvm/build/libtvm.so(tvm::transform::SequentialNode::operator()(tvm::IRModule, tvm::transform::PassContext const&) const+0x32f) [0x7f9f6ad063af]
        [bt] (6) /home/lisa/tvm/build/libtvm.so(tvm::transform::SequentialNode::operator()(tvm::IRModule, tvm::transform::PassContext const&) const+0x27e) [0x7f9f6ad062fe]
        [bt] (5) /home/lisa/tvm/build/libtvm.so(tvm::transform::ModulePassNode::operator()(tvm::IRModule, tvm::transform::PassContext const&) const+0x1d4) [0x7f9f6ad09534]
        [bt] (4) /home/lisa/tvm/build/libtvm.so(+0x28dd442) [0x7f9f6b6ad442]
        [bt] (3) /home/lisa/tvm/build/libtvm.so(+0x28dc358) [0x7f9f6b6ac358]
        [bt] (2) /home/lisa/tvm/build/libtvm.so(tvm::relay::TypeInferencer::Infer(tvm::GlobalVar, tvm::relay::Function)+0x75) [0x7f9f6b6aba45]
        [bt] (1) /home/lisa/tvm/build/libtvm.so(+0x1bdc8b1) [0x7f9f6a9ac8b1]
        [bt] (0) /home/lisa/tvm/build/libtvm.so(+0x27418f8) [0x7f9f6b5118f8]
        [bt] (8) /home/lisa/tvm/build/libtvm.so(tvm::transform::SequentialNode::operator()(tvm::IRModule, tvm::transform::PassContext const&) const+0x27e) [0x7f9f6ad062fe]
        [bt] (7) /home/lisa/tvm/build/libtvm.so(tvm::transform::ModulePassNode::operator()(tvm::IRModule, tvm::transform::PassContext const&) const+0x1d4) [0x7f9f6ad09534]
        [bt] (6) /home/lisa/tvm/build/libtvm.so(+0x28dd442) [0x7f9f6b6ad442]
        [bt] (5) /home/lisa/tvm/build/libtvm.so(+0x28dc358) [0x7f9f6b6ac358]
        [bt] (4) /home/lisa/tvm/build/libtvm.so(tvm::relay::TypeInferencer::Infer(tvm::GlobalVar, tvm::relay::Function)+0x75) [0x7f9f6b6aba45]
        [bt] (3) /home/lisa/tvm/build/libtvm.so(tvm::relay::TypeSolver::Solve()+0x45c) [0x7f9f6b5142ec]
        [bt] (2) /home/lisa/tvm/build/libtvm.so(tvm::runtime::TypedPackedFunc<bool (tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>::AssignTypedLambda<bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)>(bool (*)(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&))::{lambda(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*)#1}::operator()(tvm::runtime::TVMArgs const&, tvm::runtime::TVMRetValue*) const+0x557) [0x7f9f6ad64747]
        [bt] (1) /home/lisa/tvm/build/libtvm.so(tvm::relay::qnn::QuantizeRel(tvm::runtime::Array<tvm::Type, void> const&, int, tvm::Attrs const&, tvm::TypeReporter const&)+0x26d) [0x7f9f6b7ec58d]
        [bt] (0) /home/lisa/tvm/build/libtvm.so(+0x2a1b0d8) [0x7f9f6b7eb0d8]
    File "/home/lisa/tvm/src/relay/analysis/type_solver.cc", line 622
    TVMError:
    ---------------------------------------------------------------
    An internal invariant was violated during the execution of TVM.
    Please read TVM's error reporting guidelines.
    More details can be found here: https://discuss.tvm.ai/t/error-reporting/7793.
    ---------------------------------------------------------------
        Check failed: false == false: [10:48:58] /home/lisa/tvm/src/relay/qnn/op/quantize.cc:49:
    ---------------------------------------------------------------
    An internal invariant was violated during the execution of TVM.
    Please read TVM's error reporting guidelines.
    More details can be found here: https://discuss.tvm.ai/t/error-reporting/7793.
    ---------------------------------------------------------------
        Check failed: input_dtype == DataType::Float(32) == false: Input type should be one of float32 but was int32
    ''',

    '''
    Traceback (most recent call last):
    File "/home/lisa/TVMfuzz/buggyFile2/19.py", line 151, in <module>
        Qi0Mu=random_bsr_matrix(239,128,32,1,0.1)
    NameError: name 'random_bsr_matrix' is not defined
    ''',

    '''
    error: a constructor with the name `Cons` was previously defined
    --> from_string:11:13
        |
    11  |              Cons(A, List[A]),
        |              ^^^^
    ''',

    '''
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    The type inference pass was unable to infer a type for this expression.
    This usually occurs when an operator call is under constrained in some way, check other reported errors for hints of what may of happened.
    Traceback (most recent call last):
    File "/home/lisa/TVMfuzz/buggyFile2/7.py", line 3728, in <module>
        LZ2cL=KEkqH.partition(mcksQ)
    File "/home/lisa/tvm/python/tvm/relay/dataflow_pattern/__init__.py", line 171, in partition
        return partition(self, expr, attrs, check)
    File "/home/lisa/tvm/python/tvm/relay/dataflow_pattern/__init__.py", line 814, in partition
        return ffi.partition(pattern, expr, attrs, check)
    File "/home/lisa/tvm/python/tvm/_ffi/_ctypes/packed_func.py", line 237, in __call__
        raise get_last_ffi_error()
    tvm.error.DiagnosticError: Traceback (most recent call last):
        [bt] (8) /home/lisa/tvm/build/libtvm.so(tvm::relay::DFPatternMatcher::VisitDFPattern_(tvm::relay::DominatorPatternNode const*, tvm::RelayExpr const&)+0x1c) [0x7fa5bd868fec]
        [bt] (7) /home/lisa/tvm/build/libtvm.so(tvm::relay::DFPatternMatcher::VisitDFPattern(tvm::relay::DFPattern const&, tvm::RelayExpr const&)+0x216) [0x7fa5bd8678b6]
        [bt] (6) /home/lisa/tvm/build/libtvm.so(tvm::relay::DFPatternMatcher::VisitDFPattern_(tvm::relay::ShapePatternNode const*, tvm::RelayExpr const&)+0x3b) [0x7fa5bd86348b]
        [bt] (5) /home/lisa/tvm/build/libtvm.so(tvm::relay::InferType(tvm::RelayExpr const&)+0x17b) [0x7fa5bd86302b]
        [bt] (4) /home/lisa/tvm/build/libtvm.so(tvm::transform::ModulePassNode::operator()(tvm::IRModule, tvm::transform::PassContext const&) const+0x1d4) [0x7fa5bce01534]
        [bt] (3) /home/lisa/tvm/build/libtvm.so(+0x28dd442) [0x7fa5bd7a5442]
        [bt] (2) /home/lisa/tvm/build/libtvm.so(+0x28dc3c7) [0x7fa5bd7a43c7]
        [bt] (1) /home/lisa/tvm/build/libtvm.so(tvm::DiagnosticContext::Render()+0x231) [0x7fa5bcdb24f1]
        [bt] (0) /home/lisa/tvm/build/libtvm.so(+0x1eea0e8) [0x7fa5bcdb20e8]
    File "/home/lisa/tvm/src/ir/diagnostic.cc", line 105
    DiagnosticError: one or more error diagnostics were emitted, please check diagnostic render for output.
    ''',

    '''
    Traceback (most recent call last):
    File "/home/lisa/TVMfuzz/buggyFile2/1.py", line 275, in <module>
        q3ir3=pD1WT(nWW5C)
    File "/home/lisa/tvm/python/tvm/ir/transform.py", line 127, in __call__
        return _ffi_transform_api.RunPass(self, mod)
    File "/home/lisa/tvm/python/tvm/_ffi/_ctypes/packed_func.py", line 237, in __call__
        raise get_last_ffi_error()
    tvm._ffi.base.TVMError: Traceback (most recent call last):
        [bt] (8) /home/lisa/tvm/build/libtvm.so(tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>::InitVTable()::{lambda(tvm::runtime::ObjectRef const&, tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>*)#5}::_FUN(tvm::runtime::ObjectRef const&, tvm::relay::ExprFunctor<tvm::RelayExpr (tvm::RelayExpr const&)>*)+0x2c) [0x7f11114b739c]
        [bt] (7) /home/lisa/tvm/build/libtvm.so(tvm::relay::ExprMutator::VisitExpr_(tvm::relay::FunctionNode const*)+0x55f) [0x7f11116227ff]
        [bt] (6) /home/lisa/tvm/build/libtvm.so(tvm::relay::MixedModeMutator::VisitExpr(tvm::RelayExpr const&)+0x1b1) [0x7f1111624211]
        [bt] (5) /home/lisa/tvm/build/libtvm.so(tvm::relay::MixedModeMutator::VisitLeaf(tvm::RelayExpr const&)+0x47) [0x7f1111623447]
        [bt] (4) /home/lisa/tvm/build/libtvm.so(tvm::relay::PostOrderRewriter::DispatchVisitExpr(tvm::RelayExpr const&)+0xff) [0x7f111162ad2f]
        [bt] (3) /home/lisa/tvm/build/libtvm.so(tvm::relay::ExprRewriter::InitVTable()::{lambda(tvm::runtime::ObjectRef const&, tvm::relay::ExprRewriter*, tvm::RelayExpr const&)#6}::_FUN(tvm::runtime::ObjectRef const&, tvm::relay::ExprRewriter*, tvm::RelayExpr const&)+0x2c) [0x7f1111376bec]
        [bt] (2) /home/lisa/tvm/build/libtvm.so(tvm::relay::legalize::Legalizer::Rewrite_(tvm::relay::CallNode const*, tvm::RelayExpr const&)+0x7a0) [0x7f11114c2e60]
        [bt] (1) /home/lisa/tvm/build/libtvm.so(tvm::RelayExprNode::checked_type() const+0x157) [0x7f11113565e7]
        [bt] (0) /home/lisa/tvm/build/libtvm.so(+0x2702338) [0x7f1111354338]
    File "/home/lisa/tvm/include/tvm/ir/expr.h", line 476
    TVMError:
    ---------------------------------------------------------------
    An internal invariant was violated during the execution of TVM.
    Please read TVM's error reporting guidelines.
    More details can be found here: https://discuss.tvm.ai/t/error-reporting/7793.
    ---------------------------------------------------------------
        Check failed: checked_type_.defined() == false: internal error: the type checker has not populated the checked_type field for Var(data, ty=TensorType([10, 3], uint8))
    ''',
]

bugid = 1