"""Idempotent seed for the TECHWOOD WPC price list (from PPT - TECHWOOD.xlsx).

Run:  python db/seed_products.py
Safe to re-run: existing product ids are left untouched (so admin edits are not overwritten).
Use --reset to wipe and reload the 9 original rows.
"""
import sys
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import database

# (id, sl, name, code, category, type, image, dimensions, L, W, T, price, dealer_price, architect_price, unit, application, clip_id, clips, needs_better_image)
DEFAULT_VARIANTS = json.dumps(["Antique", "Teak", "IPE", "Maple"])
VALIDITY_DATE = "2026-12-31"

PRODUCTS = [
    ("PRD-001", 1, "Twix", None, "Cladding", "main", "/product-images/twix.jpg",
     "2900 x 200 x 25mm", 2900, 200, 25, 850.0, 765.0, 722.5, "SFT", "Cladding, Ceiling, Gate etc.", "PRD-005", 7, 0),
    ("PRD-002", 2, "Twix", "UH94", "Cladding", "main", "/product-images/twix-uh94.jpg",
     "2900 x 200 x 25mm", 2900, 200, 25, 850.0, 765.0, 722.5, "SFT", "Cladding, Ceiling, Gate etc.", "PRD-005", 7, 0),
    ("PRD-003", 3, "Clads", None, "Cladding", "main", "/product-images/clads.jpg",
     "2200 x 144 x 23mm", 2200, 144, 23, 850.0, 765.0, 722.5, "SFT", "Cladding, Ceiling, Gate etc.", "PRD-005", 7, 0),
    ("PRD-004", 4, "Twix Profile", None, "Accessories", "accessory", "/product-images/twix-profile.jpg",
     "2900 x 75 x 54mm / 2900 x 75 x 77.5mm", 2900, 75, 54, 5300.0, 4770.0, 4505.0, "Plank", "Outside Corner + F trim", None, None, 0),
    ("PRD-005", 5, "Clip", None, "Accessories", "accessory", "/product-images/clip.jpg",
     None, None, None, None, 35.0, 31.5, 29.75, "Clip", "7 clips per plank", None, None, 1),
    ("PRD-006", 6, "Deck", None, "Decking", "main", "/product-images/deck.jpg",
     "2200 x 144 x 23mm", 2200, 144, 23, 850.0, 765.0, 722.5, "SFT", "Exterior Flooring", "PRD-008", 6, 0),
    ("PRD-007", 7, "Deck Profiles", None, "Accessories", "accessory", "/product-images/deck-profiles.jpg",
     "2900 x 40 x 40mm", 2900, 40, 40, 4000.0, 3600.0, 3400.0, "Profile", "Corner", None, None, 1),
    ("PRD-008", 8, "Deck Clip", None, "Accessories", "accessory", "/product-images/deck-clip.jpg",
     None, None, None, None, 35.0, 31.5, 29.75, "Clip", "6 clips per plank", None, None, 1),
    ("PRD-009", 9, "Sunshades", None, "Pergola", "main", "/product-images/sunshades.jpg",
     "2900 x 42 x 100mm / 2900 x 42 x 60mm", 2900, 42, 100, 6100.0, 5490.0, 5185.0, "Plank", "Pergola", None, None, 1),
]

COLS = ("id, sl_no, name, code, category, item_type, image_url, dimensions, length_mm, width_mm, "
        "thickness_mm, price, dealer_price, architect_price, price_unit, application, clip_product_id, "
        "clips_per_plank, needs_better_image, variants, validity_date")


def seed(reset=False):
    with database.get_connection() as conn:
        cur = conn.cursor()
        if reset:
            cur.execute("DELETE FROM order_lines;")
            cur.execute("DELETE FROM products WHERE id IN (%s);" % ",".join("?" * len(PRODUCTS)),
                        tuple(p[0] for p in PRODUCTS))
        # clip rows first, so the clip_product_id foreign key always resolves
        ordered = sorted(PRODUCTS, key=lambda p: p[16] is not None)
        added = 0
        for p in ordered:
            row_data = p + (DEFAULT_VARIANTS, VALIDITY_DATE)
            cur.execute(f"INSERT OR REPLACE INTO products ({COLS}) VALUES ({','.join('?' * len(row_data))});", row_data)
            added += 1
        conn.commit()
    print(f"Products seeded: {added} processed.")


if __name__ == "__main__":
    seed(reset="--reset" in sys.argv)
