rm /data/local/tmp/as.bak
mv /data/local/tmp/as.tar /data/local/tmp/as.bak
echo '--start--------------'
echo 'cd /data/data/com.nintendo.zaga/files/assets; tar cf /data/local/tmp/as.tar `ls -al|grep $(date +"%m-%d")|cut -d " " -f12`'
echo '--end----------------'
