from sentence_transformers import SentenceTransformer, util
import fitz #PyMuPDF is labeled as fitz
import os

def extract_text_pdf(pdf_path): #extract the text from a .pdf
    full_text = "" #to store text
    try:
        with fitz.open(pdf_path) as doc: #open the pdf
            for page in doc:  # iterate over all pages and add the text
                full_text += page.get_text()
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
    return full_text

def extract_text_txt(txt_path): #extracts text from a .txt file
    try:
        with open(txt_path, 'r', encoding="utf-8") as doc: #open the pdf
            full_text = doc.read()
    except Exception as e:
        print(f"Error reading .txt file {txt_path}: {e}")
    return full_text

    

def load_text(file_path):
    file_extracts = {
        ".pdf" : extract_text_pdf,
        ".txt" : extract_text_txt
    }
    __, extension = os.splitext(file_path) # grab the file extension
    extension = extension.lower() # use lowercase for consistency
    if extension not in file_extracts.keys(): # check if file is not a pdf or txt
        raise ValueError(f"Unsupported file type: {extension}")
    extract = file_extracts[extension] # grab correct function for opening file
    text = extract(file_path) # collect text
    return text

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
    