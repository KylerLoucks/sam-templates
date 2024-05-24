#!/bin/bash
set -e

for file in /dumpfiles/*; do
    case "$file" in
        *.tar.gz) echo "Restoring dump ${file} into MongoDB..."; mongorestore --archive=$file --gzip --writeConcern '{w:1}' --numInsertionWorkersPerCollection 5 ;;
    esac
done