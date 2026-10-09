"""Database seeder with realistic sample CRM data for NewTechWood."""
import os
import sqlite3
import random
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "ntw_crm.db")

def seed_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    print("Seeding database...")

    # 1. Users
    users_data = [
        ("admin", "admin@newtechwood.in", "admin", "Super Administrator", "superadmin", "active", "SA"),
        ("admin_user", "admin", "admin", "System Administrator", "admin", "active", "AD"),
        ("sales_01", "sales@newtechwood.in", "sales123", "Rohan Verma", "sales", "active", "RV"),
        ("arch_01", "architect@studio.design", "UltraShield2026", "Skyline Architecture Studio", "architect", "active", "SK"),
        ("dlr_01", "dealer@lumberlife.in", "Dealer@2026", "Lumber Life Premier Partner", "dealer", "active", "LL"),
    ]
    cursor.executemany("""
        INSERT OR REPLACE INTO users (id, email, password, full_name, role, status, avatar_initials)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, users_data)

    # 2. Pipeline Projects
    projects_data = [
        # (id, project_name, client_name, location, city, state, country, fy, month, bracket, category, value, sq_ft, discount, days, stage, feedback_pending, notes)
        ("PRJ-101", "Taj Coastal Resort Decking", "Taj Hospitality", "Candolim Beach", "Goa", "Goa", "India", "FY 25-26", 4, "1-5", "UltraShield Decking", 4500000.0, 10700.0, 8.5, 42, "Win", 0, "Approved"),
        ("PRJ-102", "DLF Luxury Penthouse Terrace", "DLF Urban", "Golf Course Ext", "Gurugram", "Haryana", "India", "FY 25-26", 4, "6-10", "Pergola & Cladding", 2800000.0, 5200.0, 12.0, 0, "Pipeline", 1, "Architect sample requested"),
        ("PRJ-103", "Prestige Golfshire Villa", "Prestige Group", "Nandi Hills", "Bengaluru", "Karnataka", "India", "FY 25-26", 5, "11-15", "UltraShield Decking", 6200000.0, 14500.0, 7.0, 38, "Win", 0, "Commercial invoice released"),
        ("PRJ-104", "Oberoi Sky City Promenade", "Oberoi Realty", "Borivali East", "Mumbai", "Maharashtra", "India", "FY 25-26", 5, "16-20", "Exterior Cladding", 3900000.0, 8900.0, 10.0, 0, "Pipeline", 1, "Color finish approval awaited"),
        ("PRJ-105", "Amanora Park Town Boulevard", "Amanora Group", "Hadapsar", "Pune", "Maharashtra", "India", "FY 25-26", 6, "21-25", "Composite Deck Tiles", 1950000.0, 4800.0, 15.0, 0, "Pipeline", 0, "BOQ under verification"),
        ("PRJ-106", "Lodha Belmondo Riverside Lounge", "Lodha Group", "Gahunje", "Pune", "Maharashtra", "India", "FY 25-26", 6, "26-31", "UltraShield Decking", 5100000.0, 12000.0, 9.0, 45, "Win", 0, "Installation in progress"),
        ("PRJ-107", "Alibaug Sunset Cliff Villa", "Private Client", "Awas Beach", "Alibaug", "Maharashtra", "India", "FY 25-26", 7, "1-5", "Architectural Beams", 3400000.0, 7100.0, 11.5, 0, "Pipeline", 1, "Feedback pending from lead designer"),
        ("PRJ-108", "Hyderabad IT Hub Skydeck", "Mindspace REIT", "HITEC City", "Hyderabad", "Telangana", "India", "FY 25-26", 7, "6-10", "UltraShield Decking", 7800000.0, 18500.0, 6.5, 30, "Win", 0, "Completed"),
        ("PRJ-109", "Chennai ECR Beach House", "Greenfield Homes", "ECR Road", "Chennai", "Tamil Nadu", "India", "FY 25-26", 8, "11-15", "All-Weather Cladding", 2600000.0, 6000.0, 14.0, 0, "Pipeline", 1, "Awaiting quote signoff"),
        ("PRJ-110", "Kolkata Eco Park Boardwalk", "WBHIDCO", "New Town", "Kolkata", "West Bengal", "India", "FY 25-26", 8, "16-20", "UltraShield Decking", 8900000.0, 21000.0, 5.0, 50, "Win", 0, "Delivered"),
        ("PRJ-111", "Udaipur Lakeview Heritage Courtyard", "HRH Group", "Lake Pichola", "Udaipur", "Rajasthan", "India", "FY 25-26", 9, "21-25", "Architectural Pergola", 4100000.0, 8800.0, 9.5, 0, "Pipeline", 1, "Material sample pending test"),
        ("PRJ-112", "Jaipur Fairmont Pool Deck", "Fairmont Hotels", "Kukas", "Jaipur", "Rajasthan", "India", "FY 25-26", 9, "26-31", "UltraShield Decking", 5700000.0, 13400.0, 8.0, 35, "Win", 0, "Finished"),
        ("PRJ-113", "Ahmedabad Riverfront Pavilion", "Sabarmati DCL", "Riverfront West", "Ahmedabad", "Gujarat", "India", "FY 25-26", 10, "1-5", "Composite Decking", 6500000.0, 15200.0, 7.5, 0, "Pipeline", 1, "Structural engineer review"),
        ("PRJ-114", "Kochi Marina Yacht Club", "Kerala Tourism", "Bolgatty Island", "Kochi", "Kerala", "India", "FY 25-26", 10, "6-10", "UltraShield Decking", 4800000.0, 11000.0, 10.0, 40, "Win", 0, "Completed"),
        ("PRJ-115", "Chandigarh Sector 9 Residence", "Ar. Mehta & Assoc", "Sector 9", "Chandigarh", "Punjab", "India", "FY 25-26", 11, "11-15", "Exterior Cladding", 2200000.0, 5100.0, 13.0, 0, "Pipeline", 1, "Feedback pending on Peruvian Teak finish"),
        ("PRJ-116", "Noida Cyber One Rooftop", "Bhutani Group", "Sector 140A", "Noida", "Uttar Pradesh", "India", "FY 25-26", 11, "16-20", "Composite Decking", 5400000.0, 12800.0, 8.0, 36, "Win", 0, "Won"),
        ("PRJ-117", "Lonavala Hilltop Bungalow", "Signature Estates", "Tungarli", "Lonavala", "Maharashtra", "India", "FY 25-26", 12, "21-25", "UltraShield Decking", 3100000.0, 7200.0, 11.0, 0, "Pipeline", 1, "Budget re-allocation in progress"),
        ("PRJ-118", "Surat Diamond Bourse Walkways", "SDB Committee", "DREAM City", "Surat", "Gujarat", "India", "FY 25-26", 12, "26-31", "UltraShield Decking", 9400000.0, 22500.0, 6.0, 28, "Win", 0, "Delivered"),
        ("PRJ-119", "Dehradun Pines Mountain Villa", "Pines Retreat", "Mussoorie Rd", "Dehradun", "Uttarakhand", "India", "FY 25-26", 1, "1-5", "Exterior Cladding", 2700000.0, 6300.0, 12.0, 0, "Pipeline", 0, "Under review"),
        ("PRJ-120", "Indore Super Corridor Tech Park", "Brilliant Estates", "Super Corridor", "Indore", "Madhya Pradesh", "India", "FY 25-26", 2, "6-10", "UltraShield Decking", 4300000.0, 10200.0, 9.0, 33, "Win", 0, "Invoiced"),
    ]
    cursor.executemany("""
        INSERT OR REPLACE INTO pipeline_projects (
            id, project_name, client_name, location, city, state, country,
            financial_year, month, day_bracket, category, total_value, sq_ft,
            discount_pct, days_pipeline_to_win, stage, feedback_pending, feedback_notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, projects_data)

    # 3. Directory Firms & Contacts
    firms_data = [
        ("FRM-01", "Morphogenesis Architecture Studio", "PROPLUS", "New Delhi", "Delhi", "India", "active"),
        ("FRM-02", "Sanjay Puri Architects", "PROPLUS", "Mumbai", "Maharashtra", "India", "active"),
        ("FRM-03", "Cadence Architects", "Architect", "Bengaluru", "Karnataka", "India", "active"),
        ("FRM-04", "Studio Lotus", "PRO", "New Delhi", "Delhi", "India", "active"),
        ("FRM-05", "Abin Design Studio", "Architect", "Kolkata", "West Bengal", "India", "active"),
        ("FRM-06", "Edifice Consultants Pvt Ltd", "PROPLUS", "Mumbai", "Maharashtra", "India", "active"),
        ("FRM-07", "Mindspace Architects", "PRO", "Bengaluru", "Karnataka", "India", "active"),
        ("FRM-08", "Spaces Architects@ka", "Architect", "New Delhi", "Delhi", "India", "active"),
    ]
    cursor.executemany("""
        INSERT OR REPLACE INTO directory_firms (id, firm_name, category, city, state, country, status)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, firms_data)

    contacts_data = [
        ("CNT-01", "FRM-01", "Sonali", "Rastogi", "Principal Architect", "+91 98110 24510", "sonali@morphogenesis.org", 1),
        ("CNT-02", "FRM-01", "Manit", "Rastogi", "Principal Architect", "+91 98110 24511", "manit@morphogenesis.org", 0),
        ("CNT-03", "FRM-01", "Karan", "Malhotra", "Procurement Head", "+91 98110 24519", "procurement@morphogenesis.org", 0),
        ("CNT-04", "FRM-02", "Sanjay", "Puri", "Principal Architect", "+91 98200 45678", "sanjay@sanjaypuriarchitects.com", 1),
        ("CNT-05", "FRM-02", "Torquat", "Fernandes", "Senior Associate", "+91 98200 45690", "torquat@sanjaypuriarchitects.com", 0),
        ("CNT-06", "FRM-03", "Smaran", "Mallesh", "Principal Architect", "+91 98450 12345", "smaran@cadencearchitects.com", 1),
        ("CNT-07", "FRM-03", "Vikram", "Rajashekar", "Design Partner", "+91 98450 12346", "vikram@cadencearchitects.com", 0),
        ("CNT-08", "FRM-04", "Ambrish", "Arora", "Design Principal", "+91 98100 87654", "ambrish@studiolotus.in", 1),
        ("CNT-09", "FRM-04", "Asha", "Seshadri", "Project Lead", "+91 98100 87655", "asha@studiolotus.in", 0),
        ("CNT-10", "FRM-05", "Abin", "Chaudhuri", "Founder & Principal", "+91 98310 99887", "abin@abindesignstudio.com", 1),
        ("CNT-11", "FRM-06", "Ravi", "Sarin", "Director", "+91 98201 11223", "ravi.sarin@edifice.co.in", 1),
        ("CNT-12", "FRM-07", "Sanjay", "Mohe", "Principal Architect", "+91 98452 33445", "mohe@mindspace.in", 1),
        ("CNT-13", "FRM-08", "Kapil", "Aggarwal", "Principal Architect", "+91 98112 55667", "kapil@spacesarchitects.com", 1),
    ]
    cursor.executemany("""
        INSERT OR REPLACE INTO directory_contacts (id, firm_id, first_name, last_name, user_type, mobile, email, is_primary)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, contacts_data)

    # 4. Meetings
    meetings_data = [
        ("MTG-01", "2026-10-02", "Morphogenesis Architecture Studio", "Karan Malhotra", "+91 98110 24519", "Existing", "Architect", "India", "Delhi", "New Delhi", "Completed", "Discussed UltraShield Peruvian Teak specs for resort project.", '["/wp-content/uploads/sample1.jpg"]'),
        ("MTG-02", "2026-10-04", "Sanjay Puri Architects", "Torquat Fernandes", "+91 98200 45690", "Existing", "Architect", "India", "Maharashtra", "Mumbai", "Completed", "Cladding sample box presented. Client requested fire rating reports.", '["/wp-content/uploads/sample2.jpg"]'),
        ("MTG-03", "2026-10-05", "Design Cell Landscape Studio", "Neha Khurana", "+91 98711 34567", "New", "Landscape Architect", "India", "Delhi", "Gurugram", "Completed", "Initial introductory meeting. Introduced quick-lock deck tiles.", '[]'),
        ("MTG-04", "2026-10-06", "Cadence Architects", "Vikram Rajashekar", "+91 98450 12346", "Existing", "Architect", "India", "Karnataka", "Bengaluru", "Completed", "Villa project decking calculation verified (850 sq.ft).", '[]'),
        ("MTG-05", "2026-10-08", "Studio Lotus", "Asha Seshadri", "+91 98100 87655", "Existing", "Interior Designer", "India", "Delhi", "New Delhi", "Completed", "Pergola structural joist spacing confirmed at 16 inches on center.", '[]'),
    ]
    cursor.executemany("""
        INSERT OR REPLACE INTO meetings (
            id, meeting_date, firm_name, guest_name, mobile, user_type,
            guest_type, country, state, city, status, discussion_notes, image_urls
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, meetings_data)

    # 5. ID Invitations
    invitations_data = [
        ("INV-001", "NTW-INV-7891", "Ar. Rahul Deshmukh", "Deshmukh & Associates", "rahul@deshmukh-arch.com", "+91 98220 11223", "https://newtechwood.in/invite/NTW-INV-7891", "Active", "2026-11-09"),
        ("INV-002", "NTW-INV-7892", "Pooja Singhania", "Vibrant Spaces Interior", "pooja@vibrantspaces.in", "+91 98300 22334", "https://newtechwood.in/invite/NTW-INV-7892", "Active", "2026-11-09"),
        ("INV-003", "NTW-INV-7893", "Ar. Tarun Bakshi", "Bakshi Design Atelier", "tarun@bakshiatelier.com", "+91 98100 33445", "https://newtechwood.in/invite/NTW-INV-7893", "Accepted", "2026-10-15"),
        ("INV-004", "NTW-INV-7894", "Ananya Rao", "South Coast Builders", "ananya@southcoast.co.in", "+91 98480 44556", "https://newtechwood.in/invite/NTW-INV-7894", "Active", "2026-11-09"),
    ]
    cursor.executemany("""
        INSERT OR REPLACE INTO id_invitations (
            id, invitation_code, recipient_name, firm_name, recipient_email,
            mobile, invitation_link, status, expires_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, invitations_data)

    # 6. ID Visitors
    visitors_data = [
        ("VIS-01", "Architect", "Sameer Chawla", "+91 98114 55667", "sameer@chawla.design", "Chawla Design Studio", "2026-09-15", "2026-09-16", "India", "Delhi", "New Delhi", "2026"),
        ("VIS-02", "VIP Guest", "Vikramaditya Oberoi", "+91 98204 66778", "vo@oberoiholdings.in", "Oberoi Luxury Living", "2026-09-18", "2026-09-18", "India", "Maharashtra", "Mumbai", "2026"),
        ("VIS-03", "Contractor", "Gurpreet Singh", "+91 98184 77889", "gurpreet@gsconstructions.com", "GS Infrastructure", "2026-09-22", "2026-09-23", "India", "Punjab", "Chandigarh", "2026"),
        ("VIS-04", "Architect", "Shruti Iyer", "+91 98454 88990", "shruti@iyerassociates.in", "Iyer & Partners", "2026-09-25", "2026-09-25", "India", "Karnataka", "Bengaluru", "2026"),
        ("VIS-05", "Partner", "Manish Toshniwal", "+91 98294 99001", "manish@toshniwal.in", "Toshniwal Timber Traders", "2026-09-28", "2026-09-29", "India", "Rajasthan", "Jaipur", "2026"),
        ("VIS-06", "Architect", "Farhan Contractor", "+91 98205 10112", "farhan@contractordesign.com", "Studio FC", "2026-10-01", "2026-10-02", "India", "Maharashtra", "Pune", "2026"),
        ("VIS-07", "VIP Guest", "Nirmal Somani", "+91 98315 21223", "nirmal@somani.in", "Somani Real Estate", "2026-10-03", "2026-10-03", "India", "West Bengal", "Kolkata", "2026"),
    ]
    cursor.executemany("""
        INSERT OR REPLACE INTO id_visitors (
            id, visitor_type, name, mobile, email, firm,
            link_created_date, form_submitted_date, country, state, city, event_year
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, visitors_data)

    # 7. Go Pro / Education Assets
    assets_data = [
        ("ASST-01", "UltraShield Decking Full Installation Masterclass", "Tech Team NewTechWood", "MP4 Video", "18:24", "/videos/installation_masterclass.mp4", "/wp-content/uploads/gopro_thumb1.jpg", "Installation Guide", 1420),
        ("ASST-02", "Sub-Frame Aluminum Joist Spacing & Elevation Best Practices", "Engineering Dept", "MP4 Video", "12:15", "/videos/subframe_spacing.mp4", "/wp-content/uploads/gopro_thumb2.jpg", "Technical Standards", 980),
        ("ASST-03", "All-Weather Cladding Hidden Fastener System Walkthrough", "Product Specialist", "MP4 Video", "09:40", "/videos/cladding_fasteners.mp4", "/wp-content/uploads/gopro_thumb3.jpg", "Façade Engineering", 1150),
        ("ASST-04", "Care, Cleaning & Scratch Repair on 360 Capped Composite", "QA & Materials Lab", "MP4 Video", "06:50", "/videos/cleaning_maintenance.mp4", "/wp-content/uploads/gopro_thumb4.jpg", "Maintenance", 840),
        ("ASST-05", "Quick-Lock Interlocking Deck Tiles Balcony Transformation", "Design Studio", "MP4 Video", "08:12", "/videos/balcony_tiles.mp4", "/wp-content/uploads/gopro_thumb5.jpg", "Patio & DIY", 1630),
    ]
    cursor.executemany("""
        INSERT OR REPLACE INTO go_pro_assets (
            id, subject, creator, file_type, duration, video_url, thumbnail_url, category, views_count
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, assets_data)

    # 8. Waltz Orders
    orders_data = [
        ("ORD-W-501", "WO-2026-001", "Goa Coastal Beachfront Villa", "Taj Hospitality", "India", "Goa", "Candolim", "2026-10-01", "Win", 421260.0, "Direct Architect", "Accepted & invoiced"),
        ("ORD-W-502", "WO-2026-002", "Alibaug Cliff Villa Terrace", "Signature Estates", "India", "Maharashtra", "Alibaug", "2026-10-03", "Pipeline", 685000.0, "Experience Centre", "BOQ finalized, awaiting PO"),
        ("ORD-W-503", "WO-2026-003", "DLF Golf Links Penthouse", "DLF Urban", "India", "Haryana", "Gurugram", "2026-10-04", "Win", 1250000.0, "Dealer Referral", "Advance payment received"),
        ("ORD-W-504", "WO-2026-004", "Prestige Golfshire Louver Wall", "Prestige Group", "India", "Karnataka", "Bengaluru", "2026-10-05", "Win", 890000.0, "Website Lead", "Dispatched to site"),
        ("ORD-W-505", "WO-2026-005", "Lonavala Weekend Villa", "Private Client", "India", "Maharashtra", "Lonavala", "2026-10-06", "Lost", 340000.0, "Direct Architect", "Client postponed outdoor renovation"),
        ("ORD-W-506", "WO-2026-006", "Hyderabad IT Park Walkway", "Mindspace REIT", "India", "Telangana", "Hyderabad", "2026-10-07", "Win", 2150000.0, "Direct Architect", "Commercial contract signed"),
        ("ORD-W-507", "WO-2026-007", "Chennai ECR Seaside Cottage", "Greenfield Homes", "India", "Tamil Nadu", "Chennai", "2026-10-08", "Pipeline", 540000.0, "Website Lead", "Peruvian Teak sample sent"),
    ]
    cursor.executemany("""
        INSERT OR REPLACE INTO waltz_orders (
            id, order_number, project_name, client_name, country, state, city,
            order_date, status, final_amount, source, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, orders_data)

    conn.commit()
    conn.close()
    print("Database seeding completed with rich sample records!")

if __name__ == "__main__":
    seed_database()
