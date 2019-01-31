# -*- coding: utf-8 -*-
import torch
import torch.nn.functional as F
import torch.nn
from .measurement import ComplexMeasurement

class ComplexProjMeasurement(torch.nn.Module):
    def __init__(self, opt, embed_dim, method='sample', device = torch.device('cpu')):
        super(ComplexProjMeasurement, self).__init__()
        self.opt = opt
        self.embed_dim = embed_dim
        self.method = method
        self.measurement = ComplexMeasurement(embed_dim, units=embed_dim, ortho_init=True, device = device)

    def forward(self, inputs):

        if not isinstance(inputs, list):
            raise ValueError('This layer should be called '
                             'on a list of 2 inputs.')

        if len(inputs) != 2:
            raise ValueError('This layer should be called '
                            'on a list of 2 inputs.'
                            'Got ' + str(len(inputs)) + ' inputs.')
    
        input_real = inputs[0] 
        input_imag = inputs[1]

        seq_len = input_real.shape[1]
        chunks_real = torch.chunk(input_real, seq_len, dim=1)
        chunks_imag = torch.chunk(input_imag, seq_len, dim=1)
        real_samples = []
        imag_samples = []
        for i in range(seq_len):
            output = self.measurement([chunks_real[i].squeeze(1), chunks_imag[i].squeeze(1)]).clamp(min=1e-5)
            if self.method == 'sample':
                sampled_indice = output.multinomial(1).squeeze(1)
                real_sample = torch.index_select(self.measurement.kernel[:,:,0], 0, sampled_indice).unsqueeze(1)
                imag_sample = torch.index_select(self.measurement.kernel[:,:,1], 0, sampled_indice).unsqueeze(1)

            elif self.method == 'ensemble':
                real_sample = torch.mm(output, self.measurement.kernel[:,:,0]).unsqueeze(1)
                imag_sample = torch.mm(output, self.measurement.kernel[:,:,1]).unsqueeze(1)
            real_samples.append(real_sample)
            imag_samples.append(imag_sample)
        real_samples = torch.cat(real_samples, dim=1)
        imag_samples = torch.cat(imag_samples, dim=1)
        return [real_samples, imag_samples]
    
if __name__ == '__main__':
    pass
    
    
    
