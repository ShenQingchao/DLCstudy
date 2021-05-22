# v0.7 Type Problem High-Level IR Transformation fixed
import tvm.testing
from tvm.relay.analysis import detect_feature
import tvm.relay.transform as transform
from tvm.relay import create_executor
from tvm.relay.analysis import check_basic_block_normal_form
import tvm.topi.testing
import numpy as np
from tvm.tir.expr import *
from tvm.relay import transform
import tvm.relay.testing
from tvm.relay import op
from tvm import relay
from tvm.relay.testing import run_opt_pass
from tvm.relay.analysis import Feature
import tvm
from tvm.relay.prelude import Prelude
from tvm.relay.testing import count
import tvm.relay as relay
import tvm.relay.transform
from tvm.relay.dataflow_pattern import *
from tvm.relay.testing import Prelude

def run_opt_pass(expr, passes):
    passes = (passes if isinstance(passes, list) else [passes])
    mod = tvm.IRModule.from_expr(expr)
    seq = tvm.transform.Sequential(passes)
    with tvm.transform.PassContext(opt_level=3):
        mod = seq(mod)
    entry = mod['main']
    return (entry if isinstance(expr, relay.Function) else entry.body)


def run_opt_pass(expr, passes):
    passes = (passes if isinstance(passes, list) else [passes])
    mod = tvm.IRModule.from_expr(expr)
    seq = tvm.transform.Sequential(passes)
    with tvm.transform.PassContext(opt_level=3):
        mod = seq(mod)
    entry = mod['main']
    return (entry if isinstance(expr, relay.Function) else entry.body)


def check_eval(expr, expected_result, mod=None, rtol=1e-07):
    ctx = tvm.context('llvm', 0)
    intrp = create_executor(mod=mod, ctx=ctx, target='llvm')
    result = intrp.evaluate(expr)
    np.testing.assert_allclose(result.asnumpy(), expected_result, rtol=rtol)


def test_no_explicit_bind():
    x = relay.const(1)
    y = op.add(x, x)
    z = op.add(y, y)
    f = relay.Function([], op.add(z, z))
    '\n    fn () {\n      %0 = add(1, 1);\n      %1 = add(%0, %0);\n      add(%1, %1)\n    }\n    '
    assert (not (Feature.fLet in detect_feature(f)))
    bblock = run_opt_pass(f, transform.ToBasicBlockNormalForm())
    assert (Feature.fLet not in detect_feature(bblock))
    check_eval(f(), 8.0)
    check_eval(bblock(), 8.0)
    check_basic_block_normal_form(bblock)


def test_top_level_nested_if():
    x = relay.var('x', shape=(), dtype='bool')
    y = relay.var('y', shape=(), dtype='float32')
    z = relay.var('z', shape=(), dtype='float32')
    cond_t = relay.const(True)
    cond_f = relay.const(False)
    one = relay.const(1, dtype='float32')
    three = relay.const(3, dtype='float32')
    y2 = relay.add(y, y)
    z2 = relay.add(z, z)
    true_branch = relay.If(cond_t, relay.add(z2, y2), relay.add(three, y2))
    false_branch = relay.If(cond_f, z2, one)
    body = relay.If(x, true_branch, false_branch)
    '\n    free_var %x: bool\n    if (%x) {\n      if (True) {\n        free_var %z: float32\n        %0 = add(%z, %z);\n        free_var %y: float32\n        %1 = add(%y, %y);\n        add(%0, %1)\n      } else {\n        add(3f, %1)\n      }\n    } else {\n      if (False) {\n        %0\n      } else {\n        1f\n      }\n    }\n    '

    def expected():
        x = relay.var('x', shape=(), dtype='bool')
        y = relay.var('y', shape=(), dtype='float32')
        z = relay.var('z', shape=(), dtype='float32')
        cond_t = relay.const(True)
        cond_f = relay.const(False)
        one = relay.const(1, dtype='float32')
        three = relay.const(3, dtype='float32')
        y2 = relay.var('y2')
        z2 = relay.var('z2')
        true_branch = relay.If(cond_t, relay.add(z2, y2), relay.add(three, y2))
        true_branch = relay.Let(y2, relay.add(y, y), true_branch)
        false_branch = relay.If(cond_f, z2, one)
        body = relay.If(x, true_branch, false_branch)
        body = relay.Let(z2, relay.add(z, z), body)
        return body
    bblock = run_opt_pass(body, [transform.ToBasicBlockNormalForm()])
    '\n    free_var %z: float32\n    let %x: float32 = add(%z, %z) /* ty=float32 */;\n    free_var %x1: bool\n    if (%x1) {\n      free_var %y: float32\n      let %x2: float32 = add(%y, %y) /* ty=float32 */;\n      if (True /* ty=bool */) {\n        add(%x, %x2) /* ty=float32 */\n      } else {\n        add(3f /* ty=float32 */, %x2) /* ty=float32 */\n      }\n    } else {\n      if (False /* ty=bool */) {\n        %x\n      } else {\n        1f /* ty=float32 */\n      }\n    }\n    '
    expected_output = run_opt_pass(expected(), transform.InferType())
    assert tvm.ir.structural_equal(bblock, expected_output, map_free_vars=True)


def test_nested_if():
    x = relay.var('x', shape=(), dtype='bool')
    y = relay.var('y', shape=(), dtype='float32')
    cond_t = relay.const(True)
    cond_f = relay.const(False)
    one = relay.const(1, dtype='float32')
    two = relay.const(2, dtype='float32')
    three = relay.const(3, dtype='float32')
    y2 = relay.add(y, y)
    true_branch = relay.If(cond_t, y2, relay.add(three, y2))
    false_branch = relay.If(cond_f, two, one)
    body = relay.If(x, true_branch, false_branch)
    '\n    free_var %x: bool\n    if (%x) {\n      if (True) {\n        free_var %y: float32\n        %0 = add(%y, %y);\n        %0\n      } else {\n        add(3f, %0)\n      }\n    } else {\n      if (False) {\n        2f\n      } else {\n        1f\n      }\n    }\n    '

    def expected():
        x = relay.var('x', shape=(), dtype='bool')
        y = relay.var('y', shape=(), dtype='float32')
        cond_t = relay.const(True)
        cond_f = relay.const(False)
        one = relay.const(1, dtype='float32')
        two = relay.const(2, dtype='float32')
        three = relay.const(3, dtype='float32')
        y2 = relay.var('y2')
        true_branch = relay.If(cond_t, y2, relay.add(three, y2))
        true_branch = relay.Let(y2, relay.add(y, y), true_branch)
        false_branch = relay.If(cond_f, two, one)
        body = relay.If(x, true_branch, false_branch)
        return body
    bblock = run_opt_pass(body, [transform.ToBasicBlockNormalForm()])
    '\n    free_var %x: bool\n    if (%x) {\n      free_var %y: float32\n      let %x1: float32 = add(%y, %y) /* ty=float32 */;\n      if (True /* ty=bool */) {\n        %x1\n      } else {\n        add(3f /* ty=float32 */, %x1) /* ty=float32 */\n      }\n    } else {\n      if (False /* ty=bool */) {\n        2f /* ty=float32 */\n      } else {\n        1f /* ty=float32 */\n      }\n    }\n    '
    expected_output = run_opt_pass(expected(), transform.InferType())
    assert tvm.ir.structural_equal(bblock, expected_output, map_free_vars=True)
    check_basic_block_normal_form(bblock)


def expected():
    x = relay.var('x', shape=(), dtype='bool')
    y = relay.var('y', shape=(), dtype='float32')
    cond_t = relay.const(True)
    cond_f = relay.const(False)
    one = relay.const(1, dtype='float32')
    two = relay.const(2, dtype='float32')
    three = relay.const(3, dtype='float32')
    y2 = relay.var('y2')
    true_branch = relay.If(cond_t, y2, relay.add(three, y2))
    true_branch = relay.Let(y2, relay.add(y, y), true_branch)
    false_branch = relay.If(cond_f, two, one)
    body = relay.If(x, true_branch, false_branch)
    return body


def test_recursion():
    '\n    Program:\n       let f(n: i32) -> i32 = {\n          m = (n * 2)\n          if (n == 0) {\n              return m;\n          } else {\n              return m + f(n - 1);\n          }\n       }\n       f(5);\n    '
    mod = tvm.IRModule()
    i64 = relay.TensorType((), 'int64')
    f = relay.GlobalVar('f')
    n = relay.Var('n', i64)
    m = (n * relay.const(2, 'int64'))
    cond = relay.equal(n, relay.const(0, 'int64'))
    false_branch = (m + f((n - relay.const(1, 'int64'))))
    funcbody = relay.If(cond, m, false_branch)
    value = relay.Function([n], funcbody, i64, [])
    mod[f] = value
    check_eval(f(relay.const(5, 'int64')), 30.0, mod=mod)
    old_f = mod[f]
    mod = transform.ToBasicBlockNormalForm()(mod)
    f = mod[f]
    check_eval(f(relay.const(5, 'int64')), 30.0, mod=mod)
    check_basic_block_normal_form(f)


def test_ref():
    i = relay.Var('i')
    iv = relay.Var('iv')
    u = relay.Var('u')
    uv = relay.Var('uv')
    body = relay.add(iv, uv)
    body = relay.Let(uv, relay.RefRead(i), body)
    body = relay.Let(u, relay.RefWrite(i, relay.const(2)), body)
    body = relay.Let(iv, relay.RefRead(i), body)
    body = relay.Let(i, relay.RefCreate(relay.const(1)), body)
    check_eval(body, 3)
    opt_body = run_opt_pass(body, transform.ToBasicBlockNormalForm())
    check_eval(opt_body, 3)
    check_basic_block_normal_form(opt_body)


def test_nat_add():
    mod = tvm.IRModule()
    p = Prelude(mod)
    nat = p.nat
    add = p.add
    s = p.s
    z = p.z
    ctx = tvm.context('llvm', 0)
    intrp = create_executor(mod=mod, ctx=ctx, target='llvm')
    assert (mod[add].checked_type == relay.FuncType([nat(), nat()], nat()))
    assert (count(p, intrp.evaluate(add(s(z()), s(z())))) == 2)
    expr = add(s(z()), s(z()))
    f = relay.GlobalVar('f')
    mod[f] = relay.Function([], expr)
    mod = transform.ToBasicBlockNormalForm()(mod)
    opt_expr = mod['f']
    assert (count(p, intrp.evaluate(opt_expr.body)) == 2)
    assert (not (Feature.fLet in detect_feature(mod[add])))
    check_basic_block_normal_form(opt_expr)


def test_let():

    def test_let1():
        x = relay.Var('x')
        c = relay.const(4.0, 'float32')
        body = relay.Let(x, c, x)
        body = run_opt_pass(body, transform.InferType())
        '\n        let %x: float32 = 4f /* ty=float32 */;\n        %x\n        '
        opt_body = run_opt_pass(body, transform.ToBasicBlockNormalForm())
        assert tvm.ir.structural_equal(body, opt_body)
        check_basic_block_normal_form(opt_body)

    def test_let1_1():
        x = relay.Var('y')
        d = relay.const(4.0, 'float32')
        body = relay.Let(x, d, relay.add(x, x))
        body = run_opt_pass(body, transform.InferType())
        opt_body = run_opt_pass(body, transform.ToBasicBlockNormalForm())
        assert tvm.ir.structural_equal(body, opt_body)
        check_basic_block_normal_form(opt_body)

    def test_let2():
        x = relay.Var('x')
        y = relay.Var('y')
        d = relay.const(4.0, 'float32')
        body = relay.Let(y, x, x)
        body = relay.Let(x, d, body)
        body = run_opt_pass(body, transform.InferType())
        check_eval(body, 4)

        def expected():
            x = relay.Var('x')
            y = relay.Var('y')
            d = relay.const(4.0, 'float32')
            body = relay.Let(y, x, y)
            body = relay.Let(x, d, body)
            return body
        opt_body = run_opt_pass(body, transform.ToBasicBlockNormalForm())
        expected_body = run_opt_pass(expected(), transform.InferType())
        assert tvm.ir.structural_equal(opt_body, expected_body)
        check_basic_block_normal_form(opt_body)

    def test_let3():
        x = relay.Var('x')
        y = relay.Var('y')
        z = relay.Var('z')
        c = relay.const(3.0, 'float32')
        d = relay.const(4.0, 'float32')
        body = relay.Let(z, (x + y), (x + z))
        body = relay.Let(x, d, body)
        body = relay.Let(y, c, body)
        body = run_opt_pass(body, transform.InferType())
        opt_body = run_opt_pass(body, transform.ToBasicBlockNormalForm())
        assert tvm.ir.structural_equal(body, opt_body)
        check_basic_block_normal_form(opt_body)
    test_let1()
    test_let1_1()
    test_let2()
    test_let3()


def test_function():
    t = relay.TensorType((), 'float32')
    x = relay.Var('x', t)
    f = relay.Function([x], (x + x))
    d = relay.const(4.0, 'float32')
    bblock = run_opt_pass(f, transform.ToBasicBlockNormalForm())
    assert isinstance(bblock, relay.Function)
    check_eval(f(d), 8)
    check_eval(bblock(d), 8)
    check_basic_block_normal_form(bblock)


def test_gradient_if():
    x = relay.var('a', shape=(1, 16))
    y = relay.var('y', shape=(1, 16))
    cond = relay.var('cond', shape=(), dtype='uint1')
    net = relay.If(cond, x, x)
    net = relay.add(x, net)
    net = relay.Function([cond, x, y], net)
    mod = tvm.IRModule.from_expr(net)
    mod = relay.transform.ToBasicBlockNormalForm()(mod)
    net_grad = relay.transform.gradient(mod['main'], mode='higher_order')
    mod['main'] = net_grad
    mod_grad = relay.transform.ToBasicBlockNormalForm()(mod)
    check_basic_block_normal_form(mod_grad['main'])
    check_basic_block_normal_form(mod['main'])


def test_if():

    def if_expr(x):
        '\n        free_var %x: float32\n        %0 = equal(%x, 2f);\n        if (%0) {\n          %1 = add(%x, 1f);\n          multiply(%1, 2f)\n        } else {\n          multiply(%1, 1f)\n        }\n        '
        one = relay.const(1, dtype='float32')
        two = relay.const(2, dtype='float32')
        v1 = relay.add(x, one)
        v2 = relay.equal(x, two)
        true_branch = relay.multiply(v1, two)
        false_branch = relay.multiply(v1, one)
        body = relay.If(v2, true_branch, false_branch)
        return body

    def expected_if_expr(x):
        '\n        free_var %x: float32\n        let %v1: float32 = add(%x, 1f /* ty=float32 */) /* ty=float32 */;\n        %0 = equal(%x, 2f /* ty=float32 */) /* ty=bool */;\n        if (%0) {\n          multiply(%v1, 2f /* ty=float32 */) /* ty=float32 */\n        } else {\n          multiply(%v1, 1f /* ty=float32 */) /* ty=float32 */\n        }\n        '
        one = relay.const(1, dtype='float32')
        two = relay.const(2, dtype='float32')
        v1 = relay.var('v1')
        v2 = relay.equal(x, two)
        true_branch = relay.multiply(v1, two)
        false_branch = relay.multiply(v1, one)
        body = relay.If(v2, true_branch, false_branch)
        body = relay.Let(v1, relay.add(x, one), body)
        return body
    x = relay.var('x', shape=(), dtype='float32')
    body = if_expr(x)
    expected_body = expected_if_expr(x)
    bblock = run_opt_pass(body, transform.ToBasicBlockNormalForm())
    expected_bblock = run_opt_pass(expected_body, transform.InferType())
    assert tvm.ir.structural_equal(bblock, expected_bblock, map_free_vars=True)
    check_basic_block_normal_form(bblock)
    func = relay.Function([x], body)
    expected_func = relay.Function([x], expected_body)
    bblock = run_opt_pass(func, transform.ToBasicBlockNormalForm())
    expected_bblock = run_opt_pass(expected_func, transform.InferType())
    assert tvm.ir.structural_equal(bblock, expected_bblock)
    check_basic_block_normal_form(bblock)


def if_expr(x):
    '\n        free_var %x: float32\n        %0 = equal(%x, 2f);\n        if (%0) {\n          %1 = add(%x, 1f);\n          multiply(%1, 2f)\n        } else {\n          multiply(%1, 1f)\n        }\n        '
    one = relay.const(1, dtype='float32')
    two = relay.const(2, dtype='float32')
    v1 = relay.add(x, one)
    v2 = relay.equal(x, two)
    true_branch = relay.multiply(v1, two)
    false_branch = relay.multiply(v1, one)
    body = relay.If(v2, true_branch, false_branch)
    return body


def expected_if_expr(x):
    '\n        free_var %x: float32\n        let %v1: float32 = add(%x, 1f /* ty=float32 */) /* ty=float32 */;\n        %0 = equal(%x, 2f /* ty=float32 */) /* ty=bool */;\n        if (%0) {\n          multiply(%v1, 2f /* ty=float32 */) /* ty=float32 */\n        } else {\n          multiply(%v1, 1f /* ty=float32 */) /* ty=float32 */\n        }\n        '
    one = relay.const(1, dtype='float32')
    two = relay.const(2, dtype='float32')
    v1 = relay.var('v1')
    v2 = relay.equal(x, two)
    true_branch = relay.multiply(v1, two)
    false_branch = relay.multiply(v1, one)
    body = relay.If(v2, true_branch, false_branch)
    body = relay.Let(v1, relay.add(x, one), body)
    return body
ZmncS=relay.var('''y0''',shape=(1,4),dtype='''int16''')
SdJ2V=expected_if_expr(ZmncS)
P30df=transform.ToBasicBlockNormalForm()
WJw4J=run_opt_pass(SdJ2V,P30df)
check_basic_block_normal_form(WJw4J)
