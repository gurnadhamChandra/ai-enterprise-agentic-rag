Run data ingestion
Parses all documents in DATA/, chunks them, saves metadata to processed_data/, and indexes vectors into Qdrant.

first authenticate logfire by running this command:

uv run logfire auth

run this command to ingest true data:
python -m app.ingestion.processor DATA/true_data true

run this command to ingest noisy data:
python -m app.ingestion.processor DATA/noisy_data  noisy


run backend====
uvicorn app.main:app --reload --port 8000


run frontend===
streamlit run app/ui/app.py