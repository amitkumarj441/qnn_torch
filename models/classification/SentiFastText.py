# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
import torch.nn.functional as F

class SentiFastText(nn.Module): 
    def __init__(self, opt): 
        super(SentiFastText, self).__init__() 
        self.opt = opt
        sentiment_lexicon = opt.sentiment_dic
        if sentiment_lexicon is not None:
            self.sentiment_lexicon = torch.tensor(sentiment_lexicon, dtype=torch.float).to(opt.device)
        embedding_matrix = torch.tensor(opt.lookup_table, dtype=torch.float)
        self.embed = nn.Embedding(embedding_matrix.shape[0], embedding_matrix.shape[1])
        self.linear = nn.Linear(50, 200)
        self.bn = nn.BatchNorm1d(200)
        self.fc = nn.Linear(200, 2)
        self.senti_fc = nn.Linear(50, 1)

    def forward(self, inp):
        text_indices = inp
        embed = self.embed(text_indices) 
        x = torch.mean(embed, dim=1)
        x = self.linear(x)
        x = self.bn(x)  
        output = self.fc(x)

        if self.training:
            senti_out = torch.sigmoid(self.senti_fc(embed).flatten(0, 1))
            indices = text_indices.flatten(-2, -1)
            senti_tag = (self.sentiment_lexicon.index_select(0, indices) + 1) / 2
            senti_loss = -torch.sum(senti_tag*torch.log(senti_out)+(1-senti_tag)*torch.log(1-senti_out)) / len(senti_out)
            return senti_loss, output
        else:
            senti_out = torch.sign(self.senti_fc(embed).flatten(0, 1))
            indices = text_indices.flatten(-2, -1)
            senti_tag = self.sentiment_lexicon.index_select(0, indices)
            senti_acc = torch.sum(senti_out == senti_tag).float() / len(senti_out)
            return senti_acc, output