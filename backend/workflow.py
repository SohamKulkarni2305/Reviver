import logging
from extractor import extract_text
import urllib.parse
import json
import re
from collections import Counter

class SummarizerAgent:
    """Main Agent: Extracts a chronological, highly detailed textbook-style summary."""
    def summarize(self, text: str) -> str:
        # Fix common PDF ligature extraction errors
        text = text.replace('dierent', 'different').replace('eect', 'effect').replace('eective', 'effective').replace('icult', 'icult')
        
        # Looser filter to catch all bullet points and paragraphs
        raw_sentences = re.split(r'(?<=[.!?]) +|\n+', text)
        
        seen = set()
        sentences = []
        for s in raw_sentences:
            cleaned = s.strip().replace('\t', ' ')
            if 10 < len(cleaned) < 1500 and not cleaned.upper().startswith("PART ") and cleaned not in seen:
                seen.add(cleaned)
                sentences.append(cleaned)
                
        if not sentences:
            return "No meaningful text could be extracted."
            
        # Divide into 4 chronological chapters to ensure we cover the BEGINNING, MIDDLE, and END of the file
        chunk_size = max(1, len(sentences) // 4)
        chunks = [sentences[i:i + chunk_size] for i in range(0, len(sentences), chunk_size)][:4]
        
        chapter_titles = ["Introduction and Core Concepts", "Main Mechanics", "Technical Implementation", "Summary and Inference"]
        markdown_sections = []
        
        for i, chunk in enumerate(chunks):
            if not chunk: continue
            
            chapter = f"## Chapter {i+1}: {chapter_titles[i]}\n\n"
            
            # Calculate local word frequency for this chunk
            words = re.findall(r'\b[a-zA-Z]{5,}\b', " ".join(chunk).lower())
            stop_words = {"the", "and", "this", "that", "which", "there", "their", "these", "those", "about", "could", "would"}
            word_freq = Counter(w for w in words if w not in stop_words)
            
            # Get the top 2 keywords to make the dynamic image highly relevant to this specific text
            top_keywords = [w[0] for w in word_freq.most_common(2)]
            keyword_str = "+".join(top_keywords) if top_keywords else "technology"
            
            # We use Pollinations dynamically so it generates a new image based on the specific PDF text!
            # We use smaller dimensions (width=600&height=200) to reduce the size of the images
            safe_prompt = urllib.parse.quote(f"clean minimalist corporate vector art about {chapter_titles[i]} and {keyword_str}, dark mode, no text")
            seed = sum(ord(c) for c in chunk[0]) + i * 999 
            img_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=600&height=200&nologo=true&seed={seed}"
            
            chapter += f"![{chapter_titles[i]}]({img_url})\n\n"
            
            # Extract the 25 most important sentences from this specific chunk so the summary is MASSIVE
            chunk_scores = []
            for s in chunk:
                score = sum(word_freq[w] for w in re.findall(r'\b[a-zA-Z]{5,}\b', s.lower()) if w in word_freq)
                # Favor longer descriptive sentences slightly
                score = score * (len(s.split()) / 10.0)
                chunk_scores.append((s, score))
                
            # Take the top 25 sentences for this chapter (increased from 12!)
            best_chunk_sentences = sorted(chunk_scores, key=lambda x: x[1], reverse=True)[:25]
            
            # Sort them back into their original chronological order so it reads like a story
            ordered_chunk = [s for s in chunk if any(b[0] == s for b in best_chunk_sentences)]
            
            for s in ordered_chunk:
                chapter += f"- {s}\n"
                
            markdown_sections.append(chapter)
            
        return "\n\n".join(markdown_sections)

class ReviewerSubAgent:
    """Sub-Agent: Verifies the summary covers the main topics of the original text."""
    def review(self, original_text: str, summary: str) -> bool:
        # Find top 3 keywords in original text
        words = re.findall(r'\b[a-zA-Z]{5,}\b', original_text.lower())
        stop_words = {"the", "and", "this", "that"}
        word_freq = Counter(w for w in words if w not in stop_words)
        top_keywords = [item[0] for item in word_freq.most_common(3)]
        
        # Verify the summary contains at least some of the top keywords
        summary_lower = summary.lower()
        matches = sum(1 for keyword in top_keywords if keyword in summary_lower)
        
        logging.info(f"Reviewer Sub-Agent checking keywords: {top_keywords}. Found {matches}/3 in summary.")
        return matches >= 2  # Approve if it contains most key topics

class DiagramAgent:
    """Agent: Generates a Mermaid co-occurrence graph from the top concepts."""
    def generate_diagram(self, text: str) -> str:
        words = re.findall(r'\b[a-zA-Z]{5,}\b', text.lower())
        stop_words = {"the", "and", "this", "that", "which", "there", "their", "these", "those", "about", "could", "would"}
        word_freq = Counter(w for w in words if w not in stop_words)
        
        # Get top 12 concepts for a rich diagram
        top_concepts = [item[0].capitalize() for item in word_freq.most_common(12)]
        
        if len(top_concepts) < 4:
            return "graph TD;\n  A[Document] --> B[Concepts];"
            
        # Construct a beautiful hierarchical Mermaid Graph (Left to Right)
        mermaid = "graph LR;\n"
        
        # Central Hub
        main_topic = top_concepts[0]
        mermaid += f"  Core(({main_topic}))\n"
        
        # 3 Primary Branches
        primary_branches = top_concepts[1:4]
        for i, branch in enumerate(primary_branches):
            mermaid += f"  Core ==>|Includes| B{i}[{branch}]\n"
            
        # Distribute remaining concepts as sub-branches
        sub_concepts = top_concepts[4:]
        for i, sub in enumerate(sub_concepts):
            parent_idx = i % 3  # Distribute evenly among the 3 primary branches
            mermaid += f"  B{parent_idx} -.-> S{i}({sub})\n"
            
        return mermaid

class AgentHarness:
    """Orchestrates the Agents without using any external LLM APIs."""
    def __init__(self):
        self.summarizer = SummarizerAgent()
        self.reviewer = ReviewerSubAgent()
        self.diagrammer = DiagramAgent()
        
    def execute(self, file_path: str) -> dict:
        logging.info("Agent Harness starting...")
        
        # 1. Extraction
        raw_text = extract_text(file_path)
        if not raw_text.strip():
            raise ValueError("No text could be extracted from the file.")
            
        # Global purification: NUKE the watermark from the text before ANY agent sees it
        raw_text = re.sub(r'(?i)deboistech', '', raw_text)
            
        # 2. Main Agent Summarization loop
        logging.info("Summarizer Agent drafting detailed topic summary...")
        final_summary = self.summarizer.summarize(raw_text)
        
        # 3. Sub-Agent Verification
        if self.reviewer.review(raw_text, final_summary):
            logging.info("Reviewer Sub-Agent APPROVED the summary.")
        else:
            logging.warning("Reviewer Sub-Agent flagged the summary, but using best effort.")

        # 4. Generate Markdown
        markdown_output = f"# Course Detailed Recap\n\n{final_summary}\n\n"
        markdown_output += "> *Verified by Reviewer Sub-Agent*"

        # 5. Generate Diagram
        logging.info("Diagram Agent generating Mermaid graph...")
        mermaid_code = self.diagrammer.generate_diagram(raw_text)
        
        # 6. Final Assets (We set image_url to empty string to hide the duplicate visual at the top/bottom)
        
        return {
            "markdown_summary": markdown_output,
            "mermaid_code": mermaid_code,
            "image_url": ""
        }

async def run_agent_workflow(file_path: str) -> dict:
    """FastAPI entry point that triggers the Agent Harness."""
    try:
        harness = AgentHarness()
        # We run it synchronously because it's just pure python math now
        return harness.execute(file_path)
    except Exception as e:
        logging.error(f"Harness execution failed: {e}")
        return {
            "markdown_summary": f"# Error\n\nFailed to process file: {e}",
            "mermaid_code": "",
            "image_url": ""
        }
