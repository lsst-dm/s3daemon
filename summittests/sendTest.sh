# Simple send 20 files each in own thrread like a node for camera
# assumes s3daemon has been installed or pip install -r of its requirements.txt
# see https://github.com/lsst-dm/s3daemon/blob/main/README.md


source  envvars.sh
source venv/bin/activate

echo "S3_ENDPOINT_URL is $S3_ENDPOINT_URL"
count=20

files=`ls  ~tonyj/Test/MC*/* | head -${count}`

fcount=0
for f in $files; do 
   key=`echo $f | cut -d'/' -f6 | sed 's/.fits//g'`
   echo Sending $f $key
   python ../python/s3daemon/send.py $f “/${bucket}/${prefix}/${key}” & 
   fcount=$((fcount + 1))
   if [ $((fcount % 20)) ==  0 ]
   then
       sleep 20s
       echo "Sleeping"
   fi 
done
