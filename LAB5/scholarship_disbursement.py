"""
Lab 5: Static Code Analysis
Student: Abhirama H Y
SRN: PES2UG24CS023
Section: A

Stage 1: security fixes only.
Parameterized SQL is used and shell execution has been removed.
Other quality/correctness issues are intentionally left for Stage 2.
"""

import logging
import sqlite3

LOGGER = logging.getLogger(__name__)


def create_schema(connection):
    """Create the scholarship ledger table."""
    connection.execute(
        "CREATE TABLE IF NOT EXISTS disbursements "
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, student_id TEXT, "
        "scheme TEXT, amount REAL)"
    )
    connection.commit()


def record_disbursement(connection, student_id, scheme, amount, audit=[]):
    """Record a scholarship disbursement."""
    try:
        # Security fix: parameterized SQL; values are not concatenated into SQL.
        connection.execute(
            "INSERT INTO disbursements (student_id, scheme, amount) "
            "VALUES (?, ?, ?)",
            (student_id, scheme, amount),
        )
        connection.commit()
        audit.append(f"Recorded {amount} for {student_id} under {scheme}")
    except Exception as error:
        # Intentionally left for the code-quality commit.
        LOGGER.error("Could not record disbursement: %s", error)


def bySchemeCount(connection, scheme=None):
    """Return a count for a scheme, or all schemes when no scheme is supplied."""
    if scheme == None:
        rows = connection.execute(
            "SELECT scheme, COUNT(*) FROM disbursements GROUP BY scheme"
        ).fetchall()
        return {row[0]: row[1] for row in rows}

    row = connection.execute(
        "SELECT COUNT(*) FROM disbursements WHERE scheme = ?", (scheme,)
    ).fetchone()
    return {scheme: row[0]}


def run_demo():
    """Run a simple example."""
    connection = sqlite3.connect(":memory:")
    create_schema(connection)
    record_disbursement(connection, "STU001", "Merit", 15000)
    record_disbursement(connection, "STU002", "Need-Based", 10000)
    print(bySchemeCount(connection))
    connection.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_demo()