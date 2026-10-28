# Lab 5 — Static Code Analysis: Issues Identified and Fixes

**Student:** Abhirama H Y  
**SRN:** PES2UG24CS023  
**Section:** A  
**Program:** `scholarship_disbursement.py`

This issue log is based on the supplied Pylint, Bandit, and Flake8 BEFORE/AFTER reports. Items described as manual-review items were not independently verified by those analyzer reports.

| # | Issue | Category / Tool | Evidence before fixes | Fix applied / recommended | Evidence after fixes / status |
|---:|---|---|---|---|---|
| 1 | SQL statement constructed using string interpolation | Security — Bandit | Original file, line 10; Bandit reported **B608**, Medium severity, Medium confidence. | Use a parameterized SQL query and pass values separately as query parameters. | The supplied AFTER Bandit report says no issues were identified. |
| 2 | Unsafe shell execution | Security — Bandit | Original file, line 26; Bandit reported **B605** and **B607**, Low severity. | Remove shell execution where unnecessary. If an external process is required, use a safer API and avoid shell interpretation. | The supplied AFTER Bandit report says no issues were identified. |
| 3 | Exception silently swallowed | Security / code quality — Bandit and Pylint | Original file, lines 27–28; Bandit reported **B110** (Low); Pylint reported **W0718** for catching `Exception` at line 27. | Catch expected exception types, log useful context, and re-raise when the caller needs to know the operation failed. Avoid a silent `pass`. | The supplied AFTER Bandit report says no issues were identified. The reported broad-exception finding is not listed in the supplied AFTER Pylint report. |
| 4 | Mutable default list argument | Code quality — Pylint | Original file, line 9; Pylint reported **W0102** (`dangerous-default-value`). | Change the default to `None`, then create a new list inside the function when no list is provided. | This finding is not listed in the supplied AFTER Pylint report. |
| 5 | Function name does not follow snake_case | Code quality — Pylint | Original file, line 31; Pylint reported **C0103** (`invalid-name`) for `bySchemeCount`. | Rename it to `count_by_scheme` and update call sites. | This finding is not listed in the supplied AFTER Pylint report. |
| 6 | Equality comparison with `None` | Code quality / style — Pylint and Flake8 | Original file, line 32; Pylint reported **C0121** and Flake8 reported **E711**. | Use `scheme is None`. | This finding is not listed in the supplied AFTER Pylint or Flake8 reports. |
| 7 | Unused `Iterable` import remains | Code quality / style — Pylint and Flake8 | Not reported in the supplied BEFORE reports; appears in the AFTER reports at `scholarship_disbursement.py`, line 18. | Remove `Iterable` from the import statement if it is not used. | **Still present:** Pylint **W0611** and Flake8 **F401**, line 18. |
| 8 | Lines exceed configured style limit | Style — Flake8 | BEFORE Flake8 reported long lines at lines 5, 10, 17, 19, and 34. The original `None` comparison also produced E711 at line 32. | Wrap long statements and keep lines within the configured limit. | **Still present:** Flake8 **E501** at lines 104, 153, and 154. |
| 9 | Missing docstrings and other maintainability findings | Code quality — Pylint | BEFORE Pylint reported missing module/function docstrings and other quality findings; original score was **5.00/10**. | Add meaningful module/function docstrings, improve naming and control flow, and address the reported warnings. | AFTER Pylint score is **9.86/10**. The unused-import warning remains. |
| 10 | Input validation | Correctness — manual review | Not established by the supplied analyzer reports. | Validate that student ID and scheme are non-empty and that the amount is a finite positive number. | Treat as a code-review item. The supplied reports alone do not prove that input-validation tests passed. |
| 11 | Duplicate disbursement handling | Data integrity — manual review | Not established by the supplied analyzer reports. | Enforce a uniqueness rule for the student/scheme combination and handle database integrity errors explicitly. | Treat as a code-review item. The supplied reports alone do not prove duplicate-record tests passed. |

## Analyzer summary

| Tool | Before | After | Assessment |
|---|---|---|---|
| Pylint | **5.00/10** | **9.86/10** | Score exceeds 9.5/10, but the unused `Iterable` import warning remains. |
| Bandit | **4 findings:** 1 Medium and 3 Low | No issues identified | The supplied AFTER report indicates that the reported security findings were resolved. |
| Flake8 | **6 findings** | **4 findings** | Not clean yet: remove the unused `Iterable` import and wrap the three lines reported with E501. |
