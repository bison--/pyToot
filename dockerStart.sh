#!/bin/bash

if [ -f conf_local.py ]; then
    docker run -it --rm -v $(pwd)/cache:/app/cache -v $(pwd)/conf_local.py:/app/conf_local.py pytoot
else
    docker run -it --rm -v $(pwd)/cache:/app/cache pytoot
fi
