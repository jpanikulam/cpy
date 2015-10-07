class Code(object):
    code = ""
    abstract_code = {
        'definitions': {},
        'files': {}  # structure?
    }

    indentation_state = 0
    indentor = '  '
    scope = 0

    @classmethod
    def set_indentor(self, char='  '):
        '''char should be something like
            "\t",
            "  ",
            or
            "    "
        '''
        self.indentor = char

    @classmethod
    def start_scope(self):
        '''TODO: Make Configurable'''
        self.scope += 1
        assert self.scope >= 0, "We have a mismatched curly brace, CPY thinks we're at a negative scope level"
        self.code += ' {\n'
        self.up_indentation()

    @classmethod
    def end_scope(self):
        '''TODO: Make Configurable'''
        self.scope -= 1
        assert self.scope >= 0, "We have a mismatched curly brace, CPY thinks we're at a negative scope level"
        self.down_indentation()
        self.add('}\n')

    @classmethod
    def up_indentation(self, amt=1):
        assert isinstance(amt, int), "Indentation amount must be an integer"
        self.indentation_state += amt

    @classmethod
    def down_indentation(self, amt=1):
        assert isinstance(amt, int), "Indentation amount must be an integer"
        self.indentation_state -= amt

    @classmethod
    def add(self, line):
        indentation = self.indentation_state * self.indentor
        self.code += indentation + str(line)

    @classmethod
    def add_line(self, line):
        indentation = self.indentation_state * self.indentor
        self.code += indentation + str(line) + ';\n'