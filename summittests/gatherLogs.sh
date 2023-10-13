# put the scripts on all the nodes

# Note to jump between lsstcam nodes use 'kinit' since ipa controls it all


source  envvars.sh


for n in $nodes; do 
   scp ${n}:/home/womullan/s3daemon/summittests/*log logs
   done
