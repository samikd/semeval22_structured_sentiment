#!/bin/bash

# Set up the conda environments
if { ! conda env list | grep 'ss'; } >/dev/null 2>&1; then
    conda env create -f conda-env-local.yml
fi

# Download the embeggings
EMBEDDING_DIR="./baselines/graph_parser/embeddings"
EMBEDDING_URL_BASE="http://vectors.nlpl.eu/repository/20/"

[ ! -d $EMBEDDING_DIR ] && mkdir $EMBEDDING_DIR

for DATASET in darmstadt_unis mpqa multibooked_ca multibooked_eu norec opener_es opener_en; do
    if [ $DATASET == norec ]; then
        EMBEDDING_FILE=$EMBEDDING_DIR/58.zip
        EMBEDDING_URL=$EMBEDDING_URL_BASE/58.zip
    elif [ $DATASET == multibooked_eu ]; then
        EMBEDDING_FILE=$EMBEDDING_DIR/32.zip
        EMBEDDING_URL=$EMBEDDING_URL_BASE/32.zip
    elif [ $DATASET == multibooked_ca ]; then
        EMBEDDING_FILE=$EMBEDDING_DIR/34.zip
        EMBEDDING_URL=$EMBEDDING_URL_BASE/34.zip
    elif [ $DATASET == mpqa ]; then
        EMBEDDING_FILE=$EMBEDDING_DIR/18.zip
        EMBEDDING_URL=$EMBEDDING_URL_BASE/18.zip
    elif [ $DATASET == darmstadt_unis ]; then
        EMBEDDING_FILE=$EMBEDDING_DIR/18.zip
        EMBEDDING_URL=$EMBEDDING_URL_BASE/18.zip
    elif [ $DATASET == opener_en ]; then
        EMBEDDING_FILE=$EMBEDDING_DIR/18.zip
        EMBEDDING_URL=$EMBEDDING_URL_BASE/18.zip
    elif [ $DATASET == opener_es ]; then
        EMBEDDING_FILE=$EMBEDDING_DIR/68.zip
        EMBEDDING_URL=$EMBEDDING_URL_BASE/68.zip
    fi
    [ ! -f $EMBEDDING_FILE ] && wget -O $EMBEDDING_FILE $EMBEDDING_URL

done;