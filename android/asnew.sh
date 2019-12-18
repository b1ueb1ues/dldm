rm /data/local/tmp/asnew.tar
echo '--start--------------'
echo 'cd /data/data/com.nintendo.zaga/files; tar cf /data/local/tmp/asnew.tar `find assets -mtime -2d -type f`'
cd /data/data/com.nintendo.zaga/files; tar cf /data/local/tmp/asnew.tar `find assets -mtime -2d -type f`
echo '--end----------------'
