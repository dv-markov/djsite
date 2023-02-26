# -*- coding: utf-8 -*-
import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.insert(0, '/home/d/dmarkov/dmarkov.beget.tech/valveadvisor')
sys.path.insert(1, '/home/d/dmarkov/dmarkov.beget.tech/djangoenv/lib/python3.11/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'valveadvisor.settings'

application = get_wsgi_application()
