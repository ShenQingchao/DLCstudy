import tvm
from tvm import te
import numpy as np
from tvm import relay
from tvm.relay import memory_alloc


def check_memory_plan(func, check_fn):
    # Build Module
    mod = tvm.IRModule().from_expr(func)

    # Convert arguments.
    args = []
    for param in func.params:
        param = param.type_annotation
        sh = [int(sh) for sh in param.shape]
        data = np.random.rand(*sh).astype(param.dtype)
        args.append(tvm.nd.array(data))

    # Compute without memory planning.
    ex = relay.create_executor("vm", mod)
    no_plan_result = ex.evaluate(mod["main"])(*args)

    # Compute with memory planning.
    with tvm.transform.PassContext(opt_level=1, disabled_pass=["MemoryPlan"]):
        plan_result = ex.evaluate(mod["main"])(*args)

    # Compute Python result.
    py_res = check_fn(*[arg.asnumpy() for arg in args])

    # First check that the two VM results agree.
    np.testing.assert_allclose(no_plan_result.asnumpy(), plan_result.asnumpy())

    # Finally check that the results match the Python result.
    np.testing.assert_allclose(plan_result.asnumpy(), py_res)


def storage_type(mod):
    return relay.TypeCall(mod.get_global_type_var("Storage"), [])


def test_tyck_alloc_storage():
    mod = tvm.IRModule()
    mod.import_from_std("core.rly")


def test_tyck_alloc_tensor():
    mod = tvm.IRModule()
    mod.import_from_std("core.rly")
    sto = relay.Var("x", storage_type(mod))
    sh = relay.const(np.array([1, 2]), dtype="int64")
    at = relay.op.memory.alloc_tensor(sto, relay.const(0, dtype="int64"), sh)
    mod["main"] = relay.Function([sto], at)
    relay.transform.InferType()(mod)


def check_add(x):
    return x + x


def test_add():
    x = relay.var("x", shape=(2,))
    z = x + x
    func = relay.Function(
        [
            x,
        ],
        z,
    )
    check_memory_plan(func, check_add)


def check_add_sub(x, y):
    z = x + x
    return z - y


def test_add_sub():
    x = relay.var("x", shape=(10,))
    y = relay.var("y", shape=(10,))
    z = x + x
    z = z - y
    func = relay.Function([x, y], z)
    check_memory_plan(func, check_add_sub)


def check_no_fuse(x, y, w):
    z = x + y
    return np.matmul(z, np.transpose(w))


def test_no_fuse():
    x = relay.var("x", shape=(5, 1))
    y = relay.var("y", shape=(5, 1))
    w = relay.var("w", shape=(5, 1))
    z = x + y
    out = relay.op.nn.dense(z, w)
    func = relay.Function([x, y, w], out)
    check_memory_plan(func, check_no_fuse)
