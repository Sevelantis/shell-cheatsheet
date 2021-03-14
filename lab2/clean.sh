#!/bin/bash

DFLT1="lab_uno"
DFLT2="bakap"

# przypisz wartosc default lub wartosc odpowiedniego argumentu
SOURCE_DIR="${1:-${DFLT1}}"
TARGET_DIR="${2:-${DFLT2}}"

DATE=$(date +"%Y-%m-%d") # today RRRR-MM-DD
ZIP_OUT="bakap_${DATE}.zip"

sudo rm -r $SOURCE_DIR
sudo rm $ZIP_OUT
sudo rm -r $TARGET_DIR