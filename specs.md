# Technical Specification: Pretrained Sentiment Pipeline & Validation

## 1. Project Setup & Ingestion Specifications
* **Raw Data Location:** Download the provided `reviews.csv` file from the platform and place it precisely in `data/raw/reviews.csv` within your repository.
* **Environment Configuration:** If starting a coding project is new to you, read the platform's comprehensive project-start setup guide.
* **Dependency Management:** Extend the `requirements.txt` file with `transformers` and `torch` (or your chosen hardware acceleration backend). Every dependency **must** be explicitly version-pinned for reproducibility.

## 2. Model Pipeline Architecture & Integration Rules
* **Model Designation:** `nlptown/bert-base-multilingual-uncased-sentiment` from Hugging Face.
* **Loading Rule:** Must be integrated via the Hugging Face `pipeline()` abstraction or direct `from_pretrained()` classes.
* **Repo Compliance:** Model weights must **never** be committed directly to the git repository.
* **Inference Loop Rule:** The model and tokenizer must be loaded **once** outside and before starting the execution loop. Re-loading or re-instantiating the model inside a per-review loop is strictly prohibited due to critical memory leaks and latency degradation.
* **Version Control Pinning:** The exact model version or revision name must be pinned hard in code, not left to resolve implicitly to `"latest"`.

## 3. Sentiment Banding Rules
The selected model outputs discrete integer star ratings from 1 to 5. These predictions must be programmatically transformed into three distinct sentiment bands:

| Model Star Prediction | Assigned Sentiment Band |
| :--- | :--- |
| 1–2 Stars | Negative |
| 3 Stars | Neutral |
| 4–5 Stars | Positive |

## 4. Coding Agent Collaboration Boundaries (EDA Phase)
* **Instruction Execution:** Open `PROMPT.md` in the project directory, copy all contents *below* the header line, and paste it into your coding agent workspace.
* **Agent Boundaries:** Allow the agent to operate exclusively within the designated EDA section of `src/explore.ipynb`. This must cover exploration, visual distribution insights, and a cleaning proposal. 
* **The Hand-off Line:** The agent prompt terminates at the conclusion of the EDA section. All subsequent evaluation items listed below must be completed manually by the engineer.

## 5. Required Deliverables & Evaluation Criteria

### A. Narrative Code Artifact (`src/explore.ipynb`)
A fully executed Jupyter notebook displaying all runtime outputs. It must follow a strict, chronological arc using short transitional markdown text blocks sandwiched between major code cells to guide the reader:
1. **Objectives:** Frame the business question directly (Written sentiment analysis vs. the client's 4.5-star average score).
2. **EDA / Insights / Cleaning:** Incorporate the coding agent's prompt output with conversational descriptions of the distributions.
3. **Action Plan & Model Rationale:** Justify your next engineering choices from your insights; explicitly commit to using the designated `nlptown` model and banding constraints.
4. **Inference Pipeline:** Process all 500 reviews efficiently, saving both the raw predicted stars and final sentiment bands per review entry.
5. **Breakdown vs. 4.5-Star Average:** Mathematically compute the percentage split of Positive, Neutral, and Negative entries. Directly compare these figures against the business's nominal rating to explicitly point out discrepancies.
6. **Manual Sanity-Checking Sample:** Hand-inspect a representative sample of **15–20 reviews**. Document specific cases where predictions look correct or wrong, ensuring visible evidence of analytical validation.
7. **False Negatives Identification:** Isolate and flag reviews where the model predicts 1–2 stars but the human rating is 4–5 stars (or where human intuition reads the text as positive/neutral but the model disagrees). Document specific examples and note shared textual patterns (e.g., words like "wait time", "staff").
8. **Conclusions:** Deliver plain-language, actionable takeaways that the account manager can confidently present to the client.

### B. Production Pipeline Artifact (`src/app.py`)
* **Migration Rule:** Clean, verified inference and batch logic must be migrated out of the exploratory workspace into a production-grade script (`src/app.py`).
* **Operational Goal:** The script must run the production inference pipeline on the input dataset and save a clean, enriched data table out to disk.
* **Output Path:** `data/processed/reviews_with_sentiment.csv`

---
*Note: Evaluators are not grading model architecture design, model fine-tuning, or a standalone markdown report. The core evaluation centers on proper API integration, structural data outputs, and the depth of your narrative data investigation within the notebook.*
