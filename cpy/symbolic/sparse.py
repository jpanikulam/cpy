import sympy
import numpy as np
import operator


class SparseMatrix(object):
    """COO.

    TODO
    ----
    Do arithmetic in CSR

    Purpose
    -------
    This is a sparse matrix wrapper, targeted for use with Sympy.
    This is for code generation, so we don't really care about runtime efficiency.

    Notes
    -----
    Man, COO sucks.
    """
    def __init__(self, shape, entries={}):
        """Do nothing."""
        self._rows, self._cols = shape
        self._entries = entries
        self._col_cache = self._cache_columns(entries)
        self._row_cache = self._cache_rows(entries)

    @property
    def entries(self):
        return self._entries

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    @property
    def col_cache(self):
        return self._col_cache

    @property
    def row_cache(self):
        return self._row_cache

    def shift_down(self, n):
        new_entries = shift_down(self.entries, n)
        return new_entries

    def shift_right(self, n):
        new_entries = shift_right(self.entries, n)
        return new_entries

    def _cache_columns(self, entries):
        """This is a hacky CSR wrap."""
        cache = {}
        for coo, val in entries.items():
            cache.setdefault(coo[1], set())
            cache[coo[1]].add(coo[0])
        return cache

    def _cache_rows(self, entries):
        """This is a hacky CSR wrap."""
        cache = {}
        for coo, val in entries.items():
            cache.setdefault(coo[0], set())
            cache[coo[0]].add(coo[1])
        return cache

    def add_entry(self, ij, val):
        i, j = ij

        assert 0 <= i < self.rows
        assert 0 <= j < self.cols

        self._entries[ij] = val
        self._col_cache.setdefault(j, set())
        self._col_cache[j].add(i)
        self._row_cache.setdefault(i, set())
        self._row_cache[i].add(j)

    def dot(self, other):
        """Dot product (gemm).

        The (ij)th element of a matrix multiply is
        the dot product of the A(i, :) and B(:, j).

        In other words, the ith row of A, and the jth column of B
        """
        assert self.cols == other.rows, "Size mismatch for matrix multiply"

        new_mat = SparseMatrix((self.rows, other.cols))
        for row_num, index_set in self.row_cache.items():

            for col_num in range(other.cols):
                if col_num not in other.col_cache.keys():
                    continue

                dot_product = 0
                common = index_set.intersection(other.col_cache[col_num])
                for el in common:
                    dot_product += self.entries[(row_num, el)] * other.entries[(el, col_num)]

                if len(common):
                    new_mat.add_entry((row_num, col_num), dot_product)

        return new_mat

    def pairwise(self, other, function):
        """Apply a pairwise operation on the elements in common between the two functions"""
        assert other.cols == self.cols, "Size mismatch for pairwise operation"
        assert other.rows == self.rows, "Size mismatch for pairwise operation"
        new_entries = {}
        other_keys = set(other.entries.keys())
        for entry, val in self.entries.items():
            if entry in other_keys:
                new_entries[entry] = function(val, other.entries[entry])
                other_keys.discard(entry)
            else:
                new_entries[entry] = val

        for other_key in other_keys:
            new_entries[other_key] = other.entries[other_key]

        return SparseMatrix((self.rows, self.cols), new_entries)

    def densify(self):
        """For visualization -- not for math."""
        mat = sympy.zeros(self._rows, self._cols)
        for coo, val in self._entries.items():
            mat[coo] = val
        return mat

    def col(self, j):
        """Visualization -- Not for math."""
        return dict_get_all(self._entries, self._col_cache.get(j, set()))

    def row(self, i):
        """Visualization -- Not for math."""
        return dict_get_all(self._entries, self._row_cache.get(i, set()))

    def pprint(self):
        sympy.pretty_print(self.densify())

    def spy(self):
        from matplotlib import pyplot as plt
        image = np.zeros((self.rows, self.cols))

        keys = self.entries.keys()
        for key in keys:
            val = self.entries[key]
            try:
                v = float(val)
                image[key] = v
            except(TypeError):
                image[key] = 1

        plt.imshow(image, origin='upper')

    def __str__(self):
        return str(self.densify())

    def __add__(self, other):
        return self.pairwise(other, operator.add)

    def __sub__(self, other):
        return self.pairwise(other, operator.sub)

    def __mul__(self, other):
        return self.pairwise(other, operator.mul)

    def __div__(self, other):
        return self.pairwise(other, operator.div)

    def __setitem__(self, key, val):
        self.add_entry(key, val)


def shift_down(entries, n):
    new_entries = {}
    for coo, val in entries.items():
        coo_new = (coo[0] + n, coo[1])
        new_entries[coo_new] = val
    return new_entries


def shift_right(entries, n):
    new_entries = {}
    for coo, val in entries.items():
        coo_new = (coo[0], coo[1] + n)
        new_entries[coo_new] = val
    return new_entries


def vstack(*mats):
    new_row_ct = 0
    cols = mats[0].cols
    entries = {}
    for mat in mats:
        assert mat.cols == cols
        shifted_entries = mat.shift_down(new_row_ct)
        entries.update(shifted_entries)
        new_row_ct += mat.rows

    new_mat = SparseMatrix((new_row_ct, cols), entries)
    return new_mat


def hstack(*mats):
    new_col_ct = 0
    rows = mats[0].rows
    entries = {}
    for mat in mats:
        assert mat.rows == rows
        shifted_entries = mat.shift_right(new_col_ct)
        entries.update(shifted_entries)
        new_col_ct += mat.cols

    new_mat = SparseMatrix((rows, new_col_ct), entries)
    return new_mat


def diagstack(*mats):
    """Whoa! That's something new!."""
    new_col_ct = 0
    new_row_ct = 0

    entries = {}
    for mat in mats:
        shifted_entries = mat.shift_right(new_col_ct)
        shifted_entries = shift_down(shifted_entries, new_row_ct)

        entries.update(shifted_entries)
        new_col_ct += mat.cols
        new_row_ct += mat.rows

    new_mat = SparseMatrix((new_row_ct, new_col_ct), entries)
    return new_mat


def dict_get_all(_dict, keys):
    out = {}
    for key in keys:
        out[key] = _dict[key]
    return out


def identity(n):
    entries = {}
    for k in range(n):
        entries[(k, k)] = 1
    return SparseMatrix((n, n), entries)


def random(shape, density=0.1):
    rows, cols = shape
    nnz = int((rows * cols) * density)
    entries = {}
    for k in range(nnz):
        row = np.random.randint(0, rows)
        col = np.random.randint(0, cols)
        val = np.random.random()
        entries[(row, col)] = val

    return SparseMatrix((rows, cols), entries)


def zeros(shape):
    """No entries --> all zeros."""
    m, n = shape
    return SparseMatrix((m, n))


if __name__ == '__main__':
    from matplotlib import pyplot as plt
    spm = zeros((5, 5))
    spm.add_entry((0, 1), 1)
    spm.add_entry((1, 1), 2)
    spm.add_entry((3, 3), sympy.Symbol('a'))
    spm.add_entry((3, 4), sympy.Symbol('c'))
    spm.add_entry((2, 1), 3)

    ent2 = identity(5)
    ent2.add_entry((4, 4), 0)
    ent2.pprint()

    ent3 = spm.dot(ent2)
    ent4 = spm.dot(spm)

    sp5 = diagstack(spm, ent2, ent3, ent4)
    sp5.spy()
    plt.show()
