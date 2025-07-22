"""Flow visualization utilities for Breeze."""

from typing import Dict, List, Any, Optional


def generate_mermaid_diagram(flow_data: Dict[str, Any]) -> str:
    """Generate a Mermaid flowchart diagram from flow data."""
    
    diagram = """flowchart TD
    %% User Interaction
    subgraph User["User"]
        U1["CLI / Chat Input"]
        U2["CLI / Chat Output"]
    end

    %% CLI Entrypoint
    subgraph Entrypoint["Entrypoint Layer"]
        M1["main.py\\n(Argparse, Entrypoint)"]
        M2["__main__.py\\n(Python -m Entrypoint)"]
    end

    %% Flow Orchestration
    subgraph Flow["Flow & Orchestration"]
        F1["flow.py\\n(Flow Logic)"]
        F2["nodes.py\\n(Agent Nodes)"]
    end

    %% Node Types
    subgraph Nodes["Agent Nodes"]
        N1["DocAgentNode"]
        N2["SummaryAgentNode"]
        N3["TestGenerationAgentNode"]
        N4["BugDetectionAgentNode"]
        N5["RefactorCodeAgentNode"]
        N6["TypeAnnotationAgentNode"]
        N7["MigrationAgentNode"]
        N8["Orchestrator/Intent/Approval Nodes"]
        N9["FileManagementNode"]
        N10["SafetyCheckNode"]
        N11["ContextAwarenessNode"]
        N12["ErrorHandlingNode"]
    end

    %% Utilities
    subgraph Utils["Utilities"]
        UTL1["call_gemini.py\\n(GeminiAPIProxy)"]
        UTL2["utils.py"]
        UTL3["visualize_flow.py"]
    end

    %% LLM Cloud
    subgraph Cloud["Google AI Cloud"]
        C1["gemini-1.5-flash\\n(LLM Model)"]
    end

    %% Data Flow
    U1 --> M1
    U1 --> M2
    M1 --> F1
    M2 --> M1
    F1 --> F2
    F2 --> N1
    F2 --> N2
    F2 --> N3
    F2 --> N4
    F2 --> N5
    F2 --> N6
    F2 --> N7
    F2 --> N8
    F2 --> N9
    F2 --> N10
    F2 --> N11
    F2 --> N12
    N1 --> UTL1
    N2 --> UTL1
    N3 --> UTL1
    N4 --> UTL1
    N5 --> UTL1
    N6 --> UTL1
    N7 --> UTL1
    N8 --> UTL1
    N9 --> UTL1
    N10 --> UTL1
    N11 --> UTL1
    N12 --> UTL1
    UTL1 --> C1
    C1 -- "LLM Response" --> UTL1
    UTL1 -- "Result" --> N1
    UTL1 -- "Result" --> N2
    UTL1 -- "Result" --> N3
    UTL1 -- "Result" --> N4
    UTL1 -- "Result" --> N5
    UTL1 -- "Result" --> N6
    UTL1 -- "Result" --> N7
    UTL1 -- "Result" --> N8
    UTL1 -- "Result" --> N9
    UTL1 -- "Result" --> N10
    UTL1 -- "Result" --> N11
    UTL1 -- "Result" --> N12
    N1 --> F1
    N2 --> F1
    N3 --> F1
    N4 --> F1
    N5 --> F1
    N6 --> F1
    N7 --> F1
    N8 --> F1
    N9 --> F1
    N10 --> F1
    N11 --> F1
    N12 --> F1
    F1 --> M1
    M1 --> U2

    %% Style for solid colors
    style U1 fill:#f9d423,stroke:#e65c00,stroke-width:2px
    style U2 fill:#f9d423,stroke:#e65c00,stroke-width:2px
    style M1 fill:#36d1c4,stroke:#11998e,stroke-width:2px
    style M2 fill:#36d1c4,stroke:#11998e,stroke-width:2px
    style F1 fill:#43e97b,stroke:#38f9d7,stroke-width:2px
    style F2 fill:#43e97b,stroke:#38f9d7,stroke-width:2px
    style N1 fill:#f857a6,stroke:#ff5858,stroke-width:2px
    style N2 fill:#f857a6,stroke:#ff5858,stroke-width:2px
    style N3 fill:#f857a6,stroke:#ff5858,stroke-width:2px
    style N4 fill:#f857a6,stroke:#ff5858,stroke-width:2px
    style N5 fill:#f857a6,stroke:#ff5858,stroke-width:2px
    style N6 fill:#f857a6,stroke:#ff5858,stroke-width:2px
    style N7 fill:#f857a6,stroke:#ff5858,stroke-width:2px
    style N8 fill:#f857a6,stroke:#ff5858,stroke-width:2px
    style N9 fill:#f857a6,stroke:#ff5858,stroke-width:2px
    style N10 fill:#f857a6,stroke:#ff5858,stroke-width:2px
    style N11 fill:#f857a6,stroke:#ff5858,stroke-width:2px
    style N12 fill:#f857a6,stroke:#ff5858,stroke-width:2px
    style UTL1 fill:#36d1c4,stroke:#11998e,stroke-width:2px
    style UTL2 fill:#36d1c4,stroke:#11998e,stroke-width:2px
    style UTL3 fill:#36d1c4,stroke:#11998e,stroke-width:2px
    style C1 fill:#f9d423,stroke:#e65c00,stroke-width:2px
"""
    
    return diagram
