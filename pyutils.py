def trim(l, s=None, e=None):
    if s is not None and l.startswith(s)and len(s) > 0:
        l = l[len(s):]
    if e is not None and l.endswith(e) and len(e) > 0:
        l = l[:-len(e)]
    return l

def read(path):
    with open(path, 'r') as f:
        return f.read()

def write(what, where, mode='w'):
    with open(where, mode=mode) as f:
        return f.write(what)

def load_json(where_from):
    import os
    import json
    if os.path.exists(where_from):
        with open(where_from, 'r') as f:
            return json.load(f)
    else:
        return json.loads(where_from)

def dump_json(what, where, mode='w'):
    import json
    with open(where, mode=mode) as f:
        return json.dump(what, f)
