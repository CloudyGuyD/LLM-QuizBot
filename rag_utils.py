


def chunk_text(text, chunk_size=300): # returns a list of strings
    words = text.split() #create a list of words
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i+chunk_size])) # grab our relevant chunk and join them with a space
    return chunks