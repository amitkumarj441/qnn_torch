# -*- coding: utf-8 -*-

import os
from dataset.classification.data_reader import CRDataReader, MRDataReader, SUBJDataReader, MPQADataReader, SSTDataReader, TRECDataReader

def setup(opt):
    dir_path = os.path.join(opt.datasets_dir, opt.dataset_name)
    if opt.dataset_name == 'CR':
        reader = CRDataReader(dir_path, opt)
    if opt.dataset_name == 'MR':
        reader = MRDataReader(dir_path, opt)
    if opt.dataset_name == 'SUBJ':
        reader = SUBJDataReader(dir_path, opt)
    if opt.dataset_name == 'MPQA':
        reader = MPQADataReader(dir_path, opt)
    if opt.dataset_name == 'SST_2':
        dir_path = os.path.join(opt.datasets_dir, 'SST')
        reader = SSTDataReader(dir_path, opt, nclasses = 2)
    if opt.dataset_name == 'SST_5':
        dir_path = os.path.join(opt.datasets_dir, 'SST')
        reader = SSTDataReader(dir_path, opt, nclasses = 5)
    if opt.dataset_name == 'TREC':
        reader = TRECDataReader(dir_path, opt)
    return reader

if __name__ == '__main__':
    pass
   
#def get_sentiment_dic_training_data(reader, opt):
#    word2id = reader.embedding_params['word2id']
#    file_name = opt.sentiment_dic_file
#    pretrain_x = []
#    pretrain_y = []
#    with codecs.open(file_name, 'r') as f:
#        for line in f:
#            word, polarity = line.split()
#            if word in word2id:
#                word_id = word2id[word]
#                pretrain_x.append([word_id]* reader.max_sentence_length)
#                pretrain_y.append(int(float(polarity)))
#    
#    pretrain_x = np.asarray(pretrain_x)
#    pretrain_y = to_categorical(pretrain_y)
#    return pretrain_x, pretrain_y
#   