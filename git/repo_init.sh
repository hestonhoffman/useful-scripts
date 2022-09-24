#! bin/bash

# 1. Make sure you're authed: `gh auth login`
# 2. Remember to pass the name of the repo in as an argument.

if [[ $# -eq 0 ]] ; then
    echo 'ERROR: No arguments given.'
    echo 'Pass the name of the repo you want to create into the script'
    exit 0
else
    touch README.md
    git init
    git add README.md
    gh repo create hestonhoffman/$1 --public --source=. --remote=origin
    git branch -m main
    git commit -m "Initial commit"
    git push origin -u main 
    URL="https://github.com/hestonhoffman/$1"
    open $URL || xdg-open $URL || sensible-browser $URL || x-www-browser $URL || gnome-open $URL
fi
