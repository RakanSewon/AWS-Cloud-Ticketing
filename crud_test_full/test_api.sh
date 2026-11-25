#!/bin/bash
# Ganti dengan URL Fungsi Lambda milikmu (tanpa garis miring di akhir)
BASE_URL="https://xjtrmtjeflv4hmrksbf5uju6tq0ejoyv.lambda-url.us-east-1.on.aws"

echo "=== 1. CREATE TICKET (POST /tickets) ==="
CREATE_RES=$(curl -s -X POST "$BASE_URL/tickets" \
  -H "Content-Type: application/json" \
  -d '{"event_name": "Konser Musik Kampus 2026", "buyer_name": "Rakan", "seat_category": "VIP"}')
echo "$CREATE_RES"

# Ekstrak ticket_id dari respons JSON menggunakan Python
TICKET_ID=$(echo "$CREATE_RES" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['ticket_id'])")
echo -e "\nGenerated Ticket ID: $TICKET_ID\n"

echo "=== 2. READ TICKET (GET /tickets/$TICKET_ID) ==="
curl -s -X GET "$BASE_URL/tickets/$TICKET_ID"
echo -e "\n"

echo "=== 3. UPDATE TICKET STATUS (PUT /tickets/$TICKET_ID) ==="
curl -s -X PUT "$BASE_URL/tickets/$TICKET_ID" \
  -H "Content-Type: application/json" \
  -d '{"status": "PAID"}'
echo -e "\n"

# Jeda opsional jika ingin mengecek file JSON di konsol S3 sebelum dihapus
# read -p "Tekan Enter untuk melanjutkan ke pengujian DELETE..."

echo "=== 4. DELETE TICKET (DELETE /tickets/$TICKET_ID) ==="
curl -s -X DELETE "$BASE_URL/tickets/$TICKET_ID"
echo -e "\n"