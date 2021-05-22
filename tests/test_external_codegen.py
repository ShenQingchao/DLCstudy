import os
import sys
import numpy as np

import tvm
from tvm import te
import tvm.relay.testing
import tvm.relay.transform
from tvm import relay
from tvm import runtime

def set_external_func_attr(func, compiler, ext_symbol):
    func = func.with_attr("Primitive", tvm.tir.IntImm("int32", 1))
    func = func.with_attr("Compiler", compiler)
    func = func.with_attr("global_symbol", ext_symbol)
    return func


def test_multi_node_subgraph():
    x = relay.var("x", shape=(10, 10))
    w0 = relay.var("w0", shape=(10, 10))
    w1 = relay.var("w1", shape=(10, 10))
    w2 = relay.var("w2", shape=(10, 10))
    w3 = relay.var("w3", shape=(10, 10))
    w4 = relay.var("w4", shape=(10, 10))
    w5 = relay.var("w5", shape=(10, 10))
    w6 = relay.var("w6", shape=(10, 10))
    w7 = relay.var("w7", shape=(10, 10))

    # subgraph0
    x0 = relay.var("x0", shape=(10, 10))
    w00 = relay.var("w00", shape=(10, 10))
    w01 = relay.var("w01", shape=(10, 10))
    w02 = relay.var("w02", shape=(10, 10))
    z00 = relay.add(x0, w00)
    p00 = relay.subtract(z00, w01)
    q00 = relay.multiply(p00, w02)
    subgraph0 = relay.Function([x0, w00, w01, w02], q00)
    subgraph0 = set_external_func_attr(subgraph0, "ccompiler", "ccompiler_0")
    call0 = relay.Call(subgraph0, [x, w0, w1, w2])

    # subgraph1
    x1 = relay.var("x1", shape=(10, 10))
    w10 = relay.var("w10", shape=(10, 10))
    w11 = relay.var("w11", shape=(10, 10))
    w12 = relay.var("w12", shape=(10, 10))
    z10 = relay.add(x1, w10)
    p10 = relay.subtract(z10, w11)
    q10 = relay.multiply(p10, w12)
    subgraph1 = relay.Function([x1, w10, w11, w12], q10)
    subgraph1 = set_external_func_attr(subgraph1, "ccompiler", "ccompiler_1")
    call1 = relay.Call(subgraph1, [x, w3, w4, w5])

    # Other parts on TVM
    z2 = relay.add(x, w6)
    q2 = relay.subtract(z2, w7)

    r = relay.concatenate((call0, call1, q2), axis=0)
    f = relay.Function([x, w0, w1, w2, w3, w4, w5, w6, w7], r)
    mod = tvm.IRModule()
    mod["main"] = f
    mod = relay.transform.InferType()(mod)

    x_data = np.random.rand(10, 10).astype("float32")
    w_data = []
    for _ in range(8):
        w_data.append(np.random.rand(10, 10).astype("float32"))


def test_extern_gcc_single_op():
    x = relay.var("x", shape=(8, 8))
    y = relay.var("y", shape=(8, 8))

    x0 = relay.var("x0", shape=(8, 8))
    y0 = relay.var("y0", shape=(8, 8))
    z = x0 + y0
    f = relay.Function([x0, y0], z)
    f = set_external_func_attr(f, "ccompiler", "ccompiler_0")
    call = relay.Call(f, [x, y])
    mod = tvm.IRModule.from_expr(call)
    x_data = np.random.rand(8, 8).astype("float32")
    y_data = np.random.rand(8, 8).astype("float32")



def test_extern_gcc_single_op_int():
    x = relay.var("x", shape=(8, 8), dtype="int32")
    y = relay.var("y", shape=(8, 8), dtype="int32")

    x0 = relay.var("x0", shape=(8, 8), dtype="int32")
    y0 = relay.var("y0", shape=(8, 8), dtype="int32")
    z = x0 + y0
    f = relay.Function([x0, y0], z)
    f = set_external_func_attr(f, "ccompiler", "ccompiler_0")
    call = relay.Call(f, [x, y])
    mod = tvm.IRModule.from_expr(call)
    x_data = np.random.rand(8, 8).astype("int32")
    y_data = np.random.rand(8, 8).astype("int32")



def test_extern_gcc():
    x = relay.var("x", shape=(2, 2))
    y = relay.var("y", shape=(2, 2))

    # subgraph for mul
    x0 = relay.var("x0", shape=(2, 2))
    y0 = relay.var("y0", shape=(2, 2))
    mul = x0 * y0
    mul = relay.Function([x0, y0], mul)
    mul = set_external_func_attr(mul, "ccompiler", "ccompiler_2")
    call_mul = relay.Call(mul, [y, y])

    # subgraph for add
    x1 = relay.var("x1", shape=(2, 2))
    y1 = relay.var("y1", shape=(2, 2))
    add = x1 + y1
    add = relay.Function([x1, y1], add)
    add = set_external_func_attr(add, "ccompiler", "ccompiler_1")
    call_add = relay.Call(add, [x, x])

    # subgraph for sub
    x2 = relay.var("x2", shape=(2, 2))
    y2 = relay.var("y2", shape=(2, 2))
    sub = x2 - y2
    sub = relay.Function([x2, y2], sub)
    sub = set_external_func_attr(sub, "ccompiler", "ccompiler_0")
    call_sub = relay.Call(sub, [call_mul, call_add])
    mod = tvm.IRModule.from_expr(call_sub)

    x_data = np.random.rand(2, 2).astype("float32")
    y_data = np.random.rand(2, 2).astype("float32")



def test_extern_dnnl():
    # if not tvm.get_global_func("relay.ext.dnnl", True):
    #     print("skip because DNNL codegen is not available")
    #     return

    dtype = "float32"
    ishape = (1, 32, 14, 14)
    w1shape = (32, 1, 3, 3)
    data0 = relay.var("data0", shape=(ishape), dtype=dtype)
    weight0 = relay.var("weight0", shape=(w1shape), dtype=dtype)

    data1 = relay.var("data0", shape=(ishape), dtype=dtype)
    weight1 = relay.var("weight0", shape=(w1shape), dtype=dtype)
    weight2 = relay.var("weight1", shape=(w1shape), dtype=dtype)
    depthwise_conv2d_1 = relay.nn.conv2d(
        data1, weight1, kernel_size=(3, 3), padding=(1, 1), groups=32
    )
    depthwise_conv2d_2 = relay.nn.conv2d(
        depthwise_conv2d_1, weight2, kernel_size=(3, 3), padding=(1, 1), groups=32
    )
    out = relay.add(depthwise_conv2d_1, depthwise_conv2d_2)

    f = relay.Function([data1, weight1, weight2], out)
    ref_mod = tvm.IRModule()
    ref_mod["main"] = f

    f = set_external_func_attr(f, "dnnl", "dnnl_0")
    call = relay.Call(f, [data0, weight0, weight0])
    mod = tvm.IRModule.from_expr(call)

    i_data = np.random.uniform(0, 1, ishape).astype(dtype)
    w_data = np.random.uniform(0, 1, w1shape).astype(dtype)

    ref_ex = relay.create_executor("graph", mod=ref_mod, ctx=tvm.cpu())
    ref_res = ref_ex.evaluate()(i_data, w_data, w_data)

def test_extern_dnnl_const():
    dtype = "float32"
    ishape = (1, 32, 14, 14)
    w1shape = (32, 1, 3, 3)
    data0 = relay.var("data0", shape=(ishape), dtype=dtype)
    w_data = np.random.uniform(0, 1, w1shape).astype(dtype)

    data1 = relay.var("data0", shape=(ishape), dtype=dtype)
    weight1 = relay.const(w_data, dtype=dtype)
    weight2 = relay.const(w_data, dtype=dtype)
    depthwise_conv2d_1 = relay.nn.conv2d(
        data1, weight1, kernel_size=(3, 3), padding=(1, 1), groups=32
    )
    depthwise_conv2d_2 = relay.nn.conv2d(
        depthwise_conv2d_1, weight2, kernel_size=(3, 3), padding=(1, 1), groups=32
    )
    out = relay.add(depthwise_conv2d_1, depthwise_conv2d_2)

    f = relay.Function([data1], out)
    ref_mod = tvm.IRModule()
    ref_mod["main"] = f

    f = set_external_func_attr(f, "dnnl", "dnnl_0")
    call = relay.Call(f, [data0])
    mod = tvm.IRModule.from_expr(call)

    i_data = np.random.uniform(0, 1, ishape).astype(dtype)

    ref_ex = relay.create_executor("graph", mod=ref_mod, ctx=tvm.cpu())
    ref_res = ref_ex.evaluate()(i_data)

