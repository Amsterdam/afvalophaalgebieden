#!/usr/bin/env python

import os
import sys

from app.import_jobs import run as run_import


def shell():
    """Start app shell"""
    os.environ['PYTHONINSPECT'] = 'True'


def run_server():
    app.run(debug=True, host='0.0.0.0')


def create_all():
    with app.app_context():
        db.create_all()


def main():
    # Parsing args
    if len(sys.argv) == 1:
        shell()
    else:
        if sys.argv[1] == 'run':
            os.environ['TESTING'] = False
            run_server()
        if sys.argv[1] == 'import':
            os.environ['TESTING'] = False
            run_import()
        if sys.argv[1] == 'test':
            os.environ['TESTING'] = True
            run_server()
        elif sys.argv[1] == 'createall':
            os.environ['TESTING'] = False
            create_all()
        else:
            print('Unkown command')

if __name__ == '__main__':
    main()
