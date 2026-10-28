"""
Lab 5: Static Code Analysis
Student: Abhirama H Y
SRN: PES2UG24CS023
Section: A

A small scholarship disbursement ledger demonstrating safer input handling,
parameterized SQL, explicit validation, and audit logging.
"""

from __future__ import annotations

import logging
import sqlite3
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class Disbursement:
    """Represents a validated scholarship disbursement."""

    student_id: str
    scheme: str
    amount: Decimal


def validate_disbursement(
    student_id: str,
    scheme: str,
    amount: Decimal | str | int | float,
) -> Disbursement:
    """Validate and normalize the fields for one disbursement."""
    normalized_student_id = student_id.strip()
    normalized_scheme = scheme.strip()

    if not normalized_student_id:
        raise ValueError("student_id must not be empty")
    if not normalized_scheme:
        raise ValueError("scheme must not be empty")

    try:
        normalized_amount = Decimal(str(amount))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("amount must be a valid number") from exc

    if not normalized_amount.is_finite() or normalized_amount <= 0:
        raise ValueError("amount must be a finite positive number")

    return Disbursement(
        student_id=normalized_student_id,
        scheme=normalized_scheme,
        amount=normalized_amount,
    )


def create_schema(connection: sqlite3.Connection) -> None:
    """Create the ledger table if it does not already exist."""
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


def record_disbursement(
    connection: sqlite3.Connection,
    student_id: str,
    scheme: str,
    amount: Decimal | str | int | float,
    audit_log: list[str] | None = None,
) -> Disbursement:
    """Validate and record a disbursement once for a student and scheme."""
    item = validate_disbursement(student_id, scheme, amount)
    audit_entries = audit_log if audit_log is not None else []

    try:
        connection.execute(
            """
            INSERT INTO disbursements (student_id, scheme, amount)
            VALUES (?, ?, ?)
            """,
            (item.student_id, item.scheme, str(item.amount)),
        )
        connection.commit()
    except sqlite3.IntegrityError as exc:
        connection.rollback()
        LOGGER.warning(
            "Duplicate disbursement rejected for student %s and scheme %s",
            item.student_id,
            item.scheme,
        )
        raise ValueError("A disbursement already exists for this student and scheme") from exc
    except sqlite3.Error:
        connection.rollback()
        LOGGER.exception("Could not record scholarship disbursement")
        raise

    audit_entries.append(
        f"Recorded {item.amount} for {item.student_id} under {item.scheme}"
    )
    return item


def count_by_scheme(connection: sqlite3.Connection) -> dict[str, int]:
    """Return the number of recorded disbursements grouped by scheme."""
    rows = connection.execute(
        """
        SELECT scheme, COUNT(*)
        FROM disbursements
        GROUP BY scheme
        ORDER BY scheme
        """
    ).fetchall()
    return {str(scheme): int(count) for scheme, count in rows}


def list_disbursements(connection: sqlite3.Connection) -> list[Disbursement]:
    """Return all ledger entries in a deterministic order."""
    rows = connection.execute(
        """
        SELECT student_id, scheme, amount
        FROM disbursements
        ORDER BY student_id, scheme
        """
    ).fetchall()
    return [
        Disbursement(
            student_id=str(student_id),
            scheme=str(scheme),
            amount=Decimal(str(amount)),
        )
        for student_id, scheme, amount in rows
    ]


def run_demo(database_path: str | Path = ":memory:") -> None:
    """Run a small demonstration without executing shell commands."""
    audit_log: list[str] = []
    with sqlite3.connect(str(database_path)) as connection:
        create_schema(connection)
        record_disbursement(connection, "STU001", "Merit", "15000.00", audit_log)
        record_disbursement(connection, "STU002", "Need-Based", "10000.00", audit_log)

        print("Disbursements:")
        for item in list_disbursements(connection):
            print(f"{item.student_id}: {item.scheme} - {item.amount}")

        print("Counts by scheme:")
        for scheme, count in count_by_scheme(connection).items():
            print(f"{scheme}: {count}")

        print("Audit entries:")
        for entry in audit_log:
            print(entry)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_demo()
