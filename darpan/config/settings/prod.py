from .base import *  # noqa

DEBUG = False

SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=['darpandeva.com', 'www.darpandeva.com', 'darpandeva.com.br', 'www.darpandeva.com.br'])
