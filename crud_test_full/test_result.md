# THIS IS THE RESULT OF RUNNING @test_api.sh

=== 1. CREATE TICKET (POST /tickets) ===
{"message": "Tiket berhasil dibuat", "data": {"ticket_id": "58825449", "event_name": "Konser Musik Kampus 2026", "buyer_name": "Rakan", "seat_category": "VIP", "status": "BOOKED", "created_at": "2026-11-25T15:15:02.574356+00:00"}}

Generated Ticket ID: 58825449

=== 2. READ TICKET (GET /tickets/58825449) ===
{"data": {"ticket_id": "58825449", "event_name": "Konser Musik Kampus 2026", "buyer_name": "Rakan", "seat_category": "VIP", "status": "BOOKED", "created_at": "2026-11-25T15:15:02.574356+00:00"}}

=== 3. UPDATE TICKET STATUS (PUT /tickets/58825449) ===
{"message": "Status tiket diperbarui", "data": {"ticket_id": "58825449", "event_name": "Konser Musik Kampus 2026", "buyer_name": "Rakan", "seat_category": "VIP", "status": "PAID", "created_at": "2026-11-25T15:15:02.574356+00:00"}}

=== 4. DELETE TICKET (DELETE /tickets/58825449) ===
{"message": "Tiket 58825449 berhasil dihapus"}