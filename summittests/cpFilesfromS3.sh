#assumes you already logged in to mycloud with  mc where mycloud is the s3 endpoint URL

for f in `mc ls  mycloud/rubin-summit-users/test-lhn/ | cut -d' '  -f 7` ; do 
   s3="mycloud/rubin-summit-users/test-lhn/$f"
   mc cp  $s3 /tmp/Test/$f.fits
done

