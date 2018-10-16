#!/usr/bin/env bash

#workon demo
python response_extract.py
python item_content.py
python description2file.py
python embedded2plot.py
python gen_nations_data.py

echo "exit pipeline"
