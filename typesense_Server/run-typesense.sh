#!/bin/bash

# Load parent directory .env
export $(grep -v '^#' ../.env | xargs)

# Run Typesense using env variables
./typesense-server \
  --data-dir $TYPESENSE_DATA_DIR \
  --api-key $TYPESENSE_API_KEY \
  --listen-address $TYPESENSE_HOST \
  --listen-port $TYPESENSE_PORT \
  --enable-cors
