# Ad Project: Subgraphs with Retry and Supervisor Logic

This project demonstrates a LangGraph-based workflow with retry loops in subgraphs, backtracking logic, and a supervisor node that ensures consistency across steps.

## Workflow Overview

The workflow consists of three main steps, each running a subgraph that can retry tasks in case of failure. A supervisor checks the consistency of each step, and if inconsistencies are found, the workflow backtracks to reprocess the relevant step.

### Main Graph
```mermaid
graph TD
    A[START] --> B[Step 1: Run Subgraph]
    B --> C[Supervisor Check]
    C -->|Consistent| D[Step 2: Run Subgraph]
    C -->|Inconsistent| B[Backtrack to Step 1]
    D --> E[Supervisor Check]
    E -->|Consistent| F[Step 3: Run Subgraph]
    E -->|Inconsistent| D[Backtrack to Step 2]
    F --> G[Supervisor Check]
    G -->|Consistent| H[END]
    G -->|Inconsistent| F[Backtrack to Step 3]
```

# Subgaph with Retry Logic  
```mermaid
graph TD
    S1[Start Subgraph] --> T1[Task Step]
    T1 -->|Success| S2[Next Step]
    T1 -->|Failure| R1[Retry Logic]
    R1 -->|Retries Left| T1[Retry Task]
    R1 -->|Max Retries Reached| S2[Proceed]
    S2 --> S3[End Subgraph]
```

## Supervisor and Backtracking Logic

```
graph TD
    S1[Supervisor Node] --> C1[Check Consistency]
    C1 -->|Inconsistent| B1[Backtrack to Previous Step]
    C1 -->|Consistent| N1[Proceed to Next Step]
```