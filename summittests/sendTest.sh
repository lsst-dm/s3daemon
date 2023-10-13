# Simple send 20 files each in own thrread like a node for camera
# assumes s3daemon has been installed or pip install -r of its requirements.txt
# see https://github.com/lsst-dm/s3daemon/blob/main/README.md


source  envvars.sh
source venv/bin/activate



repeat=2
if [ $1 ] 
then
  repeat="$1"
fi
echo "$HOSTNAME S3_ENDPOINT_URL is $S3_ENDPOINT_URL  repeat $repeat $prefix"

files=`ls  ~tonyj/Test/MC*/* | head -${count}`

fcount=0
l=0

while [[ l -le repeat ]] 
do
l=$((l + 1))
for f in $files; do 
   key=`echo $f | cut -d'/' -f6 | sed 's/.fits//g'`
   python ../python/s3daemon/send.py $f /${bucket}/${prefix}/${key} & 
   fcount=$((fcount + 1))
   if [ $((fcount % 20)) ==  0 ]
      echo Sent $key total $fcount
   then
       sleep 20s
       echo "Sleeping"
   fi 
done
done
