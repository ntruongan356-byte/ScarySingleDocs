# Mermaid Guide for ScarySingleDocs Documentation

This guide explains how to use Mermaid syntax to create various diagrams for documenting the ScarySingleDocs project. Mermaid is a simple markdown-like syntax for generating diagrams and flowcharts.

## What is Mermaid?

Mermaid is a JavaScript-based diagramming and charting tool that uses Markdown-inspired text definitions to create and modify diagrams dynamically. It's perfect for documentation because:
- It's text-based and version control friendly
- It integrates seamlessly with markdown
- It supports a wide variety of diagram types
- It's easy to learn and use

## Basic Syntax

Mermaid diagrams are enclosed in triple backticks with the `mermaid` identifier:

```mermaid
graph TD
    A[Start] --> B[Process]
    B --> C[End]
```

## Supported Diagram Types

### 1. Flowcharts

Flowcharts are perfect for showing processes, workflows, and decision trees.

#### Basic Flowchart
```mermaid
graph TD
    A[Start] --> B{Is it working?}
    B -->|Yes| C[Great!]
    B -->|No| D[Debug]
    D --> B
    C --> E[End]
```

#### Flowchart with Subgraphs
```mermaid
graph TD
    subgraph Frontend
        A[React Components] --> B[State Management]
        B --> C[UI Rendering]
    end
    subgraph Backend
        D[API Routes] --> E[Database]
        E --> F[Business Logic]
    end
    A --> D
    C --> F
```

### 2. Sequence Diagrams

Sequence diagrams show how objects interact in a particular scenario.

#### Basic Sequence Diagram
```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant Database
    
    User->>Frontend: Clicks button
    Frontend->>Backend: API Request
    Backend->>Database: Query data
    Database-->>Backend: Return data
    Backend-->>Frontend: JSON Response
    Frontend-->>User: Update UI
```

#### Complex Sequence with Loops
```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant Server
    
    loop Every 5 seconds
        User->>Browser: Check for updates
        Browser->>Server: Poll /api/updates
        Server-->>Browser: Update status
        Browser-->>User: Show notification
    end
```

### 3. Class Diagrams

Class diagrams are perfect for showing software architecture and object-oriented design.

#### Basic Class Diagram
```mermaid
classDiagram
    class User {
        +string id
        +string name
        +string email
        +login()
        +logout()
    }
    
    class Model {
        +string id
        +string name
        +string type
        +download()
        +configure()
    }
    
    class DownloadManager {
        +list models[]
        +downloadModel(model)
        +getProgress()
    }
    
    User "1" -- "*" Model : owns
    DownloadManager "1" -- "*" Model : manages
```

#### Advanced Class Diagram
```mermaid
classDiagram
    class Component {
        <<abstract>>
        +render()
        +setState()
    }
    
    class TabComponent {
        +string activeTab
        +switchTab()
        +renderContent()
    }
    
    class ToggleButton {
        +boolean isChecked
        +toggle()
        +updateStyle()
    }
    
    class StatusPanel {
        +map selections
        +updateCount()
        +renderStats()
    }
    
    Component <|-- TabComponent
    Component <|-- ToggleButton
    Component <|-- StatusPanel
```

### 4. State Diagrams

State diagrams show the state transitions of a system or component.

#### Basic State Diagram
```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Downloading: Start Download
    Downloading --> Completed: Finish
    Downloading --> Failed: Error
    Failed --> Idle: Retry
    Completed --> Idle: Reset
```

#### Complex State Diagram
```mermaid
stateDiagram-v2
    [*] --> Initializing
    Initializing --> Ready: System Check OK
    Initializing --> Error: System Check Failed
    
    Ready --> ModelSelection: User Clicks
    ModelSelection --> Configuring: Model Selected
    Configuring --> Downloading: Configuration Complete
    
    Downloading --> Completed: Success
    Downloading --> Failed: Network Error
    
    Failed --> Ready: User Acknowledges
    Completed --> Ready: Continue
    
    Error --> [*]: System Restart
```

### 5. Entity Relationship Diagrams (ERD)

ERDs are perfect for showing database relationships.

#### Basic ERD
```mermaid
erDiagram
    USER {
        string id PK
        string name
        string email
        datetime created_at
    }
    
    MODEL {
        string id PK
        string name
        string type
        string file_path
        datetime created_at
    }
    
    DOWNLOAD {
        string id PK
        string user_id FK
        string model_id FK
        datetime downloaded_at
        string status
    }
    
    USER ||--o{ DOWNLOAD : "makes"
    MODEL ||--o{ DOWNLOAD : "is downloaded"
```

### 6. User Journey Maps

User journey maps show the user's experience through a system.

#### User Journey for Model Selection
```mermaid
journey
    title User Journey: Model Selection Process
    section Initial Access
      User visits ScarySingleDocs: 5: User
      System loads interface: 3: System
      User sees available models: 4: User
    
    section Model Selection
      User clicks Models tab: 5: User
      System displays model list: 3: System
      User reviews model options: 4: User
    
    section Configuration
      User toggles desired models: 5: User
      System updates selection state: 3: System
      User configures additional options: 4: User
    
    section Download
      User initiates download: 5: User
      System processes request: 3: System
      User monitors progress: 4: User
```

### 7. Git Graphs

Git graphs show branching and merging in version control.

#### Git Workflow
```mermaid
gitGraph
    commit
    branch feature/new-interface
    checkout feature/new-interface
    commit
    commit
    checkout main
    commit
    merge feature/new-interface
    commit
    branch hotfix/bug-fix
    checkout hotfix/bug-fix
    commit
    checkout main
    merge hotfix/bug-fix
```

### 8. Timeline Diagrams

Timeline diagrams show events over time.

#### Project Timeline
```mermaid
timeline
    title ScarySingleDocs Interface Development Timeline
    section Planning
      Requirement Analysis : 2024-01-01, 3d
      Design Mockups : 2024-01-04, 5d
    
    section Development
      Setup Project : 2024-01-09, 2d
      Implement UI Components : 2024-01-11, 7d
      Add Interactivity : 2024-01-18, 5d
    
    section Testing
      Unit Testing : 2024-01-23, 3d
      Integration Testing : 2024-01-26, 2d
    
    section Deployment
      Final Review : 2024-01-28, 1d
      Production Deploy : 2024-01-29, 1d
```

### 9. Pie Charts

Pie charts show data distribution.

#### Model Type Distribution
```mermaid
pie title Model Type Distribution
    "Stable Diffusion Models" : 45
    "VAE Models" : 20
    "LoRA Models" : 25
    "ControlNet Models" : 10
```

### 10. Quadrant Charts

Quadrant charts are useful for prioritization and analysis.

#### Feature Prioritization
```mermaid
quadrantChart
    title Feature Prioritization Matrix
    x-axis Low Cost --> High Cost
    y-axis Low Value --> High Value
    quadrant-1 High Priority: Do it now
    quadrant-2 Strategic: Plan for future
    quadrant-3 Low Priority: Maybe later
    quadrant-4 Reconsider: Avoid if possible
    
    "Tabbed Interface": [0.8, 0.9]
    "Dark Mode": [0.3, 0.7]
    "Advanced Search": [0.7, 0.6]
    "Mobile App": [0.9, 0.4]
```

## Best Practices for ScarySingleDocs Documentation

### 1. Consistency
- Use consistent styling across all diagrams
- Follow a naming convention for nodes and connections
- Maintain consistent direction (top-to-bottom or left-to-right)

### 2. Clarity
- Keep diagrams simple and focused
- Use descriptive names for nodes
- Add comments or notes when necessary
- Break complex diagrams into smaller, focused diagrams

### 3. Documentation Structure
```mermaid
graph TD
    A[Documentation] --> B[Architecture]
    A --> C[User Guides]
    A --> D[API Reference]
    A --> E[Development]
    
    B --> B1[System Overview]
    B --> B2[Component Diagram]
    B --> B3[Database Schema]
    
    C --> C1[Getting Started]
    C --> C2[Feature Tutorials]
    C --> C3[Troubleshooting]
    
    D --> D1[Endpoints]
    D --> D2[Data Models]
    D --> D3[Authentication]
    
    E --> E1[Setup Guide]
    E --> E2[Contributing]
    E --> E3[Testing]
```

### 4. Example: Complete ScarySingleDocs System Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[React Components]
        STATE[Zustand Store]
        ROUTES[Next.js Routes]
    end
    
    subgraph "Backend Layer"
        API[API Routes]
        AUTH[Authentication]
        DB[(Database)]
    end
    
    subgraph "External Services"
        WEBUI[WebUI Services]
        CLOUD[Cloud Storage]
        MODELS[Model Repository]
    end
    
    UI --> STATE
    STATE --> ROUTES
    ROUTES --> API
    API --> AUTH
    API --> DB
    API --> WEBUI
    API --> CLOUD
    API --> MODELS
```

## Integration with Markdown

Mermaid diagrams integrate seamlessly with markdown files:

```markdown
# ScarySingleDocs Architecture

## System Overview

The ScarySingleDocs system consists of several interconnected components:

```mermaid
graph LR
    A[User Interface] --> B[API Layer]
    B --> C[Database]
    B --> D[External Services]
```

## User Flow

Here's how users interact with the system:

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend
    
    U->>F: Access Interface
    F->>B: Load Models
    B-->>F: Return Model List
    F-->>U: Display Options
```
```

## Tools and Editors

### Online Editors
- **Mermaid Live Editor**: https://mermaid.live
- **Mermaid-js GitHub**: https://github.com/mermaid-js/mermaid

### VS Code Integration
- Install the "Markdown Preview Mermaid Support" extension
- Use "Markdown All in One" for enhanced markdown support

### Documentation Platforms
- **GitHub**: Supports Mermaid natively in markdown files
- **GitLab**: Built-in Mermaid support
- **Notion**: Supports Mermaid via code blocks
- **Confluence**: Use Mermaid plugin

## Common Issues and Solutions

### 1. Syntax Errors
- **Issue**: Diagram not rendering
- **Solution**: Check for missing brackets, quotes, or proper indentation

### 2. Performance Issues
- **Issue**: Large diagrams slow down page loading
- **Solution**: Break into smaller diagrams or use subgraphs

### 3. Styling Issues
- **Issue**: Inconsistent appearance
- **Solution**: Use consistent styling and themes

### 4. Version Compatibility
- **Issue**: Different Mermaid versions support different features
- **Solution**: Specify Mermaid version in your project

## Advanced Tips

### 1. Custom Styling
```mermaid
%%{init: {'theme': 'dark', 'themeVariables': { 'primaryColor': '#ff0000'}}}%%
graph TD
    A[Custom Style] --> B[Red Accent]
```

### 2. Links and References
```mermaid
graph TD
    A[Documentation] --> B[API Reference]
    click B "https://api.example.com" "Open API Docs"
```

### 3. Comments
```mermaid
graph TD
    A[Start] --> B[Process]
    %% This is a comment
    B --> C[End]
```

## Conclusion

Mermaid is a powerful tool for creating diagrams in documentation. For the ScarySingleDocs project, it can be used to:

- Visualize system architecture
- Document user flows
- Show database relationships
- Illustrate component hierarchies
- Map development timelines
- Create user journey maps

By following this guide, you can create clear, consistent, and informative diagrams that enhance the project documentation and improve understanding for all stakeholders.

---

**Resources**:
- [Mermaid Official Documentation](https://mermaid-js.github.io/mermaid/#/)
- [Mermaid Syntax Guide](https://mermaid-js.github.io/mermaid/#/n00b-syntaxReference)
- [Mermaid Live Editor](https://mermaid.live)