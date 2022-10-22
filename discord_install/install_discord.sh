#!/bin/bash

wget "https://discordapp.com/api/download/stable?platform=linux&format=tar.gz" -O ~/Downloads/discord.tar.gz
file=~/Downloads/discord.tar.gz
sudo tar -zxvf $file -C /opt/
rm $file