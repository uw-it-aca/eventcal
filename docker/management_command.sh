#!/bin/bash
set -e

cd /app
echo "$GIT_CRYPT_KEY" | base64 -d > git-crypt-key
git-crypt unlock git-crypt-key

source "/app/bin/activate"

python3 manage.py $@
