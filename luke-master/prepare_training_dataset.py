import json
import os
data_path = './semeval_bio_data/extraction/darmstadt_unis'
write_path = './data'
if not os.path.exists(write_path):
    os.mkdir(write_path)
files_to_process = ['train', 'dev', 'test']

for input_data in files_to_process:
    with open(data_path+'/'+input_data+'.json') as f:
        lines = f.readlines()
        last = lines[-1]
        f_input_modified = open(input_data+'_modified'+'.json','w')
        f_input_modified.write('[')
        for line in lines:
            if line is last:
                f_input_modified.write(line.replace('-Positive', '').replace('-Negative','').replace('-Neutral',''))
                f_input_modified.write(']')
            else:
                f_input_modified.write(line.replace('-Positive', '').replace('-Negative','').replace('-Neutral','')+',')
                # work on other lines
        f_input_modified.close()

    input_data_file = open(input_data+'_modified'+'.json')

    # returns JSON object as
    # a dictionary
    train_data = json.load(input_data_file,strict=False)

    # -DOCSTART- -X- -X- O
    #
    # SOCCER NN B-NP O
    # - : O O
    # JAPAN NNP B-NP B-LOC
    # GET VB B-VP O
    if input_data == 'train':
        f1 = open(write_path+'/'+'eng.train','w')
    if input_data == 'dev': 
        f1 = open(write_path+'/'+'eng.testa','w') 

    if input_data == 'test': 
        f1 = open(write_path+'/'+'eng.testb','w') 


    labels_list = []
    for element in train_data:
        text = element['text']
        f1.write('-DOCSTART- -X- -X- O')
        f1.write('\n')
        f1.write('\n')
        for word_index in range(len(text)):
            word = text[word_index]
            src = element['sources'][word_index]
            target = element['targets'][word_index]
            exp = element['expressions'][word_index]
            label = max([src, target, exp], key=len)
            if label not in labels_list:
                labels_list.append(label)
            #print('label', label)
            f1.write(word +' '+' '+' '+' '+' '+label)
            f1.write('\n')
        f1.write('\n')
    f1.close()
print('All files are saved in Data folder')





