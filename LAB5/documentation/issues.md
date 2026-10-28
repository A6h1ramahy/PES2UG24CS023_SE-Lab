# Lab 5 — Static Code Analysis: Issue Log

**Student:** Abhirama H Y  
**SRN:** PES2UG24CS023  
**Section:** A  
**Assigned repository:** https://github.com/SETAPESU26/L5_20_scholarship_disbursement  
**Working repository:** https://github.com/A6h1ramahy/PES2UG24CS023_SE-Lab/tree/main/LAB5

> Important: line numbers and exact tool messages must be filled from the actual BEFORE reports generated on your computer. Do not invent line numbers or claim a finding was reported unless it appears in your report.

| # | Issue / finding | Tool/category | Before line(s) | Risk / impact | Fix applied | Verification evidence |
|---|---|---|---|---|---|---|
| 1 | SQL query built using string interpolation/concatenation | Bandit/security | Fill from report | Untrusted input can change SQL query structure (SQL injection). | Use parameterized SQL (`?` placeholders) and pass values separately. | Bandit after report; inspect SQL calls. |
| 2 | Shell command executed through `os.system` | Bandit/security | Fill from report | Shell interpretation can allow command injection and makes behavior harder to control. | Remove shell execution; use Python APIs directly. If a subprocess is genuinely needed, pass an argument list and avoid `shell=True`. | Bandit after report; search for `os.system` and `shell=True`. |
| 3 | Mutable default such as `audit=[]` | Pylint/design | Fill from report | A shared list can retain entries across calls unexpectedly. | Use `None` as the default and create a new list inside the function. | Pylint after report; test repeated calls. |
| 4 | Broad exception swallowed, e.g. `except Exception: pass` | Pylint/robustness | Fill from report | Errors are hidden, leaving callers unaware that an operation failed. | Catch only expected exceptions, log context where appropriate, and re-raise or report the error. | Pylint after report; review exception handling. |
| 5 | Non-PEP 8 identifier such as `bySchemeCount` | Pylint/style | Fill from report | Inconsistent naming reduces readability and may trigger style warnings. | Rename to `count_by_scheme`. | Pylint and Flake8 after reports. |
| 6 | Comparison to `None` using `==` | Pylint/style | Fill from report | Python convention is identity comparison; this is clearer and avoids custom equality behavior. | Use `is None` / `is not None`. | Pylint after report. |
| 7 | Weak input validation for student, scheme, and amount | Correctness/robustness | Fill from inspection | Empty identifiers, invalid numbers, non-finite values, or non-positive amounts may enter the ledger. | Normalize text and validate amount before database write. | Run the program and test invalid values. |
| 8 | Duplicate disbursement may be recorded more than once | Correctness/data integrity | Fill from inspection | A duplicate entry can cause a student to be counted or paid twice. | Add a uniqueness constraint on `(student_id, scheme)` and handle duplicate insertion. | Test a duplicate record and verify it is rejected. |

## Notes
- This is a working issue log for the supplied solution pattern. Confirm each item against the actual original file and generated analyzer reports.
- Record the exact line numbers from `reports\pylint_report_before.txt`, `reports\bandit_report_before.txt`, and `reports\flake8_report_before.txt`.
- The assignment asks for at least four issues, all Bandit findings fixed, Pylint score above 9.5, Flake8 findings addressed, before/after reports, and three commits.
