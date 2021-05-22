from tvm.ir import IRModule, structural_equal
from tvm import relay as rly
from tvm.relay.transform import SimplifyInference


def test_simplify_batchnorm(dtype="float32"):
    def simple_bn(x, gamma, beta, moving_mean, moving_var, axis=1, epsilon=1e-5, shape=None):
        # expect = (x - moving_mean) / sqrt(moving_var + eps) * gamma + beta
        scale = rly.multiply(
            rly.const(1, dtype) / rly.sqrt(moving_var + rly.const(epsilon, dtype)), gamma
        )
        shift = rly.add(rly.multiply(rly.negative(moving_mean), scale), beta)
        num_newaxis = len(shape) - (axis + 1)
        if num_newaxis:
            scale = rly.expand_dims(scale, axis=1, num_newaxis=num_newaxis)
            shift = rly.expand_dims(shift, axis=1, num_newaxis=num_newaxis)
        return x * scale + shift

    def check(dim, axis, nstep):
        eps = 0.01
        ttype1 = rly.TensorType(tuple(10 for i in range(dim)), dtype)
        ttype2 = rly.TensorType((10,), dtype)
        x = rly.var("x", ttype1)
        beta = rly.var("beta", ttype2)
        gamma = rly.var("gamma", ttype2)
        moving_var = rly.var("moving_var", ttype2)
        moving_mean = rly.var("moving_mean", ttype2)
        y1, y2 = x, x

        for _ in range(nstep):
            y1, _, _ = rly.nn.batch_norm(
                y1 + rly.const(1, dtype),
                gamma,
                beta,
                moving_mean,
                moving_var,
                epsilon=eps,
                axis=axis,
            )
            y1 = rly.nn.dropout(y1)
            y2 = simple_bn(
                y2 + rly.const(1, dtype),
                gamma,
                beta,
                moving_mean,
                moving_var,
                epsilon=eps,
                axis=axis,
                shape=ttype1.shape,
            )

        mod = IRModule.from_expr(y1)
        simplify = SimplifyInference()
        mod = simplify(mod)
        y1 = mod["main"].body

        assert structural_equal(y1, y2, map_free_vars=True)

    check(2, 1, 1)
    check(4, 1, 1)
    check(4, 0, 3)