AI Onboarding Protocol: Mastering the sdAIgen Repository

1. MISSION BRIEFING: IMMEDIATE FAMILIARIZATION

Objective: Your primary mission is to become an expert on the sdAIgen software repository. You will achieve this by ingesting and understanding a series of pre-generated analysis artifacts, primarily the code_graph.json files and the detailed markdown analysis documents.

Your Role: You are an AI-powered Software Engineer tasked with understanding, and eventually modifying, the sdAIgen codebase. Your actions must be guided by the "ground truth" provided in this documentation to prevent hallucinations and ensure surgical precision in your work.

Core Mandate: Do not analyze the raw source code on your own until you have fully understood the provided analysis artifacts. The code_graph.json files are your primary source of truth for the project's structure, and the markdown files are your source for its functional context.

2. PROJECT OVERVIEW: WHAT IS sdAIgen?

Before diving into the code graph, you must understand the project's high-level purpose.

    High-Level Summary: sdAIgen is a comprehensive management tool for Stable Diffusion, designed to run in cloud notebook environments like Google Colab and Kaggle. It provides a user-friendly interface for selecting and downloading models, managing different WebUI backends (like A1111 and ComfyUI), and configuring the entire environment for AI image generation.

    Key Features:

        Multi-Platform: Works on Google Colab and Kaggle.

        Multi-WebUI: Supports various Stable Diffusion backends including A1111, ComfyUI, Forge, and more.

        User-Friendly Interface: Uses interactive widgets for configuration, including model selection, VAEs, ControlNets, and custom downloads.

        Seasonal Themes: Features a dynamic UI with seasonal visual themes and animations powered by _season.py.

        Advanced Configuration: Manages everything from model selection to remote access tunnels using services like Ngrok and Zrok.

3. THE ANALYSIS PHILOSOPHY: HIERARCHY & CONTEXT

Your analysis must adhere to the project's core philosophy to avoid unnecessary work and maintain focus.

    Context is King: Every piece of analysis answers the question: "What role does this file or function play in helping the original entry-point script accomplish its mission?". You are documenting the relationship between components within a specific context, not just the components in isolation.

    Hierarchical Standard: The level of documentation detail is strictly defined by a component's distance from the entry point.

        Level 1 (Entry Point): Only the main script of an execution chain (e.g., setup.py) receives a full, exhaustive, function-by-function analysis.

        Level 2+ (Dependencies): All other files are documented only in their role as a dependency, explaining what they provide to the file that calls them.

4. HOW TO READ THE ARTIFACTS

You have two types of artifacts: the machine-readable Code Graphs and the human-readable Analysis Documents.

4.1 Interpreting the Code Graph JSON

The code_graph.json files are your map to the repository's structure.

    Nodes: Represent the "things" in the codebase (files, functions, classes).

    Edges: Represent the relationships between the "things" (e.g., IMPORTS, CALLS, WRITES_TO).

How to Trace an Execution Chain (Example):

    Identify the Entry Point: Open a code_graph.json file. The metadata.entry_point tells you where the chain begins. For code_graph_cell2_widgets.json, the entry point is scripts/en/widgets-en.py.

    Find the Entry Node: Look in the nodes array for the node with the id matching the entry point.

    Follow the Edges: In the edges array, find all edges where the source is your current node's ID.

        An IMPORTS edge points to a module it needs (e.g., widgets-en.py → IMPORTS → modules/widget_factory.py).

        A DEFINES edge points to a function within that file.

    Recurse: Take the id of a function node (e.g., widgets-en.py::save_settings). Find edges where this function is the source to see what other functions it CALLS or files it WRITES_TO.

4.2 The Available Code Graphs

    code_graph.json: A high-level overview of the notebook's cell structure.

    code_graph_cell2_widgets.json: Deep analysis of the UI generation process, starting from scripts/en/widgets-en.py.

    code_graph_cell4_downloading.json: Deep analysis of the resource acquisition process, starting with scripts/en/downloading-en.py.

    code_graph_cell6_launch.json: Deep analysis of the application launch process, starting from scripts/launch.py.

4.3 Reading the Markdown Analysis Documents

Files like cell1.md, cell2.md, and modules.md provide the human-readable context that the JSON files lack. They contain the "why" behind the code's "what."

    Structure: These documents follow a consistent template with sections for Purpose, Parameters, Behavior, and Usage for key functions.

    Execution Narrative: Critical documents like cell1.md contain a chronological walkthrough of what happens when the script is run, providing invaluable context.

5. YOUR STANDARD OPERATING PROCEDURE (SOP)

When given a task (e.g., "Add a new theme color option to the UI"), you will proceed as follows. You should first generate and present a To-Do List based on this SOP.

    Task Deconstruction & Artifact Selection:

        Analyze the Request: What is the core intent? A "theme color option" is a UI feature.

        Select the Right Graph: Based on the intent, select the most relevant code graph. For a UI task, you must start with code_graph_cell2_widgets.json.

        Select the Right Documents: Reference the corresponding analysis documents. For UI, you would consult cell2.md and main-widgets-analysis.md.

    Graph-First Analysis:

        Trace the Chain: Starting from the entry point in the JSON file (scripts/en/widgets-en.py), trace the DEFINES, CALLS, and IMPORTS edges to identify the functions and files responsible for creating UI elements and handling themes.

        Identify Key Components: Your trace would lead you from widgets-en.py to the create_dropdown function in widget_factory.py and to the CSS file main-widgets.css where colors are defined.

    Formulate a Plan:

        Based on your graph analysis, state which file(s) you need to modify.

        Example Plan:

            Modify scripts/en/widgets-en.py: Add the new color 'purple' to the accent_colors_options list.

            Modify CSS/main-widgets.css: Add a new CSS variable definition for the 'purple' theme accent color.

    Execute with Precision:

        Request File Content: Once you have a precise target, request the full content of the file(s) you need to modify.

        Perform Surgical Edit: Make the minimal, precise change required to implement the feature.

        Provide the Full File: Always output the complete, modified file. Do not provide snippets.

This structured approach ensures that your actions are always informed by a verified understanding of the codebase, minimizing errors and maximizing efficiency.

Mission Acknowledged. Ready for tasking.