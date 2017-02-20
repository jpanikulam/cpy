from cpy.base import str_helpers

class CodeBlock(object):
    def __init__(self, owner=None):
        self.text = ""
        self._owner = owner

        self._tab_depth = 0
        if owner is not None:
            self._tab_depth = owner.tab_depth + 2

    def write(self, text):
        if self.is_subscope:
            self._owner.write(text)
        else:
            self.text += text

    def line(self, text):
        new_line = line(text, self._tab_depth)
        if self.is_subscope:
            self._owner.write(new_line)
        self.text += new_line

    def write_block(self, block):
        tab = ' ' * self.tab_depth
        block_split = str(block).split('\n')
        new_block = ('\n' + tab).join(block_split)

    def subscope(self):
        return CodeBlock(owner=self)

    @property
    def tab_depth(self):
        return self._tab_depth

    @property
    def is_subscope(self):
        if self._owner is None:
            return False
        else:
            return True

    def __enter__(self):
        self.write('{\n')
        return self

    def __exit__(self, *args):
        self.write('}\n')

    def __str__(self):
        return self.text

def line(text, tab_depth=0):
    text = str(text)
    text, _ = str_helpers.get_remove(text, ';')
    text = text.strip()

    tab = ' ' * tab_depth

    return tab + text + ';\n'


if __name__ == '__main__':
    print line('asddas')

    block = CodeBlock()
    with block.subscope() as ss:
        print ss
        ss.line('hello')

    print block