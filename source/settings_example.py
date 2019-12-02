from settings_base import *

# Absolute path to project root
PROJECT_ROOT = 'c:/users/kao/Desktop/AI_Project/planner/'
ADMIN_MEDIA_ROOT = PROJECT_ROOT + 'admin-media'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'planner',       # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = PROJECT_ROOT + 'media/'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # NOTE: I suggust everyone using the same path as me
    PROJECT_ROOT + 'templates/',
    
)

FIXTURE_DIRS = (
    PROJECT_ROOT + 'fixtures',
)
