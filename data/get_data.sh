#!/bin/bash

mkdir butterfly
cd butterfly
wget -O data.zip "https://bynder-media-eu-central-1.s3.eu-central-1.amazonaws.com/transfer/BA7D4B2F-1733-4C4D-BCB238380F47F465/9e78d983-556a-4483-ab87-14ffd5f14068/4a6bb222-f0fd-41d0-8cd8-e0c7bcbe1e6d?response-content-disposition=attachment%3B%20filename%3D%22COVID%20Clinical%20Gallery%20Butterfly%20Network.zip%22%3B%20filename%2A%3DUTF-8%27%27COVID%2520Clinical%2520Gallery%2520Butterfly%2520Network.zip&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAI23JIVF2HGLUN4NA%2F20200424%2Feu-central-1%2Fs3%2Faws4_request&X-Amz-Date=20200424T083758Z&X-Amz-Expires=900&X-Amz-SignedHeaders=host&X-Amz-Signature=fbdab38cb6b694013b2e74207430a19327348a6543ee00adc618cafef86703b6"
unzip data.zip
rm data.zip
cd ..

# activate environment
python process_data.py