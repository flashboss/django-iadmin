==============
Django iAdmin
==============

iAdmin is a replacement of standard django admin application.

Features
--------

- multiple columns portlets-like home page
- tabbed view of inlines
- mass updates functionality
- export to csv with options and formatting
- advanced import from csv with foreign key handling
- link to foreignkey edit page from changelist (list_display_rel_links)
- filter by cell values (cell_filters)
- ajax autocomplete widgets for ForeignKey

Please read online documentation at http://packages.python.org/django-iadmin/

Project links
-------------

* Project home page: https://github.com/saxix/django-iadmin
* Isssue tracker: https://github.com/saxix/django-iadmin/issues?sort
* Documentation: http://packages.python.org/django-iadmin/
* Download: http://pypi.python.org/pypi/django-iadmin/
* Mailing-list: django-iadmin@googlegroups.com

Install
----
Edit your settings.py and add iadmin application before django.contrib.admin ::

    INSTALLED_APPS = (
        ...
        'iadmin',
        'django.contrib.admin',
        'django.contrib.messages',
        ...
        ...
    )


    # iAdmin use STATIC_URL. You have to create this entry. Use this lines ONLY if you don't use staticfiles app,
    # leave your STATIC_* configuration otherwise
    STATIC_URL = '/s/static/'
    STATIC_ROOT = MEDIA_ROOT

Add an entry into your urls.conf ::

    from django.conf.urls.defaults import *
    import iadmin.proxy as admin

    admin.autodiscover()

    urlpatterns = patterns('',
            (r'', include('iadmin.media_urls')), # only for development
            (r'^admin/', include(admin.site.urls)),
    )


In your admin.py file ::

    from django.contrib.admin.options import TabularInline
    from geo.models import Country, Lake, Location, Ocean

    from iadmin.utils import tabular_factory


Plugins
----
To add the File Manager in the admin console

Add this variables at the beginning of your settings.py ::

	import iadmin
	import os
	import sys
	HERE = os.path.dirname('__file__')
	sys.path.insert(0, os.path.join(HERE, os.pardir) )
	__IADMIN_ROOT = os.path.abspath(os.path.dirname(iadmin.__file__))
	IADMIN_FILE_UPLOAD_MAX_SIZE = 2000000
	IADMIN_FM_ROOT = os.path.join(__IADMIN_ROOT, 'tests', 'fmenv')
        IADMIN_FM_CONFIG = {}
	
Add the row in the TEMPLATE_DIRS variable ::

    TEMPLATE_DIRS = (
          ...
          os.path.join(HERE, 'templates'),
          ...
          ...
    )
    
Create the directory templates in your project and overwrite the page base_site.html so ::

    {% extends "iadmin/base_site.html" %}
