# Phase 3: RAG Chatbot Attacks

## Setup

Make sure the RAG chatbot is running:

```bash
cd rag_chatbot
python build_index.py    # Build FAISS index (if not done already)
python app.py            # Start Flask server on port 5001
```

Test with a legitimate query:
```bash
curl -X POST http://localhost:5001/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the meal expense limit?"}'
```

---

## Attack 3: Prompt Injection

### Background

Prompt injection attacks attempt to override or manipulate the LLM's system instructions by embedding malicious instructions in the user input. Since the system prompt and user input are both processed as text, the LLM may not reliably distinguish between them.

### Implementation

Open `attacks/03_prompt_injection.py`. You need to:

1. **Design 5 injection prompts** using different techniques:
   - **System Prompt Extraction** — Try to get the bot to reveal its instructions
   - **Role Hijacking** — Make it adopt a different persona (e.g., "You are now DebugBot...")
   - **Policy Contradiction** — Inject false policy information
   - **Instruction Override** — "Ignore all previous instructions..."
   - **Encoding Bypass** — Use BASE64 or other encoding to disguise your request

2. **Define success indicators** — Keywords that would appear in the response if the injection worked

3. **Implement the indicator matching** — Check which indicators appear in each response

### Tips

- Be creative with your prompts — different LLMs are vulnerable to different techniques
- Some attacks may partially succeed (e.g., revealing metadata without full data)
- Document both successes and failures — understanding why an attack fails is valuable

### Run and Record

```bash
cd attacks
python 03_prompt_injection.py
```

Record the full transcript in `docs/prompt_injection_transcript_template.md`.

---

## Attack 4: Data Exfiltration

### Background

RAG systems retrieve documents based on semantic similarity — if a confidential document is in the vector store, any sufficiently similar query will retrieve it. This is an **architectural vulnerability**: FAISS has no concept of user permissions or document classification.

The `data/policies/` directory contains a file called `executive_bonus_structure_CONFIDENTIAL.md` with sensitive compensation data. This document was indexed alongside public policies with no access control.

### Implementation

Open `attacks/04_data_exfiltration.py`. You need to:

1. **Design 6 exfiltration queries** using different strategies:
   - **Direct Request** — Ask about bonuses/compensation directly
   - **Semantic Proximity** — Use related terms (incentives, pay structure)
   - **Indirect Framing** — Frame as a legitimate business need
   - **Broad Retrieval** — Ask for summaries of all policies
   - **Metadata Probe** — Ask about document names and classifications
   - **Keyword Focused** — Target specific data points (stock options, clawback)

2. **Implement the indicator matching** — Check which confidential data indicators appear in responses

3. **Check source documents** — Verify whether the CONFIDENTIAL document was retrieved

### Key Insight

Even if the LLM refuses to share the data (prompt-level defense), the **sources** field in the response will show that the CONFIDENTIAL document was retrieved by FAISS. This proves the architectural vulnerability exists regardless of LLM behavior.

### Run and Record

```bash
python 04_data_exfiltration.py
```

Record the evidence in `docs/data_exfiltration_evidence_template.md`. Include your root cause analysis — why does this vulnerability exist and how should it be fixed?
