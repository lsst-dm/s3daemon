# find the process and kill

#proc=`ps -ealf | grep s3daem | grep -v grep | cut -d' ' -f5`
#kill -9 $proc
pkill -if '.*s3daemon.*' 
