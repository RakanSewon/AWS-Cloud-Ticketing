# AWS-Cloud-Ticketing

### 1. Alur Permintaan & Data (*Request & Data Flow*)

1. **Client Layer (Postman / cURL):** Mengirimkan permintaan HTTP (`POST`, `GET`, `PUT`, `DELETE`) dalam format JSON melalui protokol HTTPS menuju *Invoke URL* publik milik API Gateway.
2. **Ingress Layer (Amazon API Gateway — HTTP API):**
* Menerima permintaan masuk dan mencocokkan metode HTTP serta jalur URL (`/tickets` atau `/tickets/{ticket_id}`).
* Melakukan integrasi *proxy* (*Lambda Proxy Integration*), yaitu meneruskan seluruh *payload* permintaan (`headers`, `pathParameters`, `body`) secara langsung ke fungsi Lambda.


3. **Compute Layer (AWS Lambda — `TicketHandlerFunction`):**
* Menerima objek *event* dari API Gateway.
* Mengekstrak rute dan metode HTTP untuk menentukan operasi CRUD yang diminta.
* Menjalankan validasi input dasar, membuat ID unik (`uuid4`) serta *timestamp* (untuk operasi `POST`), lalu memanggil AWS SDK (`boto3` untuk Python atau `@aws-sdk/client-dynamodb` untuk Node.js).
* Mengembalikan respons HTTP standar (kode status `200`, `201`, `400`, `404`, atau `500`) beserta *body* JSON kembali ke API Gateway.


4. **Storage Layer (Amazon DynamoDB — `TicketsTable`):**
* Mengeksekusi operasi baca/tulis berbasis *key-value* dengan latensi satu digit milidetik.
* **Skema Tabel:**
* *Table Name:* `TicketsTable`
* *Partition Key (PK):* `ticket_id` (`String`)
* *Sort Key:* Tidak digunakan (cukup PK tunggal untuk mempercepat pencarian langsung berdasarkan ID tiket).
* *Capacity Mode:* `On-Demand` (menyesuaikan kapasitas baca/tulis secara otomatis tanpa perlu *provisioning* RCU/WCU manual).




5. **Observability Layer (Amazon CloudWatch Logs):**
* Setiap eksekusi fungsi Lambda otomatis mengirimkan log standar (*stdout/stderr*, durasi eksekusi, dan *error traceback*) ke *Log Group* `/aws/lambda/TicketHandlerFunction`.



---

### 2. Arsitektur Keamanan & IAM (*Security & Identity*)

Untuk memenuhi kriteria diagram *"Label planned components, data flow, IAM/security"*, sertakan elemen keamanan berikut:

* **Enkripsi Transit:** Komunikasi antara Klien $\rightarrow$ API Gateway $\rightarrow$ Lambda $\rightarrow$ DynamoDB seluruhnya terenkripsi menggunakan **TLS/HTTPS**.
* **Resource-Based Policy (API Gateway $\rightarrow$ Lambda):**
* API Gateway diberi izin eksplisit melalui kebijakan berbasis sumber daya untuk memicu fungsi Lambda (`lambda:InvokeFunction`) khusus dari ARN API Gateway terkait.


* **Execution Role / Identity-Based Policy (Lambda $\rightarrow$ DynamoDB & CloudWatch):**
* Menggunakan IAM Role bawaan AWS Academy Learner Lab bernama **`LabRole`**.
* Pada panah koneksi dari **Lambda ke DynamoDB**, beri label izin spesifik (*least-privilege scope* secara konseptual): `dynamodb:PutItem`, `dynamodb:GetItem`, `dynamodb:UpdateItem`, `dynamodb:DeleteItem`.
* Pada panah koneksi dari **Lambda ke CloudWatch**, beri label izin: `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`.



---

### 3. Arsitektur Jaringan (*Network Architecture*)

* **AWS Managed Network (Non-VPC Lambda):** Fungsi Lambda berjalan di dalam jaringan terkelola milik AWS (*AWS-managed VPC*), bukan di dalam VPC kustom pengguna.
* **Keuntungan Desain:** Lambda memiliki akses keluar langsung ke *endpoint* publik internal layanan AWS (DynamoDB dan CloudWatch) melalui *backbone* jaringan AWS yang aman. Kamu tidak perlu membuat *Private Subnet*, *NAT Gateway*, maupun *VPC Endpoint* yang berpotensi menguras kredit AWS Learner Lab.

---

### 4. Panduan Menggambar Diagram (Draw.io / Lucidchart / Excalidraw)

Susun komponen dari kiri ke kanan dengan pengelompokan (*boundary box*) berikut agar mudah dibaca dosen/asisten:

1. **Di luar kotak AWS Cloud (Kiri):**
* Ikon **Client / User (Postman / cURL)** $\xrightarrow{\text{HTTPS / JSON}}$


2. **Di dalam kotak utama `AWS Cloud (Region: us-east-1)`:**
* **Amazon API Gateway** (beri label rute: `POST /tickets`, `GET /tickets/{id}`, `PUT /tickets/{id}`, `DELETE /tickets/{id}`)
* Panah dari API Gateway ke Lambda dengan label: `InvokeFunction (Resource Policy)`
* **AWS Lambda (`TicketHandlerFunction`)** yang ditempeli ikon badge **IAM Role (`LabRole`)**
* Panah dari Lambda ke bawah menuju **Amazon CloudWatch Logs** dengan label: `PutLogEvents`
* Panah dari Lambda ke kanan menuju **Amazon DynamoDB (`TicketsTable`)** dengan label: `PutItem, GetItem, UpdateItem, DeleteItem (HTTPS)`
