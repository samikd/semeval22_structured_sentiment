#  Structured Sentiment Analysis -SpanPrediction
This contains the instruction of fine tuning LUKE for span prediction task
# Experiment Pipelines

First, install the required packages

```sh
cd luke-master; pip install -r requirements.txt
```
Then download the LUKE pre-trained model form this link https://drive.google.com/file/d/1S7smSBELcZWV7-slfrb94BKcSCCoxGfL/view


### Data Preparation Stage
#### Step1: 
**NOTE**: 
For the dataset `darmstadt_unis` and `mpqa` we don't have train, test and dev files. Please follow the `darmstadt_unis/README.md` to generate those files. 
```bash
python convert_data_to_bio.py
```
`convert_data_to_bio.py` has been modified to run only on `darmstadt_unis`.

The output of the above script will be saved in ``semeval_bio_data`` folder
#### Step2: 
Run the following script. This only takes ```darmstadt_univs``` data, for other dataset change ```data_path``` in th code. 
```bash
python prepare_training_dataset.py
```
### Fine Tuning Stage

Run the foloowing in order to fine-tune the model

```bash
$ python -m examples.cli\
    --model-file=luke_large_500k.tar.gz \
    --output-dir=<OUTPUT_DIR> \
    ner run \
    --data-dir=<DATA_DIR> \
    --train-batch-size=2 \
    --gradient-accumulation-steps=4 \
    --learning-rate=1e-5 \
    --num-train-epochs=5 
```
The above script will take time to run. The fine tuned model will be saved into ```OUTPUT_DIR```
### Eval Stage
The following will produce predicted json file for dev.json using fine tuned checkpoint file.
```bash
 python -m examples.cli \
    --model-file=luke_large_500k.tar.gz \
    --output-dir=<OUTPUT_DIR> \
    ner run \
    --data-dir=<DATA_DIR> \
    --checkpoint-file=<OUTPUT_DIR>/pytorch_model.bin \
    --no-train
```
The produced predicted json file saved in ```OUTPUT_DIR``` will be further used by LUKE span prediction model as a next step of the pipeline.
