Noisy data is anyother data which is not kubernetes.io related
remove 
1. HTML tags
2. Java script
3. css
4. other type of html tags
5. unnecessary data


and we have true data that contians real kubernetes.io related questions and answers. on this data we have to make our chatbot to answer kubernetes.io related queries.
we can use langchain as our framework for our RAG pipeline.


check uv is installed or not first uv --version
if not installed then install uv (https://docs.astral.sh/uv/getting-started/installation/)
uv pip install -r requirements.txt

activate venv

<!-- .env -->
groq.com - create api key

<!-- GROQ_API_KEY -->
<!-- GROQ_FALLBACK_API_KEY -->   this is fallback if groq api is down then create one more api with other account add api key here 

<!-- GEMINI_API_KEY --> gemini api key (https://aistudio.google.com/app/apikey)

<!-- QDRANT_API_KEY --> qdrant.ai - create api key

<!-- QDRANT_CLUSTER_END_POINT --> qdrant.ai - get cluster end point

search in google "Qdrant cloud" for cluster end point
