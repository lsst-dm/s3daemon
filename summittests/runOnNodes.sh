# use ssh to run given scrip on all the nodes in $nodes

# Note to jump between lsstcam nodes use 'kinit' since ipa controls it all


source  envvars.sh

cmd="$@"

for n in $nodes; do 
   exec="cd s3daemon/summittests; ${cmd}" 
   echo $exec
   ssh $n "${exec}" &
   done
