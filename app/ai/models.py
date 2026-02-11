import torch
# from transformers import AutoModel, AutoTokenizer
from FlagEmbedding import BGEM3FlagModel

class SentenceEmbedder:
    def __init__(self, model_name: str = 'BAAI/bge-m3'):
        self.model = BGEM3FlagModel(model_name, use_fp16=True)

    def get_embeddings(self, sentences: list[str]):
        output = self.model.encode(
            sentences, 
            batch_size=12, 
            max_length=8192
        )
        return output['dense_vecs']
    
    def get_embedding(self, sentence: str):
        output = self.model.encode(
            [sentence], 
            batch_size=1, 
            max_length=8192
        )
        return output['dense_vecs'][0]

    @staticmethod
    def cal_score(a, b):
        import numpy as np
        return np.dot(a, b) * 100