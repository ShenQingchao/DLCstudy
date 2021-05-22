# 0.8 dev Incorrect Exception Handling High-Level IR Transformation not fixed
from tvm.relay import create_executor
import tvm.relay as relay
import tvm.topi.testing
import numpy as np
import tvm
from tvm.relay.dataflow_pattern import *
import tvm.testing
from tvm.tir.expr import *
from tvm.relay.testing import run_infer_type

def C(x):
    return relay.expr.const(x, 'float32')

def approx_exp(x):
    x = relay.minimum(relay.maximum(x, C((- 88.0))), C(88.0))
    x = (C(127.0) + (x * C(1.44269504)))
    xf = relay.floor(x)
    i = relay.cast(xf, 'int32')
    x = (x - xf)
    Y = (C(0.99992522) + (x * (C(0.69583354) + (x * (C(0.22606716) + (x * C(0.078024523)))))))
    exponent = relay.left_shift(i, relay.expr.const(23, 'int32'))
    exponent = relay.reinterpret(exponent, 'float32')
    return (exponent * Y)

def approximate_sigmoid(x):
    y = approx_exp(x)
    return (y / (y + C(1.0)))

def approximate_tanh(x):
    x = (x * C(2.0))
    y = approx_exp(x)
    return ((y - C(1.0)) / (y + C(1.0)))

a = relay.var('a', relay.TensorType((1000,), 'float32'))
y = approximate_sigmoid(a)
yy = run_infer_type(y)
data = np.linspace((- 5), 5, 100).astype('float32')
intrp = create_executor()
op_res = intrp.evaluate(y, {a: relay.const(data)})
