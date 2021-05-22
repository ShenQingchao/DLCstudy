import tvm
from tvm.ir import IRModule
from tvm import relay
from tvm.relay.transform import FastMath


def test_exp():
    x = relay.var("x", shape=(1, 16, 16, 16), dtype="float32")
    y = relay.exp(x)
    func = relay.Function([x], y)
    mod = tvm.IRModule.from_expr(func)

    fast_mod = FastMath()(mod)
    assert "fast_exp" in fast_mod.astext()

    # Check that FastMath option works for relay.build.
    with tvm.transform.PassContext(opt_level=3, required_pass=["FastMath"]):
        fast_mod = relay.optimize(mod, target="llvm", params=None)
    assert "fast_exp" in fast_mod[0].astext()


def test_tanh():
    x = relay.var("x", shape=(1, 16, 16, 16), dtype="float32")
    y = relay.tanh(x)
    func = relay.Function([x], y)
    mod = tvm.IRModule.from_expr(func)

    fast_mod = FastMath()(mod)
    assert "fast_tanh" in fast_mod.astext()

    # Check that FastMath option works for relay.build.
    with tvm.transform.PassContext(opt_level=3, required_pass=["FastMath"]):
        fast_mod = relay.optimize(mod, target="llvm", params=None)
    assert "fast_tanh" in fast_mod[0].astext()


def test_erf():
    x = relay.var("x", shape=(1, 16, 16, 16), dtype="float32")
    y = relay.erf(x)
    func = relay.Function([x], y)
    mod = tvm.IRModule.from_expr(func)

    fast_mod = FastMath()(mod)
    assert "fast_erf" in fast_mod.astext()

    # Check that FastMath option works for relay.build.
    with tvm.transform.PassContext(opt_level=3, required_pass=["FastMath"]):
        fast_mod = relay.optimize(mod, target="llvm", params=None)
    assert "fast_erf" in fast_mod[0].astext()