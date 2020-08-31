#!/bin/bash
set -e

cd /app
echo "$GIT_CRYPT_KEY" > git-crypt-key.encoded
base64 -d git-crypt-key.encoded > git-crypt-key
git-crypt unlock git-crypt-key

source "/app/bin/activate"

python3 manage.py $@
