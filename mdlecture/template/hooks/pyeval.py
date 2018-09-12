import traceback
import io
import contextlib

context = {}


def do_eval(s):
    try:
        return repr(eval(s, context))
    except SyntaxError:
        try:
            exec(s, context)
        except SyntaxError:
            traceback.print_exc()


def process(src):
    with open(src) as f:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            for line in f:
                print(line, end='')
                if line.startswith('>>>'):
                    val = do_eval(line[4:])
                    if val:
                        print(val)
        return out.getvalue()
