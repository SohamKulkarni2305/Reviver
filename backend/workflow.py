import logging
from backend.extractor import extract_text

def run_agent_workflow(file_path: str) -> dict:
    """
    Orchestrates the entire agent workflow:
    1. Extracts text from PDF
    2. Main Agent summarizes
    3. Sub-Agent reviews
    4. Canva MCP generates image
    """
    logging.info("Starting agent workflow...")
    
    # Step 1: Extract Text
    raw_text = extract_text(file_path)
    logging.info("Text extraction complete.")
    
    # Step 2: Main Agent Summarizes (Mocked for this implementation plan)
    # In a real app, this calls the LLM API
    logging.info("Main Agent summarizing text...")
    markdown_summary = f"# Course Recap\n\nBased on the extracted text:\n{raw_text}\n\n- Key Point 1\n- Key Point 2"
    
    # Step 3: Sub-Agent Reviews (Mocked)
    logging.info("Sub-Agent verifying summary against original text...")
    # Simulate sub-agent appending a verified stamp
    markdown_summary += "\n\n> **Sub-Agent Review:** Verified accurate against original text."
    
    # Step 4: Canva MCP Integration (Mocked)
    logging.info("Calling Canva MCP Server to generate diagram...")
    image_url = "https://www.canva.com/design/dummy-diagram/view"
    
    logging.info("Agent workflow complete.")
    
    return {
        "markdown_summary": markdown_summary,
        "image_url": image_url
    }
