# Ad Storyboard Design Agent

This project implements an **Ad Storyboard Design Agent** using **LangGraph** and **LLM prompting**. It follows a defined process of collecting user inputs, generating an Ad Concept, and creating a scene-wise storyboard.

The process is human-in-the-loop (HITL), where user validation is required at several stages, and retries are implemented for refining the outputs. **Backtracking** and a **supervisor node** are used to handle retries and enable the user to go back to earlier steps when necessary.

## Table of Contents

- [Features](#features)
- [Flow Overview](#flow-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Graph Flow Visualization](#graph-flow-visualization)
- [File Descriptions](#file-descriptions)

## Features

- **Ad Concept Generation:** Uses LLMs to generate Ad Concepts based on user input.
- **Storyboard Generation:** Automatically generates a scene-wise storyboard based on the Ad Duration.
- **Human-in-the-Loop (HITL):** User validation at multiple stages.
- **Backtracking & Retry:** Allows user feedback and retries if a step fails, and users can backtrack to earlier steps.
- **Supervisor Nodes:** Supervisors manage flow control and check the success of each step.
- **Graph Flow Rendering:** Visual representation of the LangGraph flow.

## Flow Overview

The Ad Storyboard Design Agent works through the following steps:

1. **Collect User Input:**
   - Ask the user for Ad Duration (0-60 seconds), Ad Channel (Facebook, Instagram, TikTok), and Ad Theme (50-word description).
   - Validate the inputs using Pydantic.

2. **Generate Ad Concept:**
   - Trigger an LLM (like GPT-4) to generate an Ad Concept based on the user’s inputs.

3. **Validate Ad Concept:**
   - Present the Ad Concept to the user for validation.
   - If the user rejects the concept, allow retry or backtrack to the input collection.

4. **Generate Storyboard:**
   - Use the Ad Concept and Ad Duration to generate a storyboard, with multiple scenes based on the Ad Duration.

5. **Validate Storyboard:**
   - Present the storyboard to the user for validation.
   - Allow feedback and iteration.

6. **Supervisors & Backtracking:** At each key point, a supervisor node will allow users to retry or backtrack.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd ad-storyboard-agent


## Graph Visualisation
1. Use GraphViz
- On Ubuntu
```
sudo apt-get install graphviz
```

- On MacOS using Homebrew
```
brew install graphviz
```

2. Generate images
```
python src/render_graph.py
```