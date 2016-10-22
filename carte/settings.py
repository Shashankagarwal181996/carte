import dj_database_url
DATABASES={}
DATABASES['default'] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']
SECRET_KEY = '$ep*%(ffh29!z+^fge2sw317j(!)gx7d--la^eb@xtmj&mu!y)'
DEBUG = False

try:
    from .local_settings import *
except ImportError:
    pass
