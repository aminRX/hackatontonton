#!/bin/bash

echo "Starting collector service in background..."
lein run 8080 &
SERVER_PID=$!

# Wait for service to start
sleep 3

echo "Testing health endpoint..."
curl -s http://localhost:8080/health | jq .

echo -e "\nTesting POST /decisions..."
CUSTOMER_ID=$(uuidgen | tr '[:upper:]' '[:lower:]')
RESPONSE=$(curl -s -X POST http://localhost:8080/decisions \
  -H "Content-Type: application/json" \
  -d "{
    \"customer-id\": \"$CUSTOMER_ID\",
    \"decision-type\": \"application\",
    \"data-decision\": {
      \"score\": 85,
      \"approved\": true,
      \"reason\": \"Good credit score\"
    }
  }")
echo $RESPONSE | jq .

echo -e "\nTesting GET /decisions/$CUSTOMER_ID..."
curl -s http://localhost:8080/decisions/$CUSTOMER_ID | jq .

echo -e "\nTesting GET /decisions..."
curl -s http://localhost:8080/decisions | jq .

echo -e "\nStopping service..."
kill $SERVER_PID
wait $SERVER_PID 2>/dev/null

echo "Done!"

