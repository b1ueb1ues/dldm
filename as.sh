rm /data/local/tmp/as.bak
mv /data/local/tmp/as.tar /data/local/tmp/as.bak
tar -c -f /data/local/tmp/as.tar -C /data/data/com.nintendo.zaga/files assets
echo '--end----------------'
