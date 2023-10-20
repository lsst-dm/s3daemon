# Simple send 20 files each in own thrread like a node for camera
# assumes s3daemon has been installed or pip install -r of its requirements.txt
# see https://github.com/lsst-dm/s3daemon/blob/main/README.md


source  envvars.sh
source venv/bin/activate



total=2
if [ $1 ] 
then
  total="$1"
fi
echo "$HOSTNAME S3_ENDPOINT_URL is $S3_ENDPOINT_URL  total $total $datadir"

files=`ls  ${datadir}/MC*/* `

fcount=0

while [[ fcount -le total ]] 
do
for f in $files; do 
   key=`echo $f | cut -d'/' -f6`
   python ../python/s3daemon/send.py $f /${bucket}/${prefix}/${key} & 
   fcount=$((fcount + 1))
   if [[ fcount -ge total0 ]]
   then
       break
   fi
   if [ $((fcount % 20)) ==  0 ]
   then
       echo Sent $key total $fcount
       echo "Sleeping"
       sleep 20s
   fi 
done
done
echo Sent  total $fcount
