import argparse
import os
import subprocess
import sys
import time

from pathlib import Path
from shutil import copytree, which

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

root = Path('.').resolve()
script_dir = Path(__file__).resolve().parent
template_dir = script_dir / 'template'

TEMPLATE = '''---
title: [Title]
subtitle: [Subtitle]
author: [Author]
date: [Date]
---
'''

def _find_template_dir():
    p = root
    while p != p.parent:
        lec = p / '.lecture'
        if lec.is_dir():
            return lec
        p = p.parent

def _pdf(f):
    return f.with_suffix('.pdf')

def _make_file(target):
    tdir = _find_template_dir()
    template = tdir / 'template.tex'
    os.environ['TEXINPUTS'] = f":{tdir}"
    subprocess.run([
        'pandoc',
        '-t', 'beamer',
        '-o', f'{_pdf(target)}',
        '-V', 'fontfamily=tgheros',
        '--listings',
        f'--template={template}',
        f'{target}',
    ])

def _find_file(args):
    if args.target and args.target.is_file():
        return args.target
    else:
        # Directory
        if args.target:
            res = list(args.target.glob('*.md'))
        else:
            res = list(root.glob('*.md'))
        if len(res) == 0:
            print(f"No markdown files found, you must specify a file or a directory", file=sys.stderr)
            sys.exit(1)
        return res[0]

def init(args):
    local = root / '.lecture'
    if local.is_dir():
        print('Already initialized', file=sys.stderr)
    copytree(str(template_dir), str(local))
    print('Initialized lecture directory')
    print(f"Template stored in '{local}'")

def new(args):
    new_dir = root / args.name
    if new_dir.exists():
        print(f"File or directory '{args.name}' already exists")
        return
    new_dir.mkdir()
    lecture_file = new_dir / f'{args.name}.md'
    lecture_file.write_text(TEMPLATE)


def make(args):
    target = _find_file(args)
    print(f"Making '{target}'...")
    _make_file(target)
    print('Done')

def watch(args):
    to_watch = _find_file(args)
    print(f"Watching '{to_watch}'")
    print(f"Press Ctrl+C to stop")
    to_watch_name = str(to_watch)
    _make_file(to_watch)

    class Handler(FileSystemEventHandler):
        def on_modified(self, event):
            if event.event_type == 'modified':
                if event.src_path == to_watch_name:
                    print('Change detected, building...')
                    _make_file(to_watch)
                    print('Done')

    if args.pdf_viewer:
        subprocess.Popen([args.pdf_viewer, str(_pdf(to_watch))])
    observer = Observer()
    observer.schedule(Handler(), str(to_watch.parent))
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print('Exiting')

def _executable(f):
    res = which(f)
    if not res:
        raise argparse.ArgumentError(f"'{f}' is not an executable")
    return res

def _file_or_dir(f):
    res = Path(f)
    if not res.exists():
        raise argparse.ArgumentError(f"'{f}' is not a file or directory")
    return res.resolve()

def main():
    # create the top-level parser
    parser = argparse.ArgumentParser(description='Create PDF lecture slides from markdown files.')
    parser.set_defaults(func=lambda _: parser.print_help())
    subparsers = parser.add_subparsers()

    parser_init = subparsers.add_parser('init', help='Initialize a directory for lectures. Creeates a template folder that is used for all slides generated in its subdirectories.')
    parser_init.set_defaults(func=init)

    parser_make = subparsers.add_parser('make', help='Build a PDF lecture from a markdown file.')
    parser_make.add_argument('target', metavar='TARGET', nargs='?', type=_file_or_dir, default=None, help='If TARGET is a file, that file is built. If TARGET is a directory, it is searched for .md files and the first one is built. If TARGET is not specified, the current directory is searched for .md files and the first one found is built.')
    parser_make.set_defaults(func=make)

    parser_new = subparsers.add_parser('new', help='Create and initialize a new markdown file for a lecture.')
    parser_new.add_argument('name', metavar='NAME')
    parser_new.set_defaults(func=new)

    parser_watch = subparsers.add_parser('watch', help='Monitor a markdown file and build a PDF lecture when it changes.')
    parser_watch.add_argument('-v', '--pdf-viewer', metavar='VIEWER', type=_executable, default=None, help='If specified, opens the built PDF file in the viewer when started.')
    parser_watch.add_argument('target', metavar='TARGET', nargs='?', type=_file_or_dir, default=None,help='If TARGET is a file, that file is built. If TARGET is a directory, it is searched for .md files and the first one is built. If TARGET is not specified, the current directory is searched for .md files and the first one found is built.')
    parser_watch.set_defaults(func=watch)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()

