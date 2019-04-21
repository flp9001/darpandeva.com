#!/bin/bash
cp -r server/ /
systemctl daemon-reload
service gunicorn-darpan stop
service nginx stop
service gunicorn-darpan start
service nginx start
