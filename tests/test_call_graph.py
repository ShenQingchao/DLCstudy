import pytest
import tvm
from tvm import relay

def test_callgraph_construct():
    mod = tvm.IRModule({})
    x = relay.var("x", shape=(2, 3))
    y = relay.var("y", shape=(2, 3))
    mod["g1"] = relay.Function([x, y], x + y)
    call_graph = relay.analysis.CallGraph(mod)
    assert "g1" in str(call_graph)
    assert tvm.ir.structural_equal(mod, call_graph.module)


def test_print_element():
    mod = tvm.IRModule({})
    x0 = relay.var("x0", shape=(2, 3))
    y0 = relay.var("y0", shape=(2, 3))
    mod["g0"] = relay.Function([x0, y0], x0 + y0)
    x1 = relay.var("x1", shape=(2, 3))
    y1 = relay.var("y1", shape=(2, 3))
    mod["g1"] = relay.Function([x1, y1], x1 - y1)
    call_graph = relay.analysis.CallGraph(mod)

    assert "#refs = 0" in str(call_graph.print_var("g0"))
    assert "#refs = 0" in str(call_graph.print_var("g1"))


def test_global_call_count():
    mod = tvm.IRModule({})
    x0 = relay.var("x0", shape=(2, 3))
    y0 = relay.var("y0", shape=(2, 3))
    g0 = relay.GlobalVar("g0")
    mod[g0] = relay.Function([x0, y0], x0 + y0)
    x1 = relay.var("x1", shape=(2, 3))
    y1 = relay.var("y1", shape=(2, 3))
    g1 = relay.GlobalVar("g1")
    mod[g1] = relay.Function([x1, y1], g0(x1, y1))
    call_graph = relay.analysis.CallGraph(mod)

    p0 = relay.var("p0", shape=(2, 3))
    p1 = relay.var("p1", shape=(2, 3))
    func = relay.Function([p0, p1], g0(p0, p1) * g1(p0, p1))
    mod["main"] = func
    call_graph = relay.analysis.CallGraph(mod)

    assert call_graph.global_call_count(g0) == 0
    assert call_graph.global_call_count(g1) == 1
    assert call_graph.global_call_count("main") == 2


def test_ref_count():
    mod = tvm.IRModule({})
    x0 = relay.var("x0", shape=(2, 3))
    y0 = relay.var("y0", shape=(2, 3))
    g0 = relay.GlobalVar("g0")
    mod[g0] = relay.Function([x0, y0], x0 + y0)
    x1 = relay.var("x1", shape=(2, 3))
    y1 = relay.var("y1", shape=(2, 3))
    g1 = relay.GlobalVar("g1")
    mod[g1] = relay.Function([x1, y1], x1 - y1)
    call_graph = relay.analysis.CallGraph(mod)

    p0 = relay.var("p0", shape=(2, 3))
    p1 = relay.var("p1", shape=(2, 3))
    func = relay.Function([p0, p1], g0(p0, p1) * g1(p0, p1))
    mod["main"] = func
    call_graph = relay.analysis.CallGraph(mod)

    assert call_graph.ref_count(g0) == 1
    assert call_graph.ref_count(g1) == 1
    assert call_graph.ref_count("main") == 0


def test_nested_ref():
    mod = tvm.IRModule({})
    x0 = relay.var("x0", shape=(2, 3))
    y0 = relay.var("y0", shape=(2, 3))
    g0 = relay.GlobalVar("g0")
    mod[g0] = relay.Function([x0, y0], x0 + y0)
    x1 = relay.var("x1", shape=(2, 3))
    y1 = relay.var("y1", shape=(2, 3))
    g1 = relay.GlobalVar("g1")
    mod[g1] = relay.Function([x1, y1], g0(x1, y1))
    call_graph = relay.analysis.CallGraph(mod)

    p0 = relay.var("p0", shape=(2, 3))
    p1 = relay.var("p1", shape=(2, 3))
    func = relay.Function([p0, p1], g0(p0, p1) * g1(p0, p1))
    mod["main"] = func
    call_graph = relay.analysis.CallGraph(mod)

    assert call_graph.ref_count(g0) == 2
    assert call_graph.ref_count(g1) == 1
    assert call_graph.ref_count("main") == 0

def test_recursive_func():
    mod = tvm.IRModule({})

    x = relay.var("x", shape=[], dtype="int32")
    fn0 = relay.Function([x], x)
    gx = relay.GlobalVar("gx")
    mod[gx] = fn0

    sum_up = relay.GlobalVar("sum_up")
    i = relay.var("i", shape=[], dtype="int32")
    sb = relay.ScopeBuilder()

    func = relay.Function([i], sb.get(), ret_type=relay.TensorType([], "int32"))
    func = func.with_attr("Compiler", "a")
    mod[sum_up] = func
    iarg = relay.var("i", shape=[], dtype="int32")
    mod["main"] = relay.Function([iarg], sum_up(iarg))
    call_graph = relay.analysis.CallGraph(mod)
