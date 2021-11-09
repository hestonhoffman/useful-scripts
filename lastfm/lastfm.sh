#!/bin/bash

# Add to an alias in your ~./bashrc or ~/.zshrc.

year=`date +'%Y'`
username='mthrl'
URL="https://www.last.fm/user/$username/library/tracks?from=$year-01-01&rangetype=year"

open $URL || xdg-open $URL || sensible-browser $URL || x-www-browser $URL || gnome-open $URL