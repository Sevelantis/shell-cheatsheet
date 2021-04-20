#!/bin/bash -eu

# Zajęcia 3
# materials https://www.cyberciti.biz/faq/howto-use-grep-command-in-linux-unix/
FILE="access_log"

# denied w linku
cat ${FILE} | grep denied | grep -P 'GET|POST|DELETE|CREATE|READ|INSERT|SELECT|UPDATE'
# POST
cat ${FILE} | grep '"POST /'
# 64.242.88.10
cat ${FILE} | grep -w '^64\.242\.88\.10'    # exact search -w
# niewyslane z 64.242.88.10
cat ${FILE} | grep -v '^[0-9\.]' | grep -P '^[a-zA-Z0-9\-\.]+' #-P perl
# unikalne DELETE
cat acc | grep -P 'DELETE .*?"' | sort -u
# unikalne 10  adresow ip
cat ${FILE} | grep -P '^([0-9]+\.){3}([0-9]+)' | sort -u | head -10

# nieparzyste id
cat yolo.csv | grep -P '^\d+[13579],' 1>&2 
# 2.99 5.99 9.99 value ludzi
cat yolo.csv | grep -P '\$[259]\.99[BM]' | cut -d',' -f2,7
# adres ip ma jednocyfrowe dwa pierwsze oktety
cat yolo.csv | cut -d',' -f6 | grep -P '^[0-9]\.[0-9]\.' 1>&2

# zamiana /temat/ na /temat/
DIR='groovies'
cd ${DIR}
for file in $(ls); do
    sed -i 's|\$HEADER\$|/temat/|g' ${file}
done

# po kazdej lini dodac nowa linie
for file in $(ls); do
    sed -i "/class.*/a \ String marker = \'\!\@\$\%\/\'" ${file}
done

# po kazdej lini dodac nowa linie
for file in $(ls); do
    sed -i "/class.*/a \ String marker = \'\!\@\$\%\/\'" ${file}
done

# usuwanie linii z help docs
for file in $(ls); do
    sed -i "/Help docs:/d" ${file}
done
