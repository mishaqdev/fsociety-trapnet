from collections import Counter
from pathlib import Path
import sqlite3


HONEYPOT_DB_PATH = Path(__file__).resolve().parents[1] / "honeypot.db"


def fetch_attack_rows() -> list[dict]:
    conn = sqlite3.connect(HONEYPOT_DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        SELECT id, ip, requestPath, username, password, user_agent, status, timestamp
        FROM attacks
        ORDER BY timestamp DESC, id DESC
        """
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def build_dashboard_data() -> dict:
    attacks = fetch_attack_rows()
    total_requests = len(attacks)
    ip_counter = Counter(row["ip"] or "Unknown" for row in attacks)
    route_counter = Counter(row["requestPath"] or "Unknown" for row in attacks)
    password_counter = Counter((row["password"] or "(empty)") for row in attacks)
    status_counter = Counter(row["status"] or "unknown" for row in attacks)

    ip_stats = _build_ranked_stats(ip_counter)
    route_stats = _build_ranked_stats(route_counter)
    password_stats = _build_ranked_stats(password_counter)

    overview = {
        "total_requests": total_requests,
        "unique_ips": len(ip_counter),
        "unique_routes": len(route_counter),
        "failed_requests": status_counter.get("failed", 0),
        "successful_requests": status_counter.get("success", 0),
        "top_ip": ip_stats[0]["label"] if ip_stats else "-",
        "top_route": route_stats[0]["label"] if route_stats else "-",
        "top_password": password_stats[0]["label"] if password_stats else "-",
    }

    return {
        "overview": overview,
        "ip_stats": ip_stats,
        "route_stats": route_stats,
        "password_stats": password_stats,
        "attacks": attacks,
    }


def _build_ranked_stats(counter: Counter) -> list[dict]:
    total = sum(counter.values())
    if not total:
        return []

    ranked = []
    for label, count in counter.most_common():
        percent = round((count / total) * 100, 1)
        ranked.append(
            {
                "label": label,
                "count": count,
                "percent": percent,
                "width": max(percent, 3),
            }
        )
    return ranked