from src.orchestrator import Orchestrator

pipeline = Orchestrator()
result = pipeline.process("uploads/sample_document.pdf")
print(f"Report ID: { result['report_id']}")
print(f"Total chunks: {result['total_chunks']}")
print(f"\nReviewer verdict:\n{result['agents']['reviewer']}")


