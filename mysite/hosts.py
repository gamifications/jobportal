from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
	host(r'www', settings.ROOT_URLCONF, name='www'),
    host(r'(\w+)', 'company.urls', name='wildcard'),
    # host(r'(?!www)\w+', 'company.urls', name='wildcard'),
)

