dir=`dirname $0`
adb push $dir/device/as.sh /data/local/tmp
adb shell su -c 'sh /data/local/tmp/as.sh'
