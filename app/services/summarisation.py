from app.services.semantic import embed_texts
from app.utils.chunking import sentence_chunk
from app.utils.mmr import mmr_select_sentences
import numpy as np

def summarize_document(
    text: str,
    top_k: int = 5,
    lambda_param: float = 0.7
):
    """
    MMR-based extractive summarization
    """

    sentences = sentence_chunk(text)

    if len(sentences) <= top_k:
        return {
            "summary": sentences,
            "method": "direct"
        }

    doc_embedding = np.array(embed_texts(text))
    sentence_embeddings = [
        np.array(embed_texts(sentence))
        for sentence in sentences
    ]

    selected_sentences = mmr_select_sentences(
        doc_embedding=doc_embedding,
        sentence_embeddings=sentence_embeddings,
        sentences=sentences,
        top_k=top_k,
        lambda_param=lambda_param
    )

    summary_text = " ".join(selected_sentences)

    return {
        "summary": summary_text,
        "selected_sentences": selected_sentences,
        "method": "mmr",
        "top_k": top_k,
        "lambda_": lambda_param
    }

