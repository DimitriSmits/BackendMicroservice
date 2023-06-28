"""
This module contains functions for performing the settings.
"""
import json
from dotenv import load_dotenv

load_dotenv()
import os
from sys import argv
from common import get_json_env

#Default local json env
# os.environ['APP_SECRET'] = json.dumps('secret')
# os.environ['POSTGRES_USER'] = json.dumps('postgres')
# os.environ['POSTGRES_PASSWORD'] = json.dumps('admin')
# os.environ['POSTGRES_DB'] = json.dumps('postgres')
# os.environ['POSTGRES_HOSTNAME'] = json.dumps('localhost:5432')

# Secret used for various parts of the application, for example as a salt to password hashing
APP_SECRET = 'APP_SECRET'


# Is automatically set to True whenever Alembic is used with either the upgrade, downgrade or current option.
# We use this flag to dynamically import models that represent database views, which may not yet exist in the db.
MIGRATING_DB = 'upgrade' in argv \
                or 'downgrade' in argv \
                or 'current' in argv


# CORS settings -- CORS can be enabled for development purposes, since different ports on localhost are considered as different origins.
# In production, if both the frontend and the backend run on the same domain, CORS should be disabled
CORS_ENABLED = get_json_env('CORS_ENABLED', False)
CORS_ALLOWED_ORIGINS = get_json_env('CORS_ALLOWED_ORIGINS', [])


# Database settings
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOSTNAME = os.getenv('POSTGRES_HOSTNAME')
CONN_STRING = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}/{POSTGRES_DB}'
ASYNC_CONN_STRING = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}/{POSTGRES_DB}'

# The default name to use for the root cluster
ROOT_CLUSTER_NAME = 'Products'


# In development, the register-user route may not need to be protected
REGISTER_ROUTE_PROTECTED = get_json_env('REGISTER_ROUTE_PROTECTED', True)


# An absolute path to the directory that media is stored in, for example the exports that are created by the application.
# This directory is mounted to the docker-host, so that the content of this folder will persist on disk. 
MEDIA_ROOT = get_json_env('MEDIA_ROOT', '/app/media/')
