#!/bin/bash

if [[ ( $@ == "--help") ||  $@ == "-h" ]]; then
    echo "$0 <optional: --no-cache>"
    exit 1
fi

if [ $# -eq 1 ]; then
    NO_CACHE=$1
fi

date_var=$(date +%Y.%m.%d.%H.%M%S)
BUILD_TAG=dbcawa/bfrs:v$date_var
docker image build $NO_CACHE --tag $BUILD_TAG . &&
echo $BUILD_TAG &&
docker push $BUILD_TAG
