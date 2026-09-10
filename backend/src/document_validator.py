class ComplianceChecker:
    """
    Deterministic rule-based document validation checker for AI document intelligence workflows.
    Checks for mentions of required sections, approvals, and supporting references.
    """

    CHECKLIST = {
        "document_authority": ["author", "prepared by", "submitted by", "issued by"],
        "revision_history": ["revision", "version", "updated on", "date changed"],
        "approval_signature": ["approved by", "signature", "signed", "authorized"],
        "reference_citations": ["citation", "reference", "source", "excerpt"],
        "key_clauses": ["clause", "section", "article", "provision"],
        "mandatory_metadata": ["date", "title", "document id", "classification"],
        "action_items": ["action item", "next step", "recommendation", "follow-up"],
        "risk_notes": ["risk", "concern", "exception", "limitation"]
    }

    def check(self, text: str):
        text_lower = text.lower()
        results = {}

        for requirement, keywords in self.CHECKLIST.items():
            found = any(kw in text_lower for kw in keywords)
            results[requirement] = {
                "present": found,
                "status": "FOUND" if found else "MISSING"
            }

        total = len(results)
        found_count = sum(1 for r in results.values() if r["present"])
        compliance_score = round((found_count / total) * 100, 1)

        return {
            "checks": results,
            "validation_score": compliance_score,
            "risk_level": "HIGH" if compliance_score < 50 else "MEDIUM" if compliance_score < 75 else "LOW"
        }