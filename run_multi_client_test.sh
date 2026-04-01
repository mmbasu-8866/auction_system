#!/bin/bash

# Multi-Client Auction Test Runner
# Starts server and runs multi-client test simultaneously

set -e

PORT=${1:-5000}
NUM_CLIENTS=${2:-3}
SERVER_URL="http://localhost:$PORT"

echo "🎯 Starting Auction Server on port $PORT..."
python3 web_server.py &
SERVER_PID=$!

# Wait for server to start
echo "Waiting for server to start..."
sleep 3

# Check if server is running
if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo "✗ Server failed to start"
    exit 1
fi

echo "✓ Server running (PID: $SERVER_PID)"
echo ""
echo "🎯 Starting multi-client test with $NUM_CLIENTS clients..."
python3 test_multi_client.py $NUM_CLIENTS $SERVER_URL

# Cleanup
echo ""
echo "Shutting down server..."
kill $SERVER_PID 2>/dev/null || true
wait $SERVER_PID 2>/dev/null || true

echo "✓ Test complete"
