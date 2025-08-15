from sentence_transformers import SentenceTransformer, util

def chunk_text(text, chunk_size=300): # returns a list of strings
    words = text.split() #create a list of words
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i+chunk_size])) # grab our relevant chunk and join them with a space
    return chunks

def similar_chunks(user_topic, doc_chunks, topk=2):
    embd_model = SentenceTransformer("all-MiniLM-L6-v2")
    topic_embd = embd_model.encode(user_topic)
    doc_embd = embd_model.encode(doc_chunks)
    cos_scores = util.cos_sim(topic_embd, doc_embd)
    chunk_idx = cos_scores[0].topk(k=topk).indices
    top_chunks = [doc_chunks[i] for i in chunk_idx]
    return top_chunks
    