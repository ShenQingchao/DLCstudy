import os

import numpy as np

import tvm
from tvm import te
from tvm import relay
import tvm.relay.transform as _transform


def test_eta_expand_global_var():
    mod = tvm.parser.fromtext(
        r"""
        #[version = "0.0.5"]
        def @aux(%x: Tensor[(), int32]) -> Tensor[(), int32] {
            %x
        }
        def @main() -> fn(Tensor[(), int32]) -> Tensor[(), int32] {
            @aux
        }
    """
    )
    seq = tvm.transform.Sequential([_transform.EtaExpand(expand_global_var=True)])
    with tvm.transform.PassContext(opt_level=3):
        mod = seq(mod)
    expected = tvm.parser.fromtext(
        r"""
        #[version = "0.0.5"]
        def @aux(%x: Tensor[(), int32]) -> Tensor[(), int32] {
            %x
        }
        def @main() -> fn(Tensor[(), int32]) -> Tensor[(), int32] {
            fn (%x: Tensor[(), int32]) -> Tensor[(), int32] {
                @aux(%x)
            }
        }
    """
    )
    tvm.ir.assert_structural_equal(mod["main"], expected["main"], map_free_vars=True)


def test_eta_expand_constructor():
    mod = tvm.parser.fromtext(
        r"""
        #[version = "0.0.5"]
        type List[A] {
            Cons(A, List[A]),
            Nil,
        }
        def @main[A]() -> fn(A, List[A]) -> List[A] {
            Cons
        }
    """
    )
    seq = tvm.transform.Sequential([_transform.EtaExpand(expand_constructor=True)])
    with tvm.transform.PassContext(opt_level=3):
        mod = seq(mod)
    expected = tvm.parser.fromtext(
        r"""
        #[version = "0.0.5"]
        type List[A] {
            Cons(A, List[A]),
            Nil,
        }
        def @main[A]() -> fn(A, List[A]) -> List[A] {
            fn [A](%x: A, %xs: List[A]) -> List[A] {
                Cons(%x, %xs)
            }
        }
    """
    )
    tvm.ir.assert_structural_equal(mod["main"], expected["main"], map_free_vars=True)