## [Digital Ocean sub domain](https://www.digitalocean.com/community/questions/automatically-create-users-subdomain-with-sub-folders-in-do-with-nginx)

If you plan to have all the subdomains of your domain pointed to the same droplet then you can create a wildcard DNS entry to point any subdomain that is encountered to your server. To do this, simply create the following record:

	*     CNAME     @

## Apache config

	<VirtualHost *:80>
	    ServerName suhail.pw
	    ServerAlias *.suhail.pw
	    WSGIDaemonProcess upworkapp python-home=/var/www/subdomain/env python-path=/var/www/subdomain
	    WSGIProcessGroup upworkapp
	    WSGIScriptAlias / /var/www/subdomain/mysite/wsgi.py
	    ErrorLog /var/www/subdomain/error.log
	    CustomLog /var/www/subdomain/access.log combined
	</VirtualHost>


## Localhost

	www.mysite.local
	help.mysite.local
