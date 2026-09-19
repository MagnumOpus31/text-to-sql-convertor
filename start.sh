#!/bin/sh

uvicorn api.main:app --host 127.0.0.1 --port 8000 &

exec streamlit run app.py \
    --server.address=0.0.0.0 \
    --server.port="$PORT"