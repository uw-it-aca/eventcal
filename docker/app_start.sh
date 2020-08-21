#!/bin/bash

if [ "$ENV" = "prod" ]
then
    cd /app
    git-crypt unlock
