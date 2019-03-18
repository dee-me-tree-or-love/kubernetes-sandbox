import functools

from custom_logger import cus_log

# FIXME: rewrite in Haskell

def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


def log_item(item):
    ''' Examples:
        >>> log_input("abc")
        ...
        'abc'
    '''
    cus_log('Received %r' % item)
    return item


def swap_input(item):
    ''' Examples:
        >>> swap_input("cba")
        'abc'
        >>> swap_input("abc")
        'cba'
    '''
    return str(item)[::-1]


def process_input(item):
    process = compose(log_item, swap_input, log_item)
    return process(item)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
