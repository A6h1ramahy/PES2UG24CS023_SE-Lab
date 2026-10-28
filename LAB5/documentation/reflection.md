# Lab 5 — Reflection Answers

**Student:** Abhirama H Y  
**SRN:** PES2UG24CS023  
**Section:** A

### 1. What is static code analysis, and how is it useful?
Static code analysis examines source code without running the program. It helps identify likely bugs, insecure patterns, and style violations early, making code easier to review and maintain. It complements, rather than replaces, tests and runtime checks.

### 2. What differences did you observe between Pylint, Bandit, and Flake8?
Pylint focuses broadly on code quality, naming, design, and possible logical problems, and provides a score. Bandit focuses on security-sensitive patterns such as unsafe shell execution or risky handling of input. Flake8 primarily reports style and basic code-quality issues such as whitespace, line length, and unused names. Their purposes overlap slightly, but they are not interchangeable.

### 3. Which issues were most important, and why?
Security issues such as constructing SQL from untrusted strings or invoking shell commands unsafely deserve high priority because they may allow unintended operations. Data-integrity problems, including duplicate disbursements, and hidden exceptions are also important because they can corrupt results or make failures difficult to detect.

### 4. How did static analysis improve the program, and what are its limitations?
The review encouraged parameterized SQL, explicit validation, safer exception handling, clearer naming, and consistent formatting. However, a clean report does not prove that a program is correct or secure: tools may miss context-dependent defects and can report false positives. The code still needs tests, manual review, and verification of expected behavior.
