class Type(object):
    def __init__(self, name, template_arguments=[]):
        self._name = name
        self.template_arguments = template_arguments

    @property
    def name(self):
        if len(self.template_arguments):
            return self._name + '<{}>'.format(', '.join(self.template_arguments))
        else:
            return self._name

    def __str__(self):
        return self.name
