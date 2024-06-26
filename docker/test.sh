#!/bin/sh
trap 'exit 1' ERR

# travis test script for django app
#
# PRECONDITION:
#   inherited env vars from application's .travis.yml MUST include:
#   DJANGO_APP: django application directory name

# start virtualenv
source bin/activate

# install test tooling
pip install pycodestyle coverage

function run_test {
    echo "##########################"
    echo "TEST: $1"
    eval $1
}

function catch {
    echo "Test failure occurred on line $LINENO"
    exit 1
}

run_test "pycodestyle ${DJANGO_APP}/ --exclude=resources"

run_test "python -Wd -m coverage run --source=${DJANGO_APP} '--omit=*/resources/*' manage.py test ${DJANGO_APP}"

# put generated coverage result where it will get processed
cp .coverage.* /coverage

exit 0
