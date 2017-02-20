from cpy.logging import Log


def prettify_output(text):
    """Turn gcc/make output into something a tad more readable."""
    lines = text.split('\n')

    for line in lines:
        if ': note:' in line:
            Log.note(line)

        elif ': error:' in line:
            Log.error(line)

        elif ': warning:' in line:
            Log.warn(line)

        # I know, I'm awful
        elif '%]' in line:
            Log.good(line)

        # Nothing interesting about this output line
        else:
            Log.info(line)
