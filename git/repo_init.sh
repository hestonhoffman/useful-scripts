#! bin/bash

# 1. Make sure you're authed: `gh auth login`
# 2. Remember to pass the name of the repo in as an argument.

if [[ $# -eq 0 ]] ; then
    echo 'ERROR: No arguments given.'
    echo 'Pass the name of the repo you want to create into the script'
    exit 0
fi

case "$1" in
    touch README.md
    git init
    git add README.md
    gh repo create hestonhoffman/$1 --public --source=. --remote=upstream
    git remote add origin git@github:hestonhoffman/$1
    git branch -m main
    git commit -m "Initial commit"
    git push origin -u main
esac
