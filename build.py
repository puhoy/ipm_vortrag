# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input

import argparse


import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingFileSystemEventHandler

from jinja2 import Environment, FileSystemLoader


class BuildEventHandler(LoggingFileSystemEventHandler):
    def on_any_event(self, event):
        super(BuildEventHandler, self).on_any_event(event)
        build()


def build():
    print('building...')
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('index.html.j2')
    output_from_parsed_template = template.render()

    with open("index.html", "wb") as fh:
        fh.write(output_from_parsed_template)


def observe():
    print('watching slides folder...')
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = 'slides'
    event_handler = BuildEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main(args=None):
    parser = argparse.ArgumentParser(description="keep track what you are doing.")
    parser.add_argument("--watch",
                        help="rebuild everytime something changes", action='store_true')

    args = parser.parse_args()

    if args.watch:
        observe()
    else:
        build()


if __name__ == '__main__':
    main()
