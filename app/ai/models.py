import torch
# from transformers import AutoModel, AutoTokenizer
from FlagEmbedding import BGEM3FlagModel

class SentenceEmbedder:
    def __init__(self, model_name: str = 'BAAI/bge-m3'):
        self.model = BGEM3FlagModel(model_name, use_fp16=True)

    def get_embedding(self, sentences: list[str]):
        output = self.model.encode(
            sentences, 
            batch_size=12, 
            max_length=8192
        )
        return output['dense_vecs']

    @staticmethod
    def cal_score(a, b):
        import numpy as np
        return np.dot(a, b) * 100