#!/usr/bin/env python

import os
import sys
import optparse

from django.conf import settings
from django.core.management import call_command

parser = optparse.OptionParser()
opts, args = parser.parse_args()

directory = os.path.abspath('%s' % os.path.dirname(__file__))

if not settings.configured:
    jenkins = []
    db_name = 'test_treenav'
    if 'jenkins' in args:
        jenkins = ['django_jenkins']
        db_name = "treenav_%s" % os.environ.get('TESTENV', db_name)

    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'treenav',
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': '',
                'TEST_NAME': db_name,
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'mptt',
            'treenav',
        ] + jenkins,
        SITE_ID=1,
        ROOT_URLCONF='treenav.urls',
        TEMPLATE_LOADERS=(
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ),
        TEMPLATE_CONTEXT_PROCESSORS=(
            "treenav.context_processors.treenav_active",
            'django.core.context_processors.request',
        ),
        TEMPLATE_DIRS=(
            '%s/sample_project/templates' % directory,
        ),
        PASSWORD_HASHERS=['django.contrib.auth.hashers.MD5PasswordHasher'],  # Increase speed in 1.4
        PROJECT_APPS=('treenav',),
        JENKINS_TASKS=(
            'django_jenkins.tasks.with_coverage',
            'django_jenkins.tasks.django_tests',
            'django_jenkins.tasks.run_pep8',
        ),
    )


def run_jenkins_tests():
    kwargs = {
        'pep8-exclude': 'migrations',
        'pep8-select': '',
        'pep8-ignore': '',
        'pep8-max-line-length': 80,
        'coverage-exclude': 'treenav.migrations',
        'coverage_with_migrations': False,
        'coverage_html_report_dir': '',
        'coverage_excludes': [],
        'coverage_measure_branch': False,
        'coverage_rcfile': '',
        'output_dir': 'reports/',
    }
    call_command('jenkins', **kwargs)


from django.test.utils import get_runner


def run_django_tests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['treenav'])
    sys.exit(failures)


def run():
    if 'jenkins' in args:
        run_jenkins_tests()
    else:
        run_django_tests()

if __name__ == '__main__':
    run()
