import tvm
from tvm import te
from tvm import relay
from tvm.relay import transform


def test_dup_type():
    a = relay.TypeVar("a")
    av = relay.Var("av", a)
    make_id = relay.Function([av], relay.Tuple([av, av]), None, [a])
    t = relay.scalar_type("float32")
    b = relay.Var("b", t)
    mod = tvm.IRModule.from_expr(make_id(b))
    mod = transform.InferType()(mod)
    inferred = mod["main"].body
    assert inferred.checked_type == relay.TupleType([t, t])


def test_id_type():
    mod = tvm.IRModule()
    id_type = relay.GlobalTypeVar("id")
    a = relay.TypeVar("a")
    mod[id_type] = relay.TypeData(id_type, [a], [])

    b = relay.TypeVar("b")
    make_id = relay.Var("make_id", relay.FuncType([b], id_type(b), [b]))
    t = relay.scalar_type("float32")
    b = relay.Var("b", t)
    mod["main"] = relay.Function([make_id, b], make_id(b))
    mod = transform.InferType()(mod)
    assert mod["main"].body.checked_type == id_type(t)