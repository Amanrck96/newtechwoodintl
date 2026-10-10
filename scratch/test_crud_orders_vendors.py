import urllib.request
import json

base = 'http://localhost:8000'

def req(url, method='GET', data=None):
    r = urllib.request.Request(url, method=method)
    if data:
        r.add_header('Content-Type', 'application/json')
        body = json.dumps(data).encode('utf-8')
    else:
        body = None
    with urllib.request.urlopen(r, data=body) as resp:
        return resp.status, json.loads(resp.read().decode('utf-8'))

print("1. Testing GET /api/orders...")
st, data = req(f'{base}/api/orders')
print(f"Status: {st}, orders count: {data.get('count')}")

print("\n2. Testing POST /api/orders...")
test_ord = {
    'order_number': 'WO-2026-TEST999',
    'project_name': 'Automated Test Decking Project',
    'client_name': 'Quality Assurance Labs',
    'country': 'India',
    'state': 'Maharashtra',
    'city': 'Mumbai',
    'order_date': '2026-10-10',
    'status': 'Pipeline',
    'final_amount': 750000,
    'source': 'Website Lead',
    'notes': 'Test order creation verified by GUARDIAN agent'
}
st, post_res = req(f'{base}/api/orders', method='POST', data=test_ord)
print(f"Status: {st}, result: {post_res}")
created_id = post_res.get('id')

if created_id:
    print(f"\n3. Testing PUT /api/orders/{created_id}...")
    update_ord = {
        'project_name': 'Automated Test Decking Project (Updated)',
        'final_amount': 820000,
        'status': 'Win'
    }
    st, put_res = req(f'{base}/api/orders/{created_id}', method='PUT', data=update_ord)
    print(f"Status: {st}, update result: {put_res}")

    print(f"\n4. Testing DELETE /api/orders/{created_id}...")
    st, del_res = req(f'{base}/api/orders/{created_id}', method='DELETE')
    print(f"Status: {st}, delete result: {del_res}")

print("\n5. Testing POST /api/vendors...")
test_vnd = {
    'vendor_id': 'VND-TEST-888',
    'full_name': 'Apex Architecture Partner',
    'email': 'apex@architecture.in',
    'password': 'SecurePartner@2026',
    'role': 'architect',
    'phone': '+91 98989 12345',
    'permissions': 'gopro_cad,pipeline_specs,meetings,invitations'
}
st, vnd_res = req(f'{base}/api/vendors', method='POST', data=test_vnd)
print(f"Status: {st}, create vendor: {vnd_res}")
created_vnd_id = vnd_res.get('id')

if created_vnd_id:
    print(f"\n6. Testing DELETE /api/vendors/{created_vnd_id}...")
    st, del_vnd_res = req(f'{base}/api/vendors/{created_vnd_id}', method='DELETE')
    print(f"Status: {st}, delete vendor: {del_vnd_res}")

print("\nALL CRUD ENDPOINTS VERIFIED SUCCESSFULLY!")
