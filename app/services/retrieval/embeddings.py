import time
import logfire
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import settings

BATCH_SIZE =50
_GEMINI_DIM =3072
_FALLBACK_DIM =768    # all-mpnet-base-v2    (fallback model if gemini rate limit exceed)

_active_model = None
_model_type: str | None = None  # "gemini" or "fallback"

# model initialization------

def _probe_geminiai():
     """Try one embed call to verify Gemini is reachable. Returns model or None."""
     try:
        model=GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-2-preview",
            google_api_key=settings.GEMINI_API_KEY
        )
        # test a single cal to test reachability
        model.embed_query("test")
        logfire.info("gemini embeddings initialized", model="GeminiEmbeddings")
        return model
     except Exception as e:
        logfire.error("gemini embeddings initialization failed will use sentense fallback ", error=str(e))
        return None 

def load_fallback():
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-mpnet-base-v2")
    logfire.info("Fallback SentenceTransformer loaded", model="all-mpnet-base-v2")
    return model

def _init():
     """Initialise embedding model once per process. Called lazily on first use."""
     global _active_model, _model_type
     if _active_model is not None:
        return

     geminiai=_probe_geminiai()
     if geminiai:
        _active_model = geminiai
        _model_type = "gemini"
     else:
        _active_model=load_fallback()
        _model_type = "fallback"

     if _active_model is None:
        raise RuntimeError(
            "Failed to initialise any embedding model. "
            "Check your GEMINI_API_KEY and that sentence-transformers is installed."
        )

# public helpers-----------

def get_embedding_dim()-> int:
     """Return the vector dimension for the active model. Call after _init()."""
     _init()
     return _GEMINI_DIM if _model_type == "gemini" else _FALLBACK_DIM

# ── Batch embedding with retry---------

def _embed_batch(batch: list[str]) -> list[list[float]]:
    if _active_model is None:
        raise RuntimeError("Embedding model is not initialised. Call _init() first.")
    if _model_type == "gemini":
        # Exponential backoff: 1 s → 2 s → 4 s → 8 s (4 attempts total)
        for attempt in range(4):
            try:
                return _active_model.embed_documents(batch)
            except Exception as e:
                err = str(e).lower()
                is_rate_limit = any(x in err for x in ("429", "rate", "quota", "resource_exhausted"))
                if is_rate_limit and attempt < 3:
                    wait = 2 ** attempt
                    logfire.warning(
                        f"Gemini rate limit hit — retrying in {wait}s "
                        f"(attempt {attempt + 1}/4)."
                    )
                    time.sleep(wait)
                else:
                    logfire.error(f"Gemini embedding failed: {e}")
                    raise
        raise RuntimeError("Gemini rate limit persisted after 4 attempts.")
    else:
        return _active_model.encode(batch, show_progress_bar=False).tolist()


#public Api---------------

def embed_query(query:str) -> list[float]:
    _init()
    if _active_model is None:
        raise RuntimeError("Embedding model is not initialised — _init() did not load any model.")
    if _model_type == "gemini":
        return _active_model.embed_query(query)
    else:
        return _active_model.encode([query])[0].tolist()

def embed_text(text:list[str])->list[list[float]]:
    _init()
    all_embeddings:list[list[float]] =[]
    for i in range(0,len(text),BATCH_SIZE):
        batch = text[i:i + BATCH_SIZE]
        with logfire.span("Embed batch", model=_model_type, start=i, size=len(batch)):
            all_embeddings.extend(_embed_batch(batch))
    return all_embeddings
    


    
   
    

