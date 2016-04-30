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
from http.server import SimpleHTTPRequestHandler
from http.server import HTTPServer
import threading

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
        fh.write(bytes(output_from_parsed_template, encoding='utf-8'))


def observe():
    print('watching slides folder...')
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = 'slides'
    event_handler = BuildEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    return observer


def serve():
    port = 8081
    server = HTTPServer(('', port), SimpleHTTPRequestHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = False

    print('serving on %s...' % port)
    return thread

def main(args=None):
    parser = argparse.ArgumentParser(description="keep track what you are doing.")
    parser.add_argument("--watch",
                        help="rebuild everytime something changes", action='store_true')
    parser.add_argument("--serve",
                        help="start httpserver", action='store_true')

    args = parser.parse_args()

    threads = []

    if args.watch:
        threads.append(observe())
    if args.serve:
        threads.append(serve())

    #try:
    #    while True:
    #        time.sleep(2)
    #except KeyboardInterrupt:
    #    observer.stop()
    #observer.join()

    else:
        build()

    try:
        for t in threads:
            t.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for t in threads:
            #t.stop()
            t.join()
        # server.shutdown()
        sys.exit(0)


if __name__ == '__main__':
    main()
