#!/bin/bash

bdir=$( dirname $0 )
current=$(pwd)

case $bdir in
    ".") BASE_DIR=$( dirname $current );;
    ..*) 
	current=$( dirname $current )
	bdir=$( echo $bdir |sed 's:^../::g' )
	BASE_DIR=$( dirname $current/$bdir )
	;;
    /*) BASE_DIR=$( dirname $bdir );;
    *) BASE_DIR=$( dirname $current/$bdir );;
esac

echo $BASE_DIR

mkdir -p $BASE_DIR/{static,database}

cd $BASE_DIR/costruttoridimondi

./manage.py migrate --noinput
./manage.py collectstatic --noinput

chmod ug+s $BASE_DIR/database
chgrp -R www-data $BASE_DIR/database
chmod -R ug+w $BASE_DIR/database
