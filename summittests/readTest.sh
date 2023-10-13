# Simple read 20 files each in own thread for a node for camera
# this is just to see the times for the read as opposed to send
# see https://github.com/lsst-dm/s3daemon/blob/main/README.md


source  envvars.sh
source venv/bin/activate



repeat=2
if [ $1 ] 
then
  repeat="$1"
fi
echo "Just read   repeat $repeat"

files=`ls  ~tonyj/Test/MC*/* | head -${count}`

fcount=0
l=0

while [[ l -le repeat ]] 
do
l=$((l + 1))
for f in $files; do 
   key=`echo $f | cut -d'/' -f6 | sed 's/.fits//g'`

   ./readFile.sh  $f  &

   fcount=$((fcount + 1))
   if [ $((fcount % 20)) ==  0 ]
   then
       sleep 20s
       echo "Sleeping"
   fi 
done
done
