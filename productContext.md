# Product Context: Sentiment Discrepancy Analysis for WeLoveReviews

## Business Background
WeLoveReviews is a data consultancy that helps corporate clients decode what their customers truly think. They have recently onboarded a new high-stakes account: a service-based business boasting an impressive average rating of 4.5 out of 5 stars. 

While the numbers look excellent on paper, the account manager harbors a nagging doubt: does the qualitative sentiment written in the text reviews genuinely reflect that near-perfect quantitative score? Before presenting the final performance report to the client, the account manager needs a data-driven second opinion to confirm whether a sentiment gap exists based on concrete data rather than a gut feeling.

## User Persona & Goals
* **Primary User:** Account Manager at WeLoveReviews.
* **Goal:** Present an honest, accurate, and deeply insightful breakdown of 500 written customer reviews to their client next week.
* **Core Questions to Answer:**
  * In plain terms, how many of the 500 reviews read as Positive, Neutral, or Negative?
  * Does this qualitative sentiment percentage breakdown mathematically align with the business's 4.5-star average rating?
  * If a discrepancy or gap exists, what is its root cause, and where exactly is it coming from?

## Technical Challenges & Domain Mismatch
1. **No Cold Starts:** The project timeline does not allow for collecting vast training datasets, tuning hyperparameters, or training a custom model from scratch. An existing pretrained model from the Hugging Face ecosystem must be correctly integrated.
2. **The Product vs. Service Gap:** The designated model (`nlptown/bert-base-multilingual-uncased-sentiment`) was fine-tuned exclusively on product reviews (such as Amazon-style product ratings). The client’s dataset consists entirely of *service reviews*, where customers focus heavily on human interactions, staff friendliness, wait times, and physical ambiance. 
3. **The False Negative Risk & Hypotheses:** This structural domain mismatch is highly likely to trigger false negatives—situations where a human reader (or a high original star rating) flags a review as positive, but the product-tuned model classifies it as low sentiment due to unfamiliar service-oriented vocabulary. Identifying, quantifying, analyzing, and documenting patterns for this gap with clear hypotheses is a core delivery requirement.

## Operational Workflow & Team Communication Style
On this team, leadership explicitly treats Jupyter notebooks as permanent, standalone communication documents for data-processing and analytics work—not throwaway scratchpads. The notebook is your sole communication artifact; no separate client markdown report is expected or evaluated.
* **The PROMPT.md Protocol:** Initial data profiling is kicked off using a predefined prompt sequence located in `PROMPT.md`.
* **Agent-Assisted Co-Pilot:** A coding agent (e.g., Cursor, Copilot, Claude Code) is introduced exclusively to scaffold the Exploratory Data Analysis (EDA), surface initial insights, and outline a data cleaning proposal inside the notebook.
* **Human-in-the-Loop Hand-off:** Once the agent completes the EDA boundaries, the project transitions entirely to the engineer to execute the core model analysis, manual sanity-checking, and script production migration following the team's pattern: **"notebook for story, script for production."**
