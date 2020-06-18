#!/bin/sh
echo '-- clean ----'
rm as.tar
rm -rf assets
echo '-- pull ----'
adb pull /data/local/tmp/as.tar
echo '-- extract ----'
tar xf as.tar
