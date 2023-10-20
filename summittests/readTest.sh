# Simple read 20 files each in own thread for a node for camera
# this is just to see the times for the read as opposed to send
# see https://github.com/lsst-dm/s3daemon/blob/main/README.md


source  envvars.sh

totalfiles=20
if [ $1 ] 
then
  repeat="$1"
fi
echo "Just read total $totalfiles"

files=`ls   ${datadir}/MC*/* `

fcount=0

while [[ fcount -le totalfiles ]] 
do
for f in $files; do 

   ./readFile.sh  $f  &

   fcount=$((fcount + 1))
   if [[ fcount -ge totalfiles ]]
   then
      break
   fi
   if [ $((fcount % 20)) ==  0 ]
   then
       sleep 20s
       echo "Sleeping after $fcount"
   fi 
done
done
