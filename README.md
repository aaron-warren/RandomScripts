# Random Scripts

This repo just contains scripts that I've made to make some actions easier to accomplish.

## ElvUI-update.py

ElvUI is a common addon used in a popular game WoW. The addon checks the website for the latest version and then compares it to the one cached on the local computer. If a newer version is found then it will download it, install it, delete the old files, and then display the changelog for the newest version.

## renameTV.py

A simple script that can be placed in a folder and then ran with `python renameTV.py --name='name of show' --season='season being renamed'`. Example: `python renameTV.py --name='BSG' --season=1`. All this script does is then gather all the files in the folder, sort them, then prepare to rename them to be easier to process by applications like Sonarr.
