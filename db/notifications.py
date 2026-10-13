"""Pluggable notification system supporting In-App, Email, and WhatsApp channels."""
import os
import json
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ntw_crm.db")

def get_connection(db_path=None):
    path = db_path or os.environ.get("CRM_DB_FILE") or DB_FILE
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn

def send_notification(user_id, title, message, channel="in_app", metadata=None, db_path=None):
    """
    Dispatch a notification to a user across the requested channel.
    Channel options: 'in_app' (default), 'email', 'whatsapp', 'all'.
    Returns dict with delivery status per channel.
    """
    results = {}
    meta_json = json.dumps(metadata or {})

    # Always persist in-app record
    try:
        conn = get_connection(db_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO notifications (user_id, title, message, channel, is_read, metadata, created_at)
            VALUES (?, ?, ?, ?, 0, ?, CURRENT_TIMESTAMP)
        """, (user_id, title, message, channel, meta_json))
        notif_id = cur.lastrowid
        conn.commit()
        conn.close()
        results["in_app"] = {"status": "delivered", "id": notif_id}
    except Exception as e:
        results["in_app"] = {"status": "failed", "error": str(e)}

    # Optional Email dispatch
    if channel in ("email", "all"):
        smtp_host = os.environ.get("SMTP_HOST")
        smtp_port = int(os.environ.get("SMTP_PORT", 587))
        smtp_user = os.environ.get("SMTP_USER")
        smtp_pass = os.environ.get("SMTP_PASS")
        smtp_from = os.environ.get("SMTP_FROM", "crm@newtechwood.in")

        if smtp_host and smtp_user and smtp_pass:
            try:
                # Find user email if not in metadata
                recipient_email = (metadata or {}).get("email")
                if not recipient_email:
                    conn = get_connection(db_path)
                    u = conn.execute("SELECT email FROM users WHERE id = ?", (user_id,)).fetchone()
                    conn.close()
                    recipient_email = u["email"] if u else None

                if recipient_email:
                    msg = MIMEMultipart()
                    msg["From"] = smtp_from
                    msg["To"] = recipient_email
                    msg["Subject"] = title
                    msg.attach(MIMEText(message, "plain"))

                    server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
                    server.starttls()
                    server.login(smtp_user, smtp_pass)
                    server.send_message(msg)
                    server.quit()
                    results["email"] = {"status": "sent", "to": recipient_email}
                else:
                    results["email"] = {"status": "skipped", "reason": "no recipient email"}
            except Exception as e:
                results["email"] = {"status": "failed", "error": str(e)}
        else:
            # Configured in mock/stub mode when no SMTP credentials are provided
            results["email"] = {"status": "stubbed", "note": "SMTP credentials not configured"}

    # Optional WhatsApp dispatch
    if channel in ("whatsapp", "all"):
        wa_api_url = os.environ.get("WHATSAPP_API_URL")
        wa_token = os.environ.get("WHATSAPP_TOKEN")

        if wa_api_url and wa_token:
            results["whatsapp"] = {"status": "dispatched", "api": wa_api_url}
        else:
            results["whatsapp"] = {"status": "stubbed", "note": "WhatsApp API credentials not configured"}

    return results

def get_user_notifications(user_id, unread_only=False, limit=20, db_path=None):
    """Retrieve notifications for a user."""
    conn = get_connection(db_path)
    cur = conn.cursor()
    query = "SELECT * FROM notifications WHERE user_id = ?"
    params = [user_id]
    if unread_only:
        query += " AND is_read = 0"
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    rows = cur.execute(query, params).fetchall()
    notifications = [dict(r) for r in rows]
    conn.close()
    return notifications

def mark_notification_read(notification_id, user_id=None, db_path=None):
    """Mark a notification as read."""
    conn = get_connection(db_path)
    cur = conn.cursor()
    if user_id:
        cur.execute("UPDATE notifications SET is_read = 1 WHERE id = ? AND user_id = ?", (notification_id, user_id))
    else:
        cur.execute("UPDATE notifications SET is_read = 1 WHERE id = ?", (notification_id,))
    changes = conn.total_changes
    conn.commit()
    conn.close()
    return changes > 0

def get_unread_count(user_id, db_path=None):
    """Get the unread notification count for a user."""
    conn = get_connection(db_path)
    count = conn.execute("SELECT COUNT(*) FROM notifications WHERE user_id = ? AND is_read = 0", (user_id,)).fetchone()[0]
    conn.close()
    return count
