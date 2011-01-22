# Create a brand new django app:
# django-admin.py startproject deleteme
# cd deleteme
# virtualenv .
# source bin/activate
# pip install lettuce
# pip install selenium
# pip install random_instances
# pip install -e git+git://github.com/ff0000/radish.git#egg=radish
# SWITCH TO THIS BRANCH
# (add 'lettuce.django' to INSTALLED_APPS)
# (add 'radish' to INSTALLED_APPS)
# (set the DB in settings then):
# python manage.py syncdb
# Add the following at the top of the project's settings (THIS HAS TO CHANGE):
# import os.path, sys
# PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
# APPS_ROOT = os.path.join(PROJECT_ROOT, "apps")
# sys.path.insert(0, APPS_ROOT)
#
# finally
# python manage.py harvest
#
# and a model should be there
#
# TODO: Maybe all of this is already done by django-admin.py createapp
# Check that code!

from lettuce import *
from nose.tools import assert_equals

# TODO: The following has definitely to change!
# radish cannot be aware of the name of the outer project
# And we cannot assume that project will have APPS_ROOT, PROJECT_ROOT
from deleteme.settings import APPS_ROOT, PROJECT_ROOT, INSTALLED_APPS

import os

def pluralize(word):
    return word + 's' # Best so far

def modelize(word):
    return word.capitalize() # Best so far

@step(u'there is no (.+)$')
def there_is_no_instance(step, model_name):
    from django.contrib.contenttypes.models import ContentType
    from django.core.exceptions import ObjectDoesNotExist
    try:
        model = ContentType.objects.get(model=model_name).model_class()
    except ObjectDoesNotExist:
        # create walnuts/ folder
        app_dir = os.path.join(APPS_ROOT, pluralize(model_name))        
        if not os.path.exists(app_dir):
            os.makedirs(app_dir)
        # create __init__.py
        if not os.path.exists(os.path.join(app_dir, '__init__.py')):
            with open(os.path.join(app_dir, '__init__.py'), 'w') as f:
                f.write("# Created by the farmer\n")
        # create models.py
        if not os.path.exists(os.path.join(app_dir, 'models.py')):
            with open(os.path.join(app_dir, 'models.py'), 'a') as f:
                f.write("# Created by the farmer\n")
                f.write("from django.db import models\n")
                f.write("class %s(models.Model):\n" % modelize(model_name))
                f.write("  pass\n")
        # create admin.py
        if not os.path.exists(os.path.join(app_dir, 'admin.py')):
            with open(os.path.join(app_dir, 'admin.py'), 'a') as f:
                f.write("# Created by the farmer\n")
                f.write("from django.contrib import admin\n")
                f.write("admin.site.register(%s)\n" % modelize(model_name))
        
        # add walnuts to INSTALLED_APPS
        with open(os.path.join(PROJECT_ROOT, 'settings.py'),'r') as f:
            lines = f.readlines()
        where = lines.index('INSTALLED_APPS = (\n')+1 # would be better at the end
        lines.insert(where, "    '%s',\n" % pluralize(model_name))
        with open(os.path.join(PROJECT_ROOT, 'settings.py'),'w') as f:
            f.writelines(lines)

        # Create the table, sync and reload
        from mgr import TestSettingsManager
        installed_apps = list(INSTALLED_APPS) + [pluralize(model_name)]
        mgr2 = TestSettingsManager()
        mgr2.set(INSTALLED_APPS=tuple(installed_apps))

        # finally load the model
        exec('from %s.models import %s' % (pluralize(model_name), modelize(model_name)))
        model = eval(modelize(model_name))
        
        ## TODO: At the end mgr2.revert()
        
    # And now we can finally check that no instances are there
    model.objects.all().delete()
