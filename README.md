# Serverless E-Ticketing REST API (AWS Track C)

Proyek ini merupakan implementasi infrastruktur komputasi awan berbasis arsitektur **Serverless (Track C)** untuk layanan manajemen tiket acara (*E-Ticketing*). Sistem menyediakan operasi CRUD (*Create, Read, Update, Delete*) melalui endpoint HTTPS publik menggunakan **AWS Lambda Function URL** dan **Amazon S3** sebagai penyimpanan dokumen JSON.

<img width="750" height="362" alt="aws drawio" src="https://github.com/user-attachments/assets/16b70593-b155-40f4-9563-100ed61d1186" />

---

## Arsitektur Sistem

Sistem dibangun sepenuhnya di atas layanan *managed serverless* pada region **`us-east-1` (N. Virginia)** di lingkungan **AWS Academy Learner Lab**:

* **Ingress & Compute:** **AWS Lambda (`TicketHandlerFunction` - Python 3.12)** yang mengekspos antarmuka HTTP langsung melalui **Lambda Function URL** (`Auth Type: NONE`, CORS aktif).
* **Storage Layer:** **Amazon S3 (`e-ticketing-json-storage-...`)** yang menyimulasikan pola penyimpanan *key-value* dengan menyimpan setiap entitas tiket sebagai objek JSON terpisah pada jalur `tickets/{ticket_id}.json`.
* **Security & IAM:** Menggunakan IAM Role bawaan **`LabRole`** pada fungsi Lambda untuk mengakses S3 dan CloudWatch. Bucket S3 dikonfigurasi dengan *Block All Public Access* aktif dan enkripsi bawaan *SSE-S3*.
* **Networking & Observability:** Berjalan pada jaringan terkelola AWS (*AWS Managed Network / Non-VPC*) tanpa memerlukan NAT Gateway atau Security Group kustom, serta terintegrasi otomatis dengan **Amazon CloudWatch Logs**.

> **Catatan Adaptasi Arsitektur:** Komponen Lambda Function URL dan Amazon S3 dipilih sebagai substitusi langsung untuk API Gateway dan DynamoDB karena pembatasan izin IAM pada *sandbox* AWS Academy Learner Lab (`apigateway:POST` dan `dynamodb:CreateTable` tidak diizinkan), dengan tetap mempertahankan prinsip desain *stateless serverless* dan *pay-per-use*.

---

Untuk saat ini, proyek sedang tahap awal dengan tujuan utama untuk mengimplementasikan konsep fundamental dalam membangun aplikasi serverless. Rencana pengembangan kedepannya berupa frontend sederhana, sistem rebutan (queue), serta status ketersediaan.
