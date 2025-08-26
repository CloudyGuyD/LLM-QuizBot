from sentence_transformers import SentenceTransformer, util
from torch.cuda import is_available

def chunk_text(text, chunk_size): # returns a list of strings
    words = text.split() #create a list of words
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i+chunk_size])) # grab our relevant chunk and join them with a space
    return chunks

def similar_chunks(user_topic, doc_chunks, topk):
    # load the "all-MiniLM-L6-v2" sentence transformer model to embed our text
    device = 'cuda' if is_available() else 'cpu'
    embd_model = SentenceTransformer("all-MiniLM-L6-v2", device)
    #encode our topic and document separately
    topic_embd = embd_model.encode(user_topic) # (1, embd_dim)
    doc_embd = embd_model.encode(doc_chunks) #gives a list of embeddings from the chunk_text function (num_chunks, embd_dim)
    #find the cosine similarity scores for each chunk and topic combination
    cos_scores = util.cos_sim(topic_embd, doc_embd) # (1, num_chunks)
    chunk_idx = cos_scores[0].topk(k=topk).indices # grab the indices of the k most similar text chunks
    top_chunks = [doc_chunks[i] for i in chunk_idx] # return a list of the most similar text chunks
    return top_chunks

def rag_text_to_chunks(text, user_topic, chunk_size=300, topk=6):
    # text = load_text(file_path) not needed when using streamlit's file object, it allows us to directly read the file
    text_chunks = chunk_text(text, chunk_size)
    similar = similar_chunks(user_topic, text_chunks, topk)
    return similar
    