#!/usr/bin/env python
# -*- coding: utf-8 -*-
from project import app, socketio

if __name__ == '__main__':
    socketio.run(app, debug=True)
