import sympy
from abstract import CpyVar


def declare_const_entrants(indexing_vector, source_var_name):
    """Assumes an enum."""
    assert indexing_vector.shape[1] == 1

    cpy_vars = []
    for row, index_var in enumerate(indexing_vector):
        assert len(index_var.free_symbols) == 1, "Only one free symbol per vector element permissible"

        value = "{source_var_name}({row})".format(source_var_name=source_var_name, row=row)
        cpy_vars.append(
            CpyVar('double', index_var, value, qualifiers=['const'])
        )

    text = ""
    for var in cpy_vars:
        text += var.declare()
    return text


def zero_elements(sym_mat):
    """Return tuples of row, col locations of zero elements."""
    elements = []
    for row in xrange(sym_mat.shape[0]):
        for col in xrange(sym_mat.shape[1]):
            if sym_mat[row, col] == 0:
                elements.append((row, col))
    return elements


def nonzero_elements(sym_mat):
    """Return tuples of row, col locations of nonzero elements."""
    elements = []
    for row in xrange(sym_mat.shape[0]):
        for col in xrange(sym_mat.shape[1]):
            if sym_mat[row, col] != 0:
                elements.append((row, col))
    return elements


def numel(sym_mat):
    """Return number of elements in symbolic matrix."""
    return sym_mat.shape[0] * sym_mat.shape[1]


def enum_from_vec(sym_q, name, extras=[]):
    out_txt = ""
    out_txt += 'enum {name}'.format(name=name) + '{'

    txt = [str(var).upper() + ' = ' + str(n) for n, var in enumerate(sym_q)]
    ct = len(txt)
    for n, extra in enumerate(extras):
        txt.append("{} = {}".format(extra, n + ct))

    out_txt += ',//\n '.join(txt) + '};'
    return out_txt


def eigen_vector(matrix, name='m'):
    assert matrix.shape[1] == 1
    rows = matrix.shape[0]

    declaration = "EigVector<{rows}> {name}".format(rows=rows, name=name)
    code = []
    for n, row in enumerate(matrix):
        code_text = sympy.printing.ccode(row)
        declaration_text = "{name}({n}) = {code}".format(name=name, n=n, code=code_text)
        code.append(declaration_text)

    text = declaration + ';' + ';'.join(code) + ';'
    return text


def eigen_matrix(matrix, name='m', setzero=True, force_size=None):
    text = ''
    if force_size is None:
        rows = matrix.shape[0]
        cols = matrix.shape[1]
    else:
        rows, cols = force_size

    zeros = zero_elements(matrix)
    element_ct = numel(matrix)
    if zeros > (0.25 * element_ct):
        text += '\n// This matrix would benefit from sparsity support -- CPY will soon have it!\n'

    declaration = "EigMat<{rows}, {cols}> {name}".format(rows=rows, cols=cols, name=name)
    declaration += ' = EigMat<{rows}, {cols}>::Zero()'.format(rows=rows, cols=cols, name=name)
    declaration_text = eigen_matrix_assign(matrix, name, num_cols=cols)

    text += declaration + ';' + declaration_text
    return text


def eigen_matrix_assign(matrix, name, num_cols=None):
    text = ''
    rows = matrix.shape[0]

    if num_cols is None:
        cols = matrix.shape[1]
    else:
        cols = num_cols

    code = []
    for row_n in range(rows):
        row_code = ", ".join([sympy.printing.ccode(decl) for decl in matrix[row_n, :]])

        row_code += ", 0.0" * (cols - matrix.shape[1])

        declaration_text = "{name}.row({n}) << {code}".format(name=name, n=row_n, code=row_code)
        code.append(declaration_text)

    return ';'.join(code) + ';'
