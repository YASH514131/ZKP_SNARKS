#!/bin/bash
echo "Starting zk-SNARK Age Verification Server..."
python -m uvicorn zksnark_main:app --host 0.0.0.0 --port $PORT
