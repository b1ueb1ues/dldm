rm /data/local/tmp/as.bak
mv /data/local/tmp/as.tar /data/local/tmp/as.bak
echo 'tar -c -f /data/local/tmp/as.tar -C /data/data/com.nintendo.zaga/files assets'
echo '--start--------------'
tar -c -f /data/local/tmp/as.tar -C /data/data/com.nintendo.zaga/files assets
echo '--end----------------'
