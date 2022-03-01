#!/bin/bash

EMBEDDINGDIR="../graph_parser/embeddings"

python convert_to_bio.py
python convert_to_rels.py

# for DATASET in darmstadt_unis mpqa multibooked_ca multibooked_eu norec opener_es opener_en; do
for DATASET in norec; do
    if [ $DATASET == norec ]; then
        EXTERNAL=$EMBEDDINGDIR/58.zip
    elif [ $DATASET == multibooked_eu ]; then
        EXTERNAL=$EMBEDDINGDIR/32.zip
    elif [ $DATASET == multibooked_ca ]; then
        EXTERNAL=$EMBEDDINGDIR/34.zip
    elif [ $DATASET == mpqa ]; then
        EXTERNAL=$EMBEDDINGDIR/18.zip
    elif [ $DATASET == darmstadt_unis ]; then
        EXTERNAL=$EMBEDDINGDIR/18.zip
    elif [ $DATASET == opener_en ]; then
        EXTERNAL=$EMBEDDINGDIR/18.zip
    elif [ $DATASET == opener_es ]; then
        EXTERNAL=$EMBEDDINGDIR/68.zip
    else
        echo "NO EMBEDDINGS SUPPLIED FOR THIS DATASET"
        echo "EXITING TRAINING PROCEDURE"
        exit
    fi

    # Train extraction models
    for ANNOTATION in sources targets expressions; do
        python extraction_module.py -data "$DATASET" -emb "$EXTERNAL" -ann "$ANNOTATION"
    done;

    # Train relation prediction model
    python relation_prediction_module.py -data "$DATASET" -emb "$EXTERNAL"

done;
