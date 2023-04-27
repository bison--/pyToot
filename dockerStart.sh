#!/bin/bash

if [ -f conf_local.py ]; then
    docker run -it --rm -v $(pwd)/conf_local.py:/app/conf_local.py my-python-app
else
    docker run -it --rm my-python-app
fi
