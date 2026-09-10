from src.document_validator import ComplianceChecker

checker = ComplianceChecker()
sample = "The document includes an author, revision history, signature, citations, key clauses, and a recommendation section."

print(checker.check(sample))