"""
Lab 5: Static Code Analysis
Student: Abhirama H Y
SRN: PES2UG24CS023
Section: A

Stage 2: security, code-quality, and correctness fixes.
"""

import logging
import sqlite3
from decimal import Decimal, InvalidOperation

LOGGER = logging.getLogger(__name__)


def validate_disbursement(student_id, scheme, amount):
    """Validate and normalize the fields for a disbursement."""
    student_id = student_id.strip()
    scheme = scheme.strip()
    if not student_id:
        raise ValueError("student_id must not be empty")
    if not scheme:
        raise ValueError("scheme must not be empty")
    try:
        amount = Decimal(str(amount))
    except (InvalidOperation, ValueError) as error:
        raise ValueError("amount must be a valid number") from error
    if not amount.is_finite() or amount <= 0:
        raise ValueError("amount must be a finite positive number")
    return student_id, scheme, amount


def create_schema(connection):
    """Create the ledger table and prevent duplicate student/scheme entries."""
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS disbursements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            scheme TEXT NOT NULL,
            amount TEXT NOT NULL,
            UNIQUE(student_id, scheme)
        )
        """
    )
    connection.commit()


def record_disbursement(connection, student_id, scheme, amount, audit_log=None):
    """Validate and record a disbursement once per student and scheme."""
    student_id, scheme, amount = validate_disbursement(student_id, scheme, amount)
    if audit_log is None:
        audit_log = []

    try:
        connection.execute(
            """
            INSERT INTO disbursements (student_id, scheme, amount)
            VALUES (?, ?, ?)
            """,
            (student_id, scheme, str(amount)),
        )
        connection.commit()
    except sqlite3.IntegrityError as error:
        connection.rollback()
        LOGGER.warning(
            "Duplicate disbursement rejected for student %s and scheme %s",
            student_id,
            scheme,
        )
        raise ValueError(
            "A disbursement already exists for this student and scheme"
        ) from error
    except sqlite3.Error:
        connection.rollback()
        LOGGER.exception("Could not record scholarship disbursement")
        raise

    audit_log.append(f"Recorded {amount} for {student_id} under {scheme}")
    return {"student_id": student_id, "scheme": scheme, "amount": amount}


def count_by_scheme(connection, scheme=None):
    """Return counts grouped by scheme, optionally for one scheme."""
    if scheme is None:
        rows = connection.execute(
            "SELECT scheme, COUNT(*) FROM disbursements "
            "GROUP BY scheme ORDER BY scheme"
        ).fetchall()
        return {str(row[0]): int(row[1]) for row in rows}

    row = connection.execute(
        "SELECT COUNT(*) FROM disbursements WHERE scheme = ?", (scheme,)
    ).fetchone()
    return {scheme: int(row[0])}


def run_demo(database_path=":memory:"):
    """Run a small demonstration using an in-memory database by default."""
    audit_log = []
    with sqlite3.connect(database_path) as connection:
        create_schema(connection)
        record_disbursement(connection, "STU001", "Merit", "15000.00", audit_log)
        record_disbursement(
            connection, "STU002", "Need-Based", "10000.00", audit_log
        )
        print("Counts by scheme:")
        print(count_by_scheme(connection))
        print("Audit entries:")
        for entry in audit_log:
            print(entry)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_demo()