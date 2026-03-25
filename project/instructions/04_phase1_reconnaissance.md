# Phase 1: Reconnaissance

Before attacking, you need to understand the systems you're testing.

## Step 1: Review the Model Architecture

Open `classifier/model.py` and study the ReceiptCNN:

- How many convolutional layers does it have?
- What is the input size and output type?
- Does it use any regularization (dropout, batch norm)?
- How many trainable parameters does it have?

Understanding the architecture is critical for the FGSM attack — you need to know how gradients flow through the network.

## Step 2: Review the Training Pipeline

Read `classifier/train.py` and `classifier/data.py`:

- What loss function is used? (This matters for FGSM)
- What data augmentation is applied?
- How is the dataset structured (folder layout)?

## Step 3: Review the RAG Chatbot

Read `rag_chatbot/rag.py`:

- What is the system prompt? What restrictions does it set?
- How are retrieved chunks passed to the LLM?
- Are source document names visible to the LLM?

Read the policy documents in `rag_chatbot/data/policies/`:

- What documents are indexed?
- Which one contains sensitive information?
- What specific data could be exfiltrated?

## Step 4: Review the Dockerfile

Open `Dockerfile` and look for:

- What base image is used? Is it pinned?
- Does the container run as root?
- What tools are installed but may not be needed at runtime?
- Does `COPY .` risk exposing secrets?

## Step 5: Write Your Red Team Charter

Using the template in `docs/charter_template.md`, write your Red Team Charter. Include:

1. **Engagement details** — Name, date, your role
2. **Objectives** — List each of the 5 attack vectors and what you aim to demonstrate
3. **Scope** — In-scope systems (classifier, chatbot, infra) and out-of-scope items
4. **Rules of engagement** — Ethical constraints (isolated environment, no production impact)
5. **Success criteria** — Measurable goals for each attack
6. **Deliverables** — List all documentation you will produce
