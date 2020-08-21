#!/bin/bash

if [ "$ENV" = "prod" ]
then
    cd /app
    echo "$GIT_CRYPT_KEY" > git-crypt-key
    git-crypt unlock git-crypt-key
