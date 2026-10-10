# Test script to verify analytics calculation logic matches api_router.py
import json

orders = [
  {"id": "ORD-NTW-501", "order_number": "NTW-2026-001", "project_name": "Goa Coastal Beachfront Villa", "client_name": "Taj Hospitality", "city": "Candolim", "state": "Goa", "order_date": "2026-10-01", "status": "Win", "final_amount": 421260.0, "source": "Direct Architect", "owner_name": "Super Administrator"},
  {"id": "ORD-NTW-502", "order_number": "NTW-2026-002", "project_name": "Alibaug Cliff Villa Terrace", "client_name": "Signature Estates", "city": "Alibaug", "state": "Maharashtra", "order_date": "2026-10-03", "status": "Pipeline", "final_amount": 685000.0, "source": "Experience Centre", "owner_name": "Skyline Architecture Studio"},
  {"id": "ORD-NTW-503", "order_number": "NTW-2026-003", "project_name": "DLF Golf Links Penthouse", "client_name": "DLF Urban", "city": "Gurugram", "state": "Haryana", "order_date": "2026-10-04", "status": "Win", "final_amount": 1250000.0, "source": "Dealer Referral", "owner_name": "Lumber Life Premier Partner"},
  {"id": "ORD-NTW-504", "order_number": "NTW-2026-004", "project_name": "Prestige Golfshire Louver Wall", "client_name": "Prestige Group", "city": "Bengaluru", "state": "Karnataka", "order_date": "2026-10-05", "status": "Win", "final_amount": 890000.0, "source": "Website Lead", "owner_name": "Super Administrator"},
  {"id": "ORD-NTW-505", "order_number": "NTW-2026-005", "project_name": "Lonavala Weekend Villa", "client_name": "Private Client", "city": "Lonavala", "state": "Maharashtra", "order_date": "2026-10-06", "status": "Lost", "final_amount": 340000.0, "source": "Direct Architect", "owner_name": "Skyline Architecture Studio"},
  {"id": "ORD-NTW-506", "order_number": "NTW-2026-006", "project_name": "Hyderabad IT Park Walkway", "client_name": "Mindspace REIT", "city": "Hyderabad", "state": "Telangana", "order_date": "2026-10-07", "status": "Win", "final_amount": 2150000.0, "source": "Direct Architect", "owner_name": "Super Administrator"},
  {"id": "ORD-NTW-507", "order_number": "NTW-2026-007", "project_name": "Chennai ECR Seaside Cottage", "client_name": "Greenfield Homes", "city": "Chennai", "state": "Tamil Nadu", "order_date": "2026-10-08", "status": "Pipeline", "final_amount": 540000.0, "source": "Website Lead", "owner_name": "Lumber Life Premier Partner"}
]

print(f"Loaded {len(orders)} fallback orders")
