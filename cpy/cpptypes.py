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
        self._type = _type
        self.name = name

    @property
    def declaration(self):
        return str(self._type) + ' ' + str(self.name)

    def __str__(self):
        return self.declaration

    def __lt__(self, other):
        return Expression(self) < Expression(other)

    def __le__(self, other):
        return Expression(self) <= Expression(other)

    def __eq__(self, other):
        return Expression(self) == Expression(other)

    def __ne__(self, other):
        return Expression(self) != Expression(other)

    def __gt__(self, other):
        return Expression(self) > Expression(other)

    def __ge__(self, other):
        return Expression(self) >= Expression(other)


class Expression(object):
    def __init__(self, expr):
        if isinstance(expr, Variable):
            self.expression_text = expr.name

        elif isinstance(expr, Expression):
            self.expression_text = expr.expression_text

        elif isinstance(expr, str):
            self.expression_text = expr

        elif isinstance(expr, (int, long, float, complex)):
            self.expression_text = str(expr)

    def __str__(self):
        return str(self.expression_text)

    def __lt__(self, other):
        return Expression(self.name + ' < ' + str(other))

    def __le__(self, other):
        return Expression(self.expression_text + ' <= ' + other.expression_text)

    def __eq__(self, other):
        return Expression(self.expression_text + ' == ' + other.expression_text)


    def __ne__(self, other):
        return Expression(self.expression_text + ' != ' + other.expression_text)

    def __gt__(self, other):
        return Expression(self.expression_text + ' > ' + other.expression_text)

    def __ge__(self, other):
        return Expression(self.expression_text + ' >= ' + other.expression_text)


if __name__ == '__main__':
    print Ptr(Type('int'))
    print Ptr(Ptr(Type('int')))
    print Variable('alpha', Ptr(Ptr(Type('int'))))

    a = Variable('alpha', Ptr(Ptr(Type('int'))))
    print (a <= 10)

