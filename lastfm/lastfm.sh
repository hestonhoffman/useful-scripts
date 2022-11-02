#!/bin/bash

# Add to an alias in your ~./bashrc or ~/.zshrc.

year=`date +'%Y'`
username='mthrl'
URL="https://www.last.fm/user/$username/library/tracks?from=$year-01-01&rangetype=year"
ostype=`echo $OSTYPE`

case $ostype in
*"linux"*) xdg-open $URL;;
*"darwin"*) open $URL;;
esac
