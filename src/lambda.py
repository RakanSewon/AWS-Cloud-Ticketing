import json
import uuid
from datetime import datetime, timezone
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
BUCKET_NAME = 'e-ticketing-json-storage-rakan2026' 

def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body)
    }

def lambda_handler(event, context):
    # Mengambil HTTP method dari format event Function URL
    http_method = event.get('requestContext', {}).get('http', {}).get('method')
    
    # Parsing path manual: contoh "/tickets" atau "/tickets/A1B2C3D4"
    raw_path = event.get('rawPath', '').strip('/')
    path_parts = raw_path.split('/') if raw_path else []
    
    resource = path_parts[0] if len(path_parts) >= 1 else ''
    ticket_id = path_parts[1] if len(path_parts) >= 2 else None

    if resource != 'tickets':
        return response(404, {'error': 'Endpoint tidak ditemukan. Gunakan jalur /tickets'})

    try:
        # 1. CREATE (POST /tickets)
        if http_method == 'POST' and not ticket_id:
            body = json.loads(event.get('body') or '{}')
            if not body.get('event_name') or not body.get('buyer_name'):
                return response(400, {'error': 'event_name dan buyer_name wajib diisi'})

            new_id = str(uuid.uuid4())[:8].upper()
            new_ticket = {
                'ticket_id': new_id,
                'event_name': body['event_name'],
                'buyer_name': body['buyer_name'],
                'seat_category': body.get('seat_category', 'Regular'),
                'status': 'BOOKED',
                'created_at': datetime.now(timezone.utc).isoformat()
            }
            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=f'tickets/{new_id}.json',
                Body=json.dumps(new_ticket, indent=2),
                ContentType='application/json'
            )
            return response(201, {'message': 'Tiket berhasil dibuat', 'data': new_ticket})

        # 2. READ (GET /tickets/{ticket_id})
        elif http_method == 'GET' and ticket_id:
            obj = s3.get_object(Bucket=BUCKET_NAME, Key=f'tickets/{ticket_id}.json')
            ticket_data = json.loads(obj['Body'].read().decode('utf-8'))
            return response(200, {'data': ticket_data})

        # 3. UPDATE (PUT /tickets/{ticket_id})
        elif http_method == 'PUT' and ticket_id:
            body = json.loads(event.get('body') or '{}')
            new_status = body.get('status')
            if not new_status:
                return response(400, {'error': 'Field status wajib diisi untuk update'})

            obj = s3.get_object(Bucket=BUCKET_NAME, Key=f'tickets/{ticket_id}.json')
            ticket_data = json.loads(obj['Body'].read().decode('utf-8'))
            ticket_data['status'] = new_status

            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=f'tickets/{ticket_id}.json',
                Body=json.dumps(ticket_data, indent=2),
                ContentType='application/json'
            )
            return response(200, {'message': 'Status tiket diperbarui', 'data': ticket_data})

        # 4. DELETE (DELETE /tickets/{ticket_id})
        elif http_method == 'DELETE' and ticket_id:
            s3.head_object(Bucket=BUCKET_NAME, Key=f'tickets/{ticket_id}.json')
            s3.delete_object(Bucket=BUCKET_NAME, Key=f'tickets/{ticket_id}.json')
            return response(200, {'message': f'Tiket {ticket_id} berhasil dihapus'})

        else:
            return response(400, {'error': 'Kombinasi rute atau metode HTTP tidak valid'})

    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code in ('NoSuchKey', '404'):
            return response(404, {'error': f'Tiket {ticket_id} tidak ditemukan'})
        return response(500, {'error': str(e)})
    except Exception as e:
        return response(500, {'error': str(e)})
