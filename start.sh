#!/bin/sh

RED='\033[0;31m'
NC='\033[0m' # No Color

if [ ! -d olaf_venv ] ; then
  printf "${RED}Creating new venv ${NC}"
  python3 -m venv olaf_venv
  NEW_VENV=true
fi

source *venv/bin/activate
if [ ! -n $NEW_VENV ] ; then
  printf "${RED}installing requierments ${NC}"
  pip install -r ./requirements.txt
fi

python3 ./Assembler/assembler.py
printf "${RED}Please load the OS and the initram files into the CPU${NC}"
