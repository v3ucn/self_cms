#!/bin/bash

#/home/qfpay/python/bin/gunicorn -c ../conf/gunicorn_setting.py server:app
gunicorn -c ../conf/gunicorn_setting.py server:app
