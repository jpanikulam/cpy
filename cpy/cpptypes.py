from core import Code
from utils import Utils


class Ptr(object):
    def __init__(self, _type):
        '''This should take a new Type as an argument'''
        assert isinstance(_type, (Type, Ptr)), "type must be a cppType"
        self._type = _type

    def __str__(self):
        return str(self._type) + '*'


class Type(object):
    def __init__(self, type_name):
        assert isinstance(type_name, str), "type_name must be a str, like 'int' or 'bool'"
        self.type_name = type_name

    def __str__(self):
        return self.type_name


class Variable(object):
    def __init__(self, name, _type):
        if '=' in name:
            self.name, self.initalization = Utils.clean_split(name, '=')

        else:
            self.initalization = None
            self.name = name

        self._type = _type

    @property
    def declaration(self):
        return str(self._type) + ' ' + str(self.name)

    def declare(self):
        Code.add_line(self.declaration)

    def __str__(self):
        return self.declaration

    def __lt__(self, other):
        return Expression(self) < other

    def __le__(self, other):
        return Expression(self) <= other

    def __eq__(self, other):
        return Expression(self) == other

    def __ne__(self, other):
        return Expression(self) != other

    def __gt__(self, other):
        return Expression(self) > other

    def __ge__(self, other):
        return Expression(self) >= other

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __floordiv__(self, other):
        pass

    def __mod__(self, other):
        pass

    def __divmod__(self, other):
        pass

#    def __pow__(self, other[, modulo]):
#        pass

    def __lshift__(self, other):
        pass

    def __rshift__(self, other):
        pass

    def __and__(self, other):
        pass

    def __xor__(self, other):
        pass

    def __or__(self, other):
        pass

    def __radd__(self, other):
        pass

    def __rsub__(self, other):
        pass

    def __rmul__(self, other):
        pass

    def __rdiv__(self, other):
        pass

    def __rtruediv__(self, other):
        pass

    def __rfloordiv__(self, other):
        pass

    def __rmod__(self, other):
        pass

    def __rdivmod__(self, other):
        pass

    def __rpow__(self, other):
        pass

    def __rlshift__(self, other):
        pass

    def __rrshift__(self, other):
        pass

    def __rand__(self, other):
        pass

    def __rxor__(self, other):
        pass

    def __ror__(self, other):
        pass


class Expression(object):
    def __init__(self, expr):
        self.parent = expr
        if isinstance(expr, Variable):
            self.expression_text = expr.name

        elif isinstance(expr, Expression):
            self.expression_text = '{}'.format(expr.expression_text)

        elif isinstance(expr, str):
            self.expression_text = expr

        elif isinstance(expr, (int, long, float, complex)):
            self.expression_text = str(expr)

    def nexpr(self, other, char):
        other_exp = Expression(other)
        if isinstance(self.parent, Expression):
            return Expression(Expression('({}) {} {}'.format(self.expression_text, char, other_exp.expression_text)))
        else:
            return Expression(Expression('{} {} {}'.format(self.expression_text, char, other_exp.expression_text)))

    def __str__(self):
        return str(self.expression_text)

    def __lt__(self, other):
        new_expr = self.nexpr(other, '<')
        return new_expr

    def __le__(self, other):
        new_expr = self.nexpr(other, '<=')
        return new_expr

    def __eq__(self, other):
        new_expr = self.nexpr(other, '==')
        return new_expr

    def __ne__(self, other):
        new_expr = self.nexpr(other, '!=')
        return new_expr

    def __gt__(self, other):
        new_expr = self.nexpr(other, '>')
        return new_expr

    def __ge__(self, other):
        new_expr = self.nexpr(other, '>=')
        return new_expr

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __floordiv__(self, other):
        pass

    def __mod__(self, other):
        pass

    def __divmod__(self, other):
        pass

#    def __pow__(self, other[, modulo]):
#        pass

    def __lshift__(self, other):
        pass

    def __rshift__(self, other):
        pass

    def __and__(self, other):
        pass

    def __xor__(self, other):
        pass

    def __or__(self, other):
        pass

    def __radd__(self, other):
        pass

    def __rsub__(self, other):
        pass

    def __rmul__(self, other):
        pass

    def __rdiv__(self, other):
        pass

    def __rtruediv__(self, other):
        pass

    def __rfloordiv__(self, other):
        pass

    def __rmod__(self, other):
        pass

    def __rdivmod__(self, other):
        pass

    def __rpow__(self, other):
        pass

    def __rlshift__(self, other):
        pass

    def __rrshift__(self, other):
        pass

    def __rand__(self, other):
        pass

    def __rxor__(self, other):
        pass

    def __ror__(self, other):
        pass


if __name__ == '__main__':
    print Ptr(Type('int'))
    print Ptr(Ptr(Type('int')))
    print Variable('alpha', Ptr(Ptr(Type('int'))))

    a = Variable('alpha', Ptr(Ptr(Type('int'))))
    print (a <= 10)

