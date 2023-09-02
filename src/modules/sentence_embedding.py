from queue import PriorityQueue

import nltk
import sentence_transformers
import torch
from sentence_transformers import SentenceTransformer

nltk.download('punkt')

class SentenceEmbedding:
    def __init__(self, model: str, device: str):
        self.device = torch.device(device)
        self.embedding_model = SentenceTransformer(model).to(self.device)
        
    def get_embedding(self, text_data: list, is_query: bool = False) -> torch.Tensor:
        embedding = [] 
        if is_query:
            sentences = text_data
        else:
            sentences = self.sentence_tokenize(text_data)
            sentences = [i for i in sentences if not i.isdigit()]
        
        for sent in sentences:
            embedding.append(self.embedding_model.encode(sent,  convert_to_tensor = True))

        return embedding, sentences
    
    def sentence_tokenize(self, text_data):
        sentences = []
        for p in range(len(text_data)):
            sentences += nltk.sent_tokenize(text_data[p])
        return sentences
        
        
def get_most_similarity(query: str, embedding_model: SentenceEmbedding, embedding_data: list):
    query_embedding = embedding_model.get_embedding([query])[0]

    answer_pq = PriorityQueue()
    for index, embed in enumerate(embedding_data):
        sim = sentence_transformers.util.semantic_search(query_embedding,embed,top_k=1)[0]
        answer_pq.put((-sim[0]['score'], index, sim[0]['corpus_id']))

    r = [] 
    for _ in range(min(4, answer_pq.qsize())):
        r.append(answer_pq.get())

    return r


if __name__ == "__main__":
    model = SentenceEmbedding('paraphrase-MiniLM-L3-v2', "cuda")
    
    data = ['A idempotent if and only if the corresponding ',
    'We point out that one should interpret a solution to (3) in the projectiv sense.',
    'which is naturally identified with a corresponding element',
    'It is convenient to consider the projectivization of the latter system. Namely']
    data1 = ["is homogeneous of degree 2.By the made assumption on Kwe can conside both (2 and (3) as equations over the compl numbers.Furthermore,3) defines a variety in CPn.Clearly,if x solves 2) then X=(1,) is a solution of 3),and conversely, X = (xo,x) solves (3) with xo  0 then r.x is a solution of (2). In the exceptional case o=0,one has =0i.e.e is a 2-nilpotent in A. In summary,there exists a natural bijection (depending on a choice of a basis in A between the set PAc and all solutions of 3) in CPn.In this picture,2 nilpotents correspond to the infinite' part of solutions of (2) (i.e. solutions of (3 witho=0. Then the classical Bezout's theorem implies the following dichotomy: either there are infinitely many solutions of (3) or the number of distinct solutions is less or equal to 2n,where n = dimK A. Therefore if the set P(Ac) is finite then necessarily"]
    d = [model.sentence_tokenize(data), model.sentence_tokenize(data1)]
    e = []
    e.append(model.get_embedding(data))
    e.append(model.get_embedding(data1))
    res = get_most_similarity("projectivization", model, e)
    print(res)
    for i in res:
        print(i)
        print("Score : ", -i[0])
        # print("Revelent document : ", i[1])
        print("Revelent sentence : ", d[i[1]][i[2]-1])
        