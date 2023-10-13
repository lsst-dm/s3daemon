# Simple config for s3daemon
# assumes s3daemon has been installed or pip install -r of its requirements.txt
# see https://github.com/lsst-dm/s3daemon/blob/main/README.md


source  envvars.sh

echo "S3_ENDPOINT_URL is $S3_ENDPOINT_URL"

python ../python/s3daemon/s3daemon.py &
