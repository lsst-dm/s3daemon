# Simple send 20 files each in own thrread like a node for camera
# assumes s3daemon has been installed or pip install -r of its requirements.txt
# see https://github.com/lsst-dm/s3daemon/blob/main/README.md


source  envvars.sh

echo "S3_ENDPOINT_URL is $S3_ENDPOINT_URL"
count=20

files=`ls ~tonyj/Data/MC_C_20200822_000054/MC_C_20200822* | head -${count}`
echo $files
for f in $files; do 
   key=`echo $f | cut -d'/' -f6 | sed 's/.fits//g'`
   echo Sending $f $key
   python ../python/s3daemon/send.py $f “/${bucket}/${prefix}/${key}” & 
   done
