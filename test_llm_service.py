from service.llm_service import LLMService

def test_llm_generate_content():
    llm_service = LLMService()
    test_prompt = "What is the capital of India?"
    print(f"Testing LLM with prompt: {test_prompt}")
    response = llm_service.generate_content(test_prompt)
    print(f"LLM Response: {response}")

if __name__ == "__main__":
    test_llm_generate_content()
