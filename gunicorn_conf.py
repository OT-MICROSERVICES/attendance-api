"""
Module for custom json log model in flask and gunicorn
"""
# pylint: disable=invalid-name

import json

bind = '0.0.0.0:8080'
workers = 3
accesslog = '-'  # Send access logs to stdout

access_log_format = json.dumps({
    'remote_address': r'%(h)s',
    'user_name': r'%(u)s',
    'date': r'%(t)s',
    'status': r'%(s)s',
    'method': r'%(m)s',
    'url_path': r'%(U)s',
    'query_string': r'%(q)s',
    'protocol': r'%(H)s',
    'response_length': r'%(B)s',
    'referer': r'%(f)s',
    'user_agent': r'%(a)s',
    'request_time_seconds': r'%(L)s',
})
