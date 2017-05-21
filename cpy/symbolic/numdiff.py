import numpy as np
from scipy.misc import derivative


def _create_partial_func(func, x0, dim_num):
    """Return a partial function that only varies one input dimension of f.

    Arguments
    ---------
    func : callable
        A function that can be evaluated on a numpy asarray

    x0 : np.ndarray of floats
        The value that the function should be "frozen" at

    dim_num : The index of the dimension along which the function should be evaluated

    Returns
    -------
    float
        `func` evaluated at x0_prime; `x0_prime = x0[dim_num]` = val
        This is equivalent to say "freezing" the function around x0,
        and then allowing the function to vary along only one dimension

    """

    def partial_func(val):
        """A function that evaluates `func` along only one input dimension.

        Arguments
        ---------
        val : float

        Returns
        -------
        float
            `func` evaluated at x0_prime; `x0_prime = x0[dim_num]` = val
            This is equivalent to say "freezing" the function around x0,
            and then allowing the function to vary along only one dimension
        """

        xi = np.copy(x0)
        xi[dim_num] = val
        return func(xi)

    return partial_func


def jacobian(func, x0, dx=1e-6):
    """Compute a numerical jacobian.

    Arguments
    ---------
    func : callable
        A function that can be evaluated on a numpy asarray

    x0 : np.ndarray of floats
        The value that the function should be "frozen" at

    dx : float
        The differentiation step size

    Returns
    -------
    np.ndarray
        A matrix of floats, which will have:
            - The same number of columns as the length of the input vector
            - The same number of rows as the length of `func(x0)`

        Formatted as in [1]:
            `jacobian[row, col] = df_row / dx_col`

        The nth row of the jacobian is the gradient of the nth output element
        w.r.t the input vector

    Examples
    --------
    ## Vector-Vector functions
    >>> def func(x):
            return np.array([x[0] * 2, 3.0 * x[0] + x[1] ** 2])
    >>>
    >>> x0 = np.array([1.0, 2.0])
    >>> jacobian(func, x0)
      array([
          [2.0, 0.0],
          [3.0, 4.0]
      ])

    ## Scalar-Vector functions
    >>> def func(x):
    >>>     return np.array([x, 2 * x])

    >>> x0 = np.array([0.0])
    >>> jacobian(func, x0)
      array([
          [1.0],
          [2.0]
      ])

    Notes
    -----
    [1] https://en.wikipedia.org/wiki/Jacobian_matrix_and_determinant
    """
    out_shape = np.asarray(func(x0)).shape[0]
    in_shape = x0.shape[0]
    jacobian = np.zeros((out_shape, in_shape))
    for dim_num in range(in_shape):
        f_n = _create_partial_func(func, x0, dim_num)
        partial = derivative(f_n, x0[dim_num], dx=dx)
        if jacobian.shape[1] == 1:
            jacobian[:, dim_num] = partial[:, 0]
        else:
            jacobian[:, dim_num] = partial

    return jacobian
