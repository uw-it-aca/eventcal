#!/bin/bash
set -e

if [ ! -e git-crypt-key ]; then
  echo "$GIT_CRYPT_KEY" > git-crypt-key.encoded
  base64 -d git-crypt-key.encoded > /app/git-crypt-key
  git-crypt unlock /app/git-crypt-key
fi
source "/app/bin/activate"

python3 manage.py $@
