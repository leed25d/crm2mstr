def make_tableclass(klass, *args, **kwattrs):
    return type(klass, (args), dict(**kwattrs))
