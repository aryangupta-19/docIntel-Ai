from src.llm_engine import LLMEngine
from src.vectorstore import ReportVectorStore


class AgentPanel:
    def __init__(self):
        self.llm = LLMEngine()
        self.store = ReportVectorStore()


    # retrieval
    


    def _retrieve(self, query: str, report_id: str, top_k: int =4):
        results = self.store.query(query, report_id, top_k = top_k)
        docs= results.get("documents", [[]])[0]
        return "\n\n".join(docs)
        # retieval
    


    def executive_summary_agent(self, report_id: str, full_text: str):
        context = self._retrieve("executive summary key overview document purpose main findings", report_id)
        prompt = f"""You are an expert document intelligence analyst.
Summarize the provided document content for a broad audience.
Focus on the main purpose, key themes, critical findings, and any notable gaps.
Keep the summary concise, structured, and suitable for legal, business, technical, or academic documents.

Document Sections:
{context}"""
        return self.llm.chat(system_prompt=prompt, user_message="Provide an executive summary.")

    def semantic_search_agent(self, report_id: str, full_text: str):
        context = self._retrieve("question answer relevant evidence document content", report_id)
        prompt = f"""You are a semantic retrieval specialist.
Answer the user's question using only the retrieved document sections below.
If information is not present, say so clearly and avoid hallucinating.
Be precise and reference the content directly.

Document Sections:
{context}"""
        return self.llm.chat(system_prompt=prompt, user_message="Answer the document question using the provided context.")

    def citation_agent(self, report_id: str, full_text: str):
        context = self._retrieve("supporting evidence citation page references source snippet", report_id)
        prompt = f"""You are a citation and evidence extraction specialist.
Identify supporting evidence from the retrieved document sections.
Return the most relevant quotes, excerpts, or snippets and any available page or section references.
If references are unavailable, state that clearly.

Document Sections:
{context}"""
        return self.llm.chat(system_prompt=prompt, user_message="Extract supporting citations and evidence.")

    def key_insights_agent(self, report_id: str, full_text: str):
        context = self._retrieve("important findings risks action items recommendations insights", report_id)
        prompt = f"""You are a document insights analyst.
Extract the most important findings, risks, action items, and recommendations from the document content.
Group the output into clear categories and keep it concise.

Document Sections:
{context}"""
        return self.llm.chat(system_prompt=prompt, user_message="Extract key insights and recommendations.")

    def document_compliance_agent(self, report_id: str, full_text: str):
        context = self._retrieve("required sections signatures dates clauses mandatory information compliance", report_id)
        prompt = f"""You are a document compliance analyst.
Review the document content for missing mandatory sections, signatures, dates, clauses, or required information.
Flag omissions clearly and distinguish between present and missing items.

Document Sections:
{context}"""
        return self.llm.chat(system_prompt=prompt, user_message="Assess document compliance and missing requirements.")

    def annotation_agent(self, report_id: str, full_text: str):
        context = self._retrieve("important passage notable section key clause significant statement", report_id)
        prompt = f"""You are a document annotation specialist.
Identify important portions of the document that should be highlighted for downstream review.
Describe why each passage is significant and categorize it appropriately.

Document Sections:
{context}"""
        return self.llm.chat(system_prompt=prompt, user_message="Generate annotations for important document content.")

    def response_composer(self, assessments: dict):
        summary = "\n\n".join([f"{k.upper()}:\n{v}" for k, v in assessments.items()])
        prompt = f"""You are the lead document intelligence reviewer.
Synthesize the outputs from the specialist agents into a structured response.
Produce:
1. A concise overall summary
2. The most relevant findings
3. Priority actions or recommendations
4. Any notable compliance concerns

Agent Assessments:
{summary}"""
        return self.llm.chat(system_prompt=prompt, user_message="Compose the final document intelligence response.")

    def run(self, report_id: str, full_text: str):
        assessments = {
            "executive_summary": self.executive_summary_agent(report_id, full_text),
            "semantic_search": self.semantic_search_agent(report_id, full_text),
            "citation": self.citation_agent(report_id, full_text),
            "key_insights": self.key_insights_agent(report_id, full_text),
            "document_compliance": self.document_compliance_agent(report_id, full_text),
            "annotation": self.annotation_agent(report_id, full_text),
        }
        assessments["response_composer"] = self.response_composer(assessments)
        return assessments
    
