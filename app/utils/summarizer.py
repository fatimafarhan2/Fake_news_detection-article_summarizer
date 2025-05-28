from transformers import pipeline

def split_chunks(text, max_chunk_len=2000):  # Reduced from 3000
    paragraphs = text.split('\n')
    chunks = []
    current = ""
    
    for para in paragraphs:
        if len(current) + len(para) <= max_chunk_len:
            current += para + '\n'
        else:
            chunks.append(current.strip())
            current = para + '\n'
    if current:
        chunks.append(current.strip())
    
    return [ch for ch in chunks if ch.strip()]

def safe_bart_summarize(summarizer, text, max_len, min_len):
    # wrapper to handle BART's index out of range error
    try:
        # First attempt with our normal parameters
        # we simply try to put the chink in model
        return summarizer(
            text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )[0]['summary_text']
    except (IndexError, RuntimeError) as e:
        # if the normal method doesnt work then we check for different error

        if "index out of range" in str(e).lower():
            #we change the min max en param
            try:
                conservative_max = min(50, max_len)
                conservative_min = min(10, conservative_max - 5)
                return summarizer(
                    text,
                    max_length=conservative_max,
                    min_length=conservative_min,
                    do_sample=False,
                    early_stopping=True
                )[0]['summary_text']
            except Exception:
                # incase of failure again we just take the 2-3 sentences from chunk and  join it
                sentences = text.split('.')[:3]
                return '. '.join(sentences) + '.'
        else:
            raise e

def text_summarizer(data: str) -> str:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    chunks = split_chunks(data, max_chunk_len=2000)[:3]  # Reduced chunk size
    result = []
    
    for i, ch in enumerate(chunks):
        try:
            ch = ch.strip()
            if not ch or len(ch.split()) < 20:  # Increased from 5 to 20
                result.append(f"[Skipped chunk {i+1}: Too short]")
                continue
            
            input_length = len(ch.split())
            max_len = max(30, min(130, int(0.3 * input_length)))  # More conservative
            min_len = max(10, min(max_len - 10, int(0.15 * input_length)))  # More conservative
            
            if min_len >= max_len:
                min_len = max(5, int(0.4 * max_len))
            
        #    instead of direct implementation we call teh wrapper
            summary = safe_bart_summarize(summarizer, ch, max_len, min_len)
            result.append(summary)
            
        except Exception as e:
            result.append(f"[Error in summarizing chunk {i+1}] : {str(e)}")
    
    return " ".join(result)