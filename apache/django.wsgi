
import os,sys

os.environ['DJANGO_SETTINGS_MODULE']='bl.settings'

path = '/var/www/bl'
if path not in sys.path:
        sys.path.append(path)

import django.core.handlers.wsgi

application=django.core.handlers.wsgi.WSGIHandler()

