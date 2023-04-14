public/emse/.htaccess: public
	printf "DirectoryIndex index.ttl\nOptions +Indexes +MultiViews" > public/.htaccess

sync:
	rsync --delete -rcv public/ ci:/var/www/html/knx/
