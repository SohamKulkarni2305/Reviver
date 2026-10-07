---
name: doc-summarizer
description: Use this skill whenever summarizing a document. It defines the required output format and style rules every summary must follow.
---

# Document Summarizer Skill

## Purpose

Produce a consistent, structured summary of any document fed to you. Follow the format below exactly — no sections may be omitted.

## Workflow

When asked to summarize a document:

1. **Delegate to the Extractor sub-agent** — pass the file path. Receive plain text in return.
   - If the Extractor returns an `ERROR:` message, report it to the user and stop.
2. **Draft a structured summary** using the output format below. Apply all style rules.
3. **Delegate to the Reviewer sub-agent** — pass both the raw source text and the draft summary.
   - If the Reviewer returns `APPROVED`, proceed to step 4.
   - If the Reviewer returns `CORRECTIONS:`, fix each listed issue and resubmit once.
   - If corrections are still returned after one retry, save the summary with a warning header.
4. **Save the final summary** as `<original-filename>.summary.md` in the same directory as the source file.
5. **Report completion** to the user with the path to the saved file.

## Output Format

Every summary you produce MUST use this exact structure:

```markdown
# Summary: <Document Title>
> Summarized from: `<original filename>`

## 🔑 Key Points
- <5–7 bullet points — each must be a fact directly stated in the document>

## 📝 Summary
<Paragraph 1: What the document is about and its main purpose>

<Paragraph 2: Core arguments, findings, or instructions>

<Paragraph 3 (optional): Conclusions, recommendations, or next steps>

## 🏷️ Topics Covered
- <Specific topic 1>
- <Specific topic 2>
- ...

## 📊 Document Stats
- **File Type:** PDF / DOCX / TXT
- **Estimated Length:** X pages or X words
- **Language:** English
```

## Style Rules

- **Key Points** must be traceable to a direct statement in the source — no inferences, no paraphrasing facts not in the document
- **Summary** paragraphs must be written in plain, student-friendly language
- **Topics** must be specific (e.g., "Supervised Learning" not "Machine Learning")
- If something in the document is unclear or ambiguous, say so explicitly — never guess or fill in gaps
- Do NOT invent statistics, names, dates, or claims not present in the source text
- If the Reviewer finds issues and max retries are exhausted, prepend this warning to the saved file:

```markdown
> ⚠️ **Warning:** This summary could not be fully verified. Some points may not be accurately reflected. Please cross-check with the source document.
```
