#!/bin/bash
BASE_URL="https://xjtrmtjeflv4hmrksbf5uju6tq0ejoyv.lambda-url.us-east-1.on.aws"

CREATE_RES=$(curl -s -X POST "$BASE_URL/tickets" \
  -H "Content-Type: application/json" \
  -d '{"event_name": "Paramore Jogja 2024", "buyer_name": "Rakan", "seat_category": "VIP+"}')
echo "$CREATE_RES"

CREATE_RES=$(curl -s -X POST "$BASE_URL/tickets" \
  -H "Content-Type: application/json" \
  -d '{"event_name": "Muse Tangerang 2025", "buyer_name": "Hendian", "seat_category": "VIP"}')
echo "$CREATE_RES"

CREATE_RES=$(curl -s -X POST "$BASE_URL/tickets" \
  -H "Content-Type: application/json" \
  -d '{"event_name": "Hindia Jakarta 2026", "buyer_name": "Ramadhan", "seat_category": "Regular"}')
echo "$CREATE_RES"
