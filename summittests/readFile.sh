# just read the file  noop
# see https://github.com/lsst-dm/s3daemon/blob/main/README.md


if [ $1 ]
then
  f="$1"
else
  echo "Specify file "
  exit 1
fi

start=`date +%s`
while IFS= read -r line
do
   : # nothing
done <"$f"
end=`date +%s`
echo Reading $f `expr $end - $start` seconds 
