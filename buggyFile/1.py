# v0.7 Type Problem High-Level IR Transformation fixed
from tvm import relay
import tvm
cObhB=relay.var('x')
B28Qg=relay.var('xjym')
Xzba1=relay.add(cObhB,B28Qg)
pDL7X=relay.Function([cObhB,B28Qg],Xzba1)
xqvpP=tvm.IRModule.from_expr(pDL7X)
