from colorama import Fore, Style
import os

_verbosity_table = {
    'info': 5,
    'good': 5,
    'note': 5,
    'warn': 2,
    'error': 1,
}


def get_terminal_width(default=80):
    """Get the current terminal width.

    http://stackoverflow.com/questions/566746/
    Gosh, python 2.7 :*(.
    """
    twidth = os.popen('stty size', 'r').read().split()
    if len(twidth):
        rows, columns = twidth
        return int(columns)
    else:
        return 80


class Log(object):
    _verbosity = 5
    # init(autoreset=True)

    @classmethod
    def set_verbosity(cls, verbosity):
        if verbosity is True:
            cls._verbosity = 5
        elif verbosity is False:
            cls._verbosity = 1
        elif verbosity in _verbosity_table.keys():
            cls._verbosity = _verbosity_table[verbosity]
        else:
            raise(KeyError("Unknown verbosity value: {}".format(verbosity)))

    @classmethod
    def add_logger(cls, name, color):
        """Register a new logging function, with a name."""
        assert name in _verbosity_table.keys(), "{} does not have an associated verbosity level".format(name)

        def log_func(cls, *text):
            if cls._verbosity >= _verbosity_table[name]:
                print(color + ' '.join(text) + Style.RESET_ALL)

        setattr(cls, name, classmethod(log_func))

    @classmethod
    def br(cls):
        """A terrible stupid function."""
        term_width = get_terminal_width()

        if hasattr(cls, 'info'):
            cls.info('-' * term_width)
        else:
            print('-' * term_width)

# Let's call this metaprogramming
Log.add_logger("info", Fore.WHITE)
Log.add_logger("good", Fore.GREEN)
Log.add_logger("note", Fore.BLUE)
Log.add_logger("warn", Fore.YELLOW)
Log.add_logger("error", Fore.RED)
