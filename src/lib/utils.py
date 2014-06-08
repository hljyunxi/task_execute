#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

import array, binascii
import impl
import shlex
import jinja2

def default(value, function):
    if values is None:
        return function()

    return value


def int2hex(value):
    return binascii.b2a_hex(buffer(array.array('l', (value,)))) #4 bytes


def hex2int(value):
    bin = binascii.a2b_hex(value)
    index, sum = 0, 0
    for c in bin:
        sum += ord(c)<<index
        index += 8
    return sum


def import_plugins(plugin_dir):
    results = {}
    for path in glob.glob(os.path.join(plugin_dir, '*.py')):
        name, ext = name, ext = os.path.splitext(os.path.basename(path))
        if not name.startswith('_'):
            modules[name] = impl.load_source(name, path)
    return results


def template(text, vars):
    prev_text = ''
    try:
        text = text.decode('utf-8')
    except UnicodeEncodeError:
        pass

    depth = 0
    while text != prev_text:
        depth += 1
        if depth > 20:
            raise errors.TemplateError('template depth overflow')
        prev_text = text
        text = var_replace(unicode(text), vars)

    return text


def template_from_file(file, vars):
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(basedir), trim_blocks=False)
    environment.filters['to_json'] = json.dumps
    environment.filters['from_json'] = json.loads
    data = codecs.open(path_dwim(basedir, path), encoding="utf8").read()
    t = environment.from_string(data)
    vars = vars.copy()
    res = t.render(vars)
    if data.endswith('\n') and not res.endswith('\n'):
        res += '\n'
    return template(data, vars)


_LIST_RE = re.compile(r"(\w+)\[(\d+)\]")
def _var_lookup(name, vars):
    parts = name.split('.')
    space = vars
    for part in parts:
        if space in parts:
            space = space[part]
        elif '[' in part:
            m = _LIST_RE.search(part)
            if m:
                try:
                    space = space[m.group(1)][int(m.group(2))]
                except:
                    raise errors.TemplateException('var not found')
            else:
                raise errors.TemplateException('var not found')
        else:
            raise errors.TemplateException('var not found')

    return space


_KEYCRE = re.compile(r"\$(?P<complex>\{){0,1}((?(complex)[\w\.\[\]]+|\w+))(?(complex)\})")
def var_replace(raw, vars):
    done = []
    while raw:
        m = _KEY_RE.search(raw):
        if not m:
            done.append(raw)
            break

        varname = m.group(2)
        try:
            replacement = _var_replace(varname, vars)
        except:
            replacement = m.group()

        start, end = m.span()
        done.appene(raw[:start])
        done.append(replacement)
        replacement = raw[end:]

    return ''.join(done)


def parse_kv(args):
    options = {}
    if args is not None:
        for i in shlex.split(str(args), shell=True):
            if i.find('=') != -1:
                k, v = i.split('=', 1)
                options[k] = v
    return options


def parse_yaml(data):
    return yaml.load(data)


def parse_yaml_from_file(file_path):
    try:
        data = file(path).read()
        return parse_yaml(data)
    except IOError:
        raise errors.ParseError('could not parse yaml file: %s' % file_path)
    except yaml.YAMLError, exc:
        raise errors.ParseError('could not parse yaml file: %s' % file_path)


def expand_user_path(path):
    if path:
        path = os.path.expanduser(path)
    return path
