## Local Setup
pip install -r requirements.txt \
uvicorn main:app --reload

## Endpoints
GET /health → {"status": "ok"}
POST /sort-ticket → see schema in task doc

## Deploy (Render)
- Connect GitHub repo
- Build command: pip install -r requirements.txt
- Start command: uvicorn main:app --host 0.0.0.0 --port $PORT
