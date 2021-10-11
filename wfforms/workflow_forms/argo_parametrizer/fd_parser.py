# Field format parser

def cast_with_lim(t, mi, ma, cast):
    c = cast(t)
    if mi is not None:
        if c < mi:
            raise ValueError('Field value less than min')
    if ma is not None:
        if c > ma:
            raise ValueError('Field value greater than max')
    return c

def cast_str_with_maxlength(t, ma):
    if len(t) > ma:
        raise ValueError('String field too long')
    return t
def parse_field_definition(text):
    '''parse_filed_format: Parse field definition
       text: A multi-line str-like object of the following format:
       field_name\tfield_descr\tfield_type\tdefault_value\tlim_min\tlim_max\tstored_name
       where:
           * field_name: The name of the field being defined
           * field_descr: The description of the field being defined
           * field_type: The type of the field being defined. Can be int, float, str
                         or file.ext, where ext the desired file extension.
           * default_value: The default value of the field. Use none for no default value.
           * lim_min: For numerical fields, the minimum allowed value. Use none for none.
                      Not applicable to string of file fields.
           * lim_max: For numerical fields, the maximum allowed value. 
                      For string fields, the maximum allowed length.
                      Not applicable to file fields.
                      Use none for none.
           * stored_name: The variable to store the field's value in. If the field
                          takes a file as input, the file name in which to store
                          the file.
        Returns a dict-like object, with the following keys:
            name -> field_name
            descr -> field_descr
            type -> field_type
            cast_function: A function which can be used to cast/verify the input value
            default_value -> default_value
            lim_min -> lim_min
            lim_max -> lim_max
            stored_name -> stored_name'''
    ts = text.strip().split(',')
    rv = {}
    rv['name'] = ts[0]
    rv['descr'] = ts[1]
    rv['type'] = ts[2]
    if rv['type'] == 'str':
        if ts[4] != 'none':
            maxlen = int(ts[4])
            rv['cast_function'] = lambda x: cast_str_with_maxlength(x,maxlen)
            rv['lim_max'] = maxlen
        else:
            rv['cast_function'] = str
            rv['lim_max'] = None
        rv['stored_name'] = ts[5]
    elif rv['type'] == 'int' or rv['type'] == 'float':
        if rv['type'] == 'int':
            cf = int
        else:
            cf = float
        if ts[4] == 'none':
            mi = None
        else:
            mi = cf(ts[4])
        if ts[5] == 'none':
            ma = None
        else:
            ma = cf(ts[5])
        rv['cast_function'] = lambda x: cast_with_lim(x, mi, ma, cf)
        rv['lim_min'] = mi
        rv['lim_max'] = ma
        rv['stored_name'] = ts[6]
    elif 'file' in rv['type']:
        rv['stored_name'] = ts[3]
        rv['cast_function'] = str
    if 'file' not in rv['type']:
        rv['default_value'] = rv['cast_function'](ts[3])
    return rv

def parse_field_tsv(s):
    rv = []
    lc = 0
    for l in s.splitlines():
        lc += 1
        try:
            rv.append(parse_field_definition(l))
        except ValueError as ve:
            raise ValueError(f'Syntax error in line {lc}, {ve}')
    return rv

