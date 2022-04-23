#!/bin/sh
#rm *.log *.out
rm -rf /data/html
if [ ! -d /data ]; then
    mkdir -p /data/image
	mkdir -p /data/photo	
	mkdir -p /data/database
	mkdir -p /data/download
	mkdir -p /data/photo/thumbnails
	rm -rf /data/html
	cp -rf html/ /data/
	chmod -R 755 /data

fi;

rm -f /data/image
rm -f /data/html
cp -rf html/ /data/
chmod  -R 755 /data

python AppMgr.py
nginx -s reload
#aria2c --enable-rpc --rpc-listen-all
#sqlite_web data/database/database.db
