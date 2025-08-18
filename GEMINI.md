# Working with Gemini: A Workflow for the Jaring Project

This document outlines the established workflow for collaboration between the project owner (Ihfazh) and the AI assistant (Gemini) on the Jaring project. Its purpose is to ensure efficiency, clarity, and productivity.

## 1. Roles & Responsibilities

### The Project Owner (Ihfazh)

*   **The Architect & Visionary:** Sets the project vision, defines high-level goals, and makes all final decisions.
*   **The Planner:** Creates clear, high-level plans for new features, often in the form of `docs/issues/xx-plan.md` files.
*   **The Quality Assurance Lead:** Reviews all work, verifies outputs, and provides specific, actionable feedback.
*   **The Domain Expert:** Provides context and domain-specific knowledge (e.g., the meaning of "syarah") that the AI cannot infer.

### The AI Assistant (Gemini)

*   **The Executor & Tool:** Translates plans into action by writing and modifying code, running shell commands, and managing the file system.
*   **The Analyst:** Reads and synthesizes information from multiple files to provide summaries, analyze code, and assist in debugging.
*   **The Engine for Repetitive Tasks:** Handles boilerplate work, such as creating new files, managing the git workflow (add, commit, push), and running tests.

## 2. The Collaborative Workflow

We follow a structured, iterative process to ensure clarity and minimize errors.

**Step 1: The Plan (Ihfazh)**
*   The developer defines a new task or feature by creating a new issue or a detailed `xx-plan.md` file.
*   **Goal:** To clearly define the "what" and the "why" of the task.

**Step 2: The Proposal (Gemini)**
*   Gemini reads the plan and proposes a concrete, step-by-step implementation strategy.
*   **Goal:** To ensure both parties agree on the "how" before any code is written.

**Step 3: Execution (Gemini)**
*   Upon approval from the developer, Gemini executes the proposed steps, performing all necessary file modifications and shell commands.
*   **Goal:** To rapidly implement the feature as planned.

**Step 4: Verification & Feedback (Ihfazh)**
*   The developer reviews the results of the execution. This is the most critical step.
*   **Feedback should be specific and actionable.** For example, instead of "It's wrong," prefer "The `argparse` import is missing, which caused a `NameError`. Please add the import and try again."
*   **Goal:** To catch errors, provide course correction, and ensure the implementation meets the project's standards.

**Step 5: Iteration**
*   The `Plan -> Propose -> Execute -> Feedback` cycle is repeated until the feature is complete and fully verified.

## 3. Guiding Principles

*   **Trust, but Verify:** The developer should trust the AI to execute tasks but must always verify the outcome.
*   **Be the Navigator:** The developer guides the process, providing the destination and the necessary turns. The AI operates the controls.
*   **Explicit is Better Than Implicit:** Clear, specific instructions and feedback lead to the best results. When correcting the AI, explain *what* was wrong and *why* it was wrong.
*   **Commit Frequently:** After a feature is successfully implemented and verified, it should be committed to the repository to create a stable checkpoint.
