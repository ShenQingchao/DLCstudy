# 0.8 dev Incorrect Exception Handling High-Level IR Transformation not fixed
import tvm.testing
import tvm.relay.testing
import pytest
import tvm.relay.transform
from tvm.tir.expr import *
from tvm.relay.dataflow_pattern import *
import tvm.topi.testing
import tvm.relay as relay


warning=pytest.raises(tvm.error.DiagnosticError)

SEMVER = '#[version = "0.0.5"]\n'

def assert_graph_equal(lhs, rhs):
    tvm.ir.assert_structural_equal(lhs, rhs, map_free_vars=True)


def graph_equal(lhs, rhs):
    return tvm.ir.structural_equal(lhs, rhs, map_free_vars=True)

def roundtrip_expr(expr):
    text = tvm.relay.Expr.astext(expr, show_meta_data=False)
    x = tvm.parser.parse_expr(text)
    assert_graph_equal(x, expr)

def roundtrip(expr):
    x = tvm.parser.fromtext(expr.astext())
    assert_graph_equal(x, expr)

def parse_text(code):
    expr = tvm.parser.parse_expr(code)
    roundtrip_expr(expr)
    return expr

def parses_as(code, expr):
    parsed = parse_text(code)
    result = graph_equal(parsed, expr)
    return result

def parse_module(code):
    mod = tvm.parser.parse((SEMVER + code))
    roundtrip(mod)
    return mod
    
with warning:
	parse_module(('''
            %s

            type List[A] {
            Cons(A, List[A]),
            Nil,
            }
            ''' % '''
type List[A] {
    Cons(A, List[A]),
    Nil,
}
'''))

