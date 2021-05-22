import numpy as np
import tvm
from tvm import te
import tvm.testing
from tvm import nd
from tvm import relay
from tvm.runtime import container
from tvm.relay.backend.interpreter import RefValue, ConstructorValue
from tvm.relay.scope_builder import ScopeBuilder
from tvm.relay import testing, create_executor

def test_tuple_value():
    tv = container.tuple_object([relay.const(1), relay.const(2), relay.const(3)])
    np.testing.assert_allclose(tv[0].data.asnumpy(), 1)
    np.testing.assert_allclose(tv[1].data.asnumpy(), 2)
    np.testing.assert_allclose(tv[2].data.asnumpy(), 3)


def test_tuple_getitem():
    two = relay.add(relay.const(1), relay.const(1))
    func = relay.Function([], relay.TupleGetItem(relay.Tuple([relay.const(1), relay.const(2)]), 0))

def test_id():
    x = relay.var("x", "float32")
    ident = relay.Function([x], x)
    one = np.array(1.0, "float32")

def test_add_const():
    two = relay.add(relay.const(1), relay.const(1))
    func = relay.Function([], two)

def test_mul_param():
    x = relay.var("x", shape=(10, 10))
    y = relay.var("y", shape=(1, 10))
    func = relay.Function([x, y], relay.multiply(x, y))
    x_data = np.random.rand(10, 10).astype("float32")
    y_data = np.random.rand(1, 10).astype("float32")
 
def test_equal():
    i = relay.var("i", shape=[], dtype="int32")
    j = relay.var("i", shape=[], dtype="int32")
    z = relay.equal(i, j)
    func = relay.Function([i, j], z, ret_type=relay.TensorType([], "bool"))
    i_data = relay.const(0, "int32")
    j_data = relay.const(0, "int32")

def test_subtract():
    i = relay.var("i", shape=[], dtype="int32")
    sub = relay.subtract(i, relay.const(1, dtype="int32"))
    func = relay.Function([i], sub, ret_type=relay.TensorType([], "int32"))
    i_data = np.array(1, dtype="int32")

def test_ref():
    mod = tvm.IRModule()
    three_with_ref = relay.GlobalVar("three_with_ref")
    i = relay.Var("i")
    iv = relay.Var("iv")
    u = relay.Var("u")
    uv = relay.Var("uv")
    body = relay.add(iv, uv)
    body = relay.Let(uv, relay.RefRead(i), body)
    body = relay.Let(u, relay.RefWrite(i, relay.const(2)), body)
    body = relay.Let(iv, relay.RefRead(i), body)
    body = relay.Let(i, relay.RefCreate(relay.const(1)), body)
    mod[three_with_ref] = relay.Function([], body)

def test_binds():
    x = relay.var("x")
    y = relay.add(x, x)
    intrp = create_executor("debug")
    xx = np.ones((10, 20))
    res = intrp.evaluate(y, binds={x: xx}).asnumpy()
    tvm.testing.assert_allclose(xx + xx, res)

def test_kwargs_params():
    x = relay.var("x", shape=(1, 10))
    y = relay.var("y", shape=(1, 10))
    z = relay.var("z", shape=(1, 10))
    f = relay.Function([x, y, z], x + y + z)
    x_data = np.random.rand(1, 10).astype("float32")
    y_data = np.random.rand(1, 10).astype("float32")
    z_data = np.random.rand(1, 10).astype("float32")
    params = {"y": y_data, "z": z_data}
    intrp = create_executor("debug")
    res = intrp.evaluate(f)(x_data, **params)
    tvm.testing.assert_allclose(res.asnumpy(), x_data + y_data + z_data)

def test_tuple_passing():
    x = relay.var(
        "x",
        type_annotation=relay.ty.TupleType(
            [relay.ty.TensorType((), "int64"), relay.ty.TensorType((), "int64")]
        ),
    )

    fn = relay.Function([x], relay.expr.TupleGetItem(x, 0))
    mod = tvm.IRModule({})
    gv = relay.GlobalVar("main")
    mod[gv] = fn
    mod = relay.transform.InferType()(mod)

    ctx = tvm.cpu()
    target = tvm.target.Target("llvm")
    exec = relay.create_executor(mod=mod, ctx=ctx, target=target)
    f = exec.evaluate(gv)
    # First use a Python tuple.
    out = f((10, 8))
    tvm.testing.assert_allclose(out.asnumpy(), np.array(10))
    # Second use a tuple value.
    value_tuple = container.tuple_object([nd.array(np.array(11)), nd.array(np.array(12))])
    out = f(value_tuple)
    tvm.testing.assert_allclose(out.asnumpy(), np.array(11))