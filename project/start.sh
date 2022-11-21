#!/bin/bash
gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 --reload -b 0.0.0.0:8060 app:app