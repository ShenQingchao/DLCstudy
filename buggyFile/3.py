# v0.7 Tensor Shape Problem High-Level IR Transformation fixed
import tvm
import tvm.relay.transform as transform
from tvm import relay

zqKSk=relay.var('y2','uint64')
hNVPr=relay.split(zqKSk,3,axis=0)
Gko2H=hNVPr.astuple()
QLiMS=relay.Function([zqKSk],Gko2H)
EeNPI=tvm.IRModule()
EeNPI['main']=QLiMS