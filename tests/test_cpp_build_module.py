import numpy as np
import tvm
from tvm import te
from tvm import relay
from tvm.contrib.nvcc import have_fp16
import tvm.testing

def test_basic_build():
    tgt = "llvm"
    ctx = tvm.cpu()
    # func
    a = relay.var("a", dtype="float32", shape=(16, 8))
    b = relay.var("b", dtype="float32", shape=(8, 8))
    c = relay.var("c", dtype="float32", shape=(16, 8))
    x = relay.nn.dense(a, b)
    y = relay.nn.relu(x)
    z = y + c
    func = relay.Function([a, b, c], z)
    A = tvm.nd.array(np.random.uniform(-1, 1, (16, 8)).astype("float32"), ctx=ctx)
    B = tvm.nd.array(np.random.uniform(-1, 1, (8, 8)).astype("float32"), ctx=ctx)
    C = tvm.nd.array(np.random.uniform(-1, 1, (16, 8)).astype("float32"), ctx=ctx)
    params = {"b": B, "c": C}
    # build
    targets = {tvm.tir.IntImm("int32", ctx.device_type): tgt}
    mod = tvm.IRModule.from_expr(func)
    func_in_mod = mod["main"]
    assert mod["main"] == func_in_mod, "cannot compare function to itself"

    lib = relay.build(mod, targets, "llvm", params=params)
    assert mod["main"] == func_in_mod, "relay.build changed module in-place"

    # test
    rt = tvm.contrib.graph_runtime.GraphModule(lib["default"](ctx))
    rt.set_input("a", A)
    rt.run()
    out = rt.get_output(0)

    np.testing.assert_allclose(
        out.asnumpy(),
        np.maximum(np.dot(A.asnumpy(), B.asnumpy().T), 0) + C.asnumpy(),
        atol=1e-5,
        rtol=1e-5,
    )


@tvm.testing.requires_cuda
def test_fp16_build():
    dtype = "float16"

    ctx = tvm.gpu(0)
    x = relay.var("x", dtype=dtype, shape=(4, 4))
    y = relay.var("y", dtype=dtype, shape=(4, 4))
    z = x + y
    func = relay.Function([x, y], z)
    X = tvm.nd.array(np.random.uniform(-1, 1, (4, 4)).astype(dtype), ctx=ctx)
    Y = tvm.nd.array(np.random.uniform(-1, 1, (4, 4)).astype(dtype), ctx=ctx)
    params = {
        "x": X,
        "y": Y,
    }

    # build
    g_json, mmod, params = relay.build(func, "cuda", params=params)

    # test
    rt = tvm.contrib.graph_runtime.create(g_json, mmod, ctx)
    rt.load_params(relay.save_param_dict(params))
    rt.run()
    out = rt.get_output(0)

    np.testing.assert_allclose(out.asnumpy(), X.asnumpy() + Y.asnumpy(), atol=1e-5, rtol=1e-5)


# @tvm.testing.parametrize_targets("llvm", "cuda")
def test_fp16_conversion():
    target = 'llvm'
    ctx = tvm.cpu()

    n = 10

    for (src, dst) in [("float32", "float16"), ("float16", "float32")]:
        x = relay.var("x", relay.TensorType((n,), src))
        y = x.astype(dst)
        func = relay.Function([x], y)

        # init input
        X = tvm.nd.array(n * np.random.randn(n).astype(src) - n / 2)

        # build
        with tvm.transform.PassContext(opt_level=1):
            g_json, mmod, params = relay.build(tvm.IRModule.from_expr(func), target)

        # test
        rt = tvm.contrib.graph_runtime.create(g_json, mmod, ctx)
        rt.set_input("x", X)
        rt.run()
        out = rt.get_output(0)

        np.testing.assert_allclose(out.asnumpy(), X.asnumpy().astype(dst), atol=1e-5, rtol=1e-5)


