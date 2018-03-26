from datetime import timedelta

from django.conf import settings as django_settings
from django.utils.text import slugify

from .apps import CeleryGrowthMonitorConfig as appConfig

TTL = getattr(django_settings, '{}_TTL'.format(appConfig.name.upper()),
              getattr(django_settings, 'CELERY_TASK_RESULT_EXPIRES',
                      timedelta(10)))  # 10 days
"""
Time to live. After that time, jobs should be dropped from file system.
"""

APP_MEDIA_ROOT = getattr(django_settings, '{}_MEDIA_ROOT'.format(appConfig.name.upper()), '')

SLUGIFIER = getattr(django_settings, '{}_SLUGIFY_FUNCTION'.format(appConfig.name.upper()),
                    getattr(django_settings, 'AUTOSLUG_SLUGIFY_FUNCTION', slugify))
