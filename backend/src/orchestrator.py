from src.loader import load_and_chunk_report
from src.vectorstore import ReportVectorStore
from src.agents import AgentPanel
import uuid
import os


class Orchestrator:
    """
    Main pipeline coordinator for DocIntel.
    Handles: document loading -> chunking -> storing -> running agents -> returning document intelligence results.
    """

    def __init__(self):
        self.store = ReportVectorStore()
        self.panel = AgentPanel()

    def process(self, pdf_path: str, project_type: str = "business", city_tier: str = "tier_2"):
        """
        Full pipeline from document upload to final document intelligence response.
        Returns structured result with all agent outputs.
        """

        # Step 1: Load and chunk
        chunks = load_and_chunk_report(pdf_path)
        if not chunks:
            return {"error": "Could not extract text from document"}

        # Step 2: Generate a unique document ID
        report_id = str(uuid.uuid4())[:8]

        # Step 3: Store in ChromaDB
        self.store.add_chunks(chunks, report_id=report_id)

        # Step 4: Build full text for deterministic layers
        full_text = " ".join([c.page_content for c in chunks])

        # Step 5: Run agent panel
        results = self.panel.run(report_id, full_text)

        document_type = project_type
        jurisdiction_tier = city_tier

        return {
            "report_id": report_id,
            "project_type": document_type,
            "document_type": document_type,
            "city_tier": jurisdiction_tier,
            "jurisdiction_tier": jurisdiction_tier,
            "total_chunks": len(chunks),
            "agents": results,
        }