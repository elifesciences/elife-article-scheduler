#!/bin/bash
set -e
export DJANGO_SETTINGS_MODULE=core.settings
pylint -E ./src/schedule/** --load-plugins=pylint_django --disable=E1103
echo "* passed linting"
