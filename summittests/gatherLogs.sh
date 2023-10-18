# pull all logs back to main node
# Assumes you are in the simmit tests directory
#

# Note to jump between lsstcam nodes use 'kinit' since ipa controls it all


source  envvars.sh

pwd=`pwd`
for n in $nodes; do 
   scp ${n}:${pwd}/*log logs
   done
