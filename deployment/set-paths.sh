#!/bin/bash
sed -i -e "s/ubuntu/$USER/g" deployment/spacy-pl-demo
sed -i -e "s/ubuntu/$USER/g" deployment/spacy-pl-demo.service
sed -i -e "s/User=$USER/User=$PID/g" deployment/spacy-pl-demo.service
