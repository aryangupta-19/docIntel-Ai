from src.llm_engine import LLMEngine

llm = LLMEngine()
response = llm.chat(
    system_prompt = "You are a document intelligence analyst.",
    user_message="In one sentence, what is the main insight in this document?"
)

print(response)
