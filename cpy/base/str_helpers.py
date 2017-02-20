def between(text, left_delimeter, right_delimeter):
    start = text.index(left_delimeter) + 1
    end = text.index(right_delimeter)
    return text[start:end]

def not_between(text, left_delimeter, right_delimeter):
    start = text.index(left_delimeter)
    end = text.index(right_delimeter)
    return text[:start] + text[end + 1:]

def after(text, delimeter):
    return text[text.index(delimeter) + 1:]

def before(text, delimeter):
    return text[:text.index(delimeter)]

def comma_join(iterable):
    text = ', '.join(iterable)
    return text

def get_remove(text, target):
    if target in text:
        return text.replace(target, '').strip(), True
    else:
        return text, False

def map_strip(iterable):
    return map(lambda o: o.strip(), iterable)

def clean_split(text, delimeter):
    split = text.split(delimeter)
    clean = map_strip(split)
    return clean
