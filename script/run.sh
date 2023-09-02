#!/bin/bash

# turn on bash's job control
set -m

# Start the primary process and put it in the background
uvicorn src.app:app --host 0.0.0.0 --port 5000 &

# Start the helper process
streamlit run streamlit_app.py

# the my_helper_process might need to know how to wait on the
# primary process to start before it does its work and returns
wait -n

# now we bring the primary process back into the foreground
# and leave it there
fg %1