
import tvm.topi.testing
import tvm.relay.transform
import tvm.relay.testing
import tvm
import tvm.relay as relay
import pytest
import tvm.testing
from tvm.tir.expr import *
from tvm.relay.dataflow_pattern import *

warning=pytest.raises(tvm.error.DiagnosticError)

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

with warning:
	res=parse_text('''meta[random_entry][15123]''')

