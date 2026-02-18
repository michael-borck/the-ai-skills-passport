#!/bin/bash
# Quick test script for the progress tracker

BASE_URL="${1:-http://localhost:5050}"
TEST_UID="test-user-$$"

echo "Testing AI Skills Passport Progress Tracker"
echo "Base URL: $BASE_URL"
echo "Test UID: $TEST_UID"
echo "=========================================="

echo -e "\n1. Health check..."
curl -s "$BASE_URL/health" | python3 -m json.tool

echo -e "\n2. Check initial progress (should be empty)..."
curl -s "$BASE_URL/progress/$TEST_UID" | python3 -m json.tool

echo -e "\n3. Complete first experience..."
curl -s -X POST "$BASE_URL/complete" \
  -H "Content-Type: application/json" \
  -d "{\"uid\": \"$TEST_UID\", \"experience\": \"is-this-ai\"}" | python3 -m json.tool

echo -e "\n4. Check progress (should have 1 completion, Explorer badge)..."
curl -s "$BASE_URL/progress/$TEST_UID" | python3 -m json.tool

echo -e "\n5. Complete two more experiences..."
curl -s -X POST "$BASE_URL/complete" \
  -H "Content-Type: application/json" \
  -d "{\"uid\": \"$TEST_UID\", \"experience\": \"what-would-you-do\"}" > /dev/null

curl -s -X POST "$BASE_URL/complete" \
  -H "Content-Type: application/json" \
  -d "{\"uid\": \"$TEST_UID\", \"experience\": \"rules-of-engagement\"}" > /dev/null

echo -e "\n6. Check progress (should have 3 completions, Thinker badge)..."
curl -s "$BASE_URL/progress/$TEST_UID" | python3 -m json.tool

echo -e "\n7. Test duplicate completion (should update, not fail)..."
curl -s -X POST "$BASE_URL/complete" \
  -H "Content-Type: application/json" \
  -d "{\"uid\": \"$TEST_UID\", \"experience\": \"is-this-ai\"}" | python3 -m json.tool

echo -e "\n8. Test invalid experience..."
curl -s -X POST "$BASE_URL/complete" \
  -H "Content-Type: application/json" \
  -d "{\"uid\": \"$TEST_UID\", \"experience\": \"invalid-exp\"}" | python3 -m json.tool

echo -e "\n=========================================="
echo "Tests complete!"
