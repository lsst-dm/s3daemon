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
echo "$HOSTNAME S3_ENDPOINT_URL is $S3_ENDPOINT_URL  repeat $repeat $datadir"

files=`ls  ${datadir}/MC*/* `

fcount=0
l=0

while [[ l -le repeat ]] 
do
echo Repetition number $l out of $repeat on $HOSTNAME
l=$((l + 1))
for f in $files; do 
   key=`echo $f | cut -d'/' -f6`
   python ../python/s3daemon/send.py $f /${bucket}/${prefix}/${key} & 
   fcount=$((fcount + 1))
   if [ $((fcount % 20)) ==  0 ]
   then
       echo Sent $key total $fcount
       echo "Sleeping"
       sleep 20s
   fi 
done
done
echo Sent total $fcount from $HOSTNAME to $S3_ENDPOINT_URL