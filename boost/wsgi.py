import os

import sys

sys.path.append('/opt/bitnami/projects/boost')

sys.path.append('/opt/bitnami/projects/boost/boost')





#sys.path.insert(0, '/opt/bitnami/apps/django/django_projects/my_app')

os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/projects/boost/egg_cache")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boost.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
