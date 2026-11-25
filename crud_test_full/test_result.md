# THIS IS THE RESULT OF RUNNING @test_api.sh

=== 1. CREATE TICKET (POST /tickets) ===
{"message": "Tiket berhasil dibuat", "data": {"ticket_id": "A643F834", "event_name": "Paramore Jogja 2026", "buyer_name": "Rakan", "seat_category": "VIP", "status": "BOOKED", "created_at": "2026-11-25T16:01:44.949122+00:00"}}

Generated Ticket ID: A643F834

=== 2. READ TICKET (GET /tickets/A643F834) ===
{"data": {"ticket_id": "A643F834", "event_name": "Paramore Jogja 2026", "buyer_name": "Rakan", "seat_category": "VIP", "status": "BOOKED", "created_at": "2026-11-25T16:01:44.949122+00:00"}}

=== 3. UPDATE TICKET STATUS (PUT /tickets/A643F834) ===
{"message": "Status tiket diperbarui", "data": {"ticket_id": "A643F834", "event_name": "Paramore Jogja 2026", "buyer_name": "Rakan", "seat_category": "VIP", "status": "PAID", "created_at": "2026-11-25T16:01:44.949122+00:00"}}

=== 4. DELETE TICKET (DELETE /tickets/A643F834) ===
{"message": "Tiket A643F834 berhasil dihapus"}