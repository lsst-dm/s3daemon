# Simple config for s3daemon
# eventually this shoudl be installed and excuted by puppe on every node
# assumes s3daemon has been installed or pip install -r of its requirements.txt
# see https://github.com/lsst-dm/s3daemon/blob/main/README.md

# Note to jump between lsstcam nodes use 'kinit' since ipa controls it all


source  envvars.sh
source venv/bin/activate

host=`echo $HOSTNAME | cut -d'.' -f1`
logfile="${host}-s3daemon.log"

echo "S3_ENDPOINT_URL is $S3_ENDPOINT_URL"

python ../python/s3daemon/s3daemon.py > $logfile  2>&1 &
