# sdAIgen Complete File Map

## Overview
This document provides a comprehensive map of all files in the sdAIgen project, organized by folder with detailed descriptions of each file's purpose and functionality.

---

## 📁 Root Directory (`/`)

### 📄 README.md
**Purpose**: Main project landing page and feature overview for English users
**Description**: Primary README file containing project introduction, feature list, supported extensions, installation links for Colab/Kaggle, and credits. Includes comprehensive tables of installed extensions for different WebUI variants and custom nodes for ComfyUI.

### 📄 README-ru-RU.md  
**Purpose**: Main project landing page and feature overview for Russian users
**Description**: Russian language version of the main README file with identical structure and content, translated for Russian-speaking users. Includes the same feature lists, extension tables, and platform links.

---

## 📁 `.Docs/` (Hidden Documentation Folder)

### 📁 `.Docs/Imgs/`
#### 🖼️ `logo.png`
**Purpose**: Project logo image asset
**Description**: Official sdAIgen project logo used in documentation and branding.

#### 🖼️ `preview.png` 
**Purpose**: Project preview/screenshot image
**Description**: Preview image showcasing the sdAIgen interface and capabilities, used in README files for visual representation.

### 📁 `.Docs/SVG/`
#### 🎨 `Boosty_Logo_Color.svg`
**Purpose**: Boosty donation platform logo
**Description**: Colored SVG logo for Boosty donation platform, used in support/donation sections.

#### 🎨 `DA_Logo_Color.svg`
**Purpose**: DonationAlerts logo
**Description**: Colored SVG logo for DonationAlerts platform, used in support/donation sections.

### 📁 `.Docs/SVG/en/` (English Language Assets)
#### 🎨 `colab-en.svg`
**Purpose**: Google Colab platform banner (English)
**Description**: English language banner for Google Colab platform integration, used in README for platform access links.

#### 🎨 `discord-en.svg`
**Purpose**: Discord community banner (English)
**Description**: English language banner for Discord community server, used in README for community engagement links.

#### 🎨 `kaggle-en.svg`
**Purpose**: Kaggle platform banner (English)
**Description**: English language banner for Kaggle platform integration, used in README for platform access links.

### 📁 `.Docs/SVG/ru/` (Russian Language Assets)
#### 🎨 `colab-ru.svg`
**Purpose**: Google Colab platform banner (Russian)
**Description**: Russian language banner for Google Colab platform integration, used in Russian README for platform access links.

#### 🎨 `discord-ru.svg`
**Purpose**: Discord community banner (Russian)
**Description**: Russian language banner for Discord community server, used in Russian README for community engagement links.

#### 🎨 `kaggle-ru.svg`
**Purpose**: Kaggle platform banner (Russian)
**Description**: Russian language banner for Kaggle platform integration, used in Russian README for platform access links.

### 📁 `.Docs/flags/`
#### 🏁 `en-US.png`
**Purpose**: English language flag icon
**Description**: Flag icon representing English (US) language, used for language selection and localization.

#### 🏁 `ru-RU.png`
**Purpose**: Russian language flag icon
**Description**: Flag icon representing Russian language, used for language selection and localization.

---

## 📁 `CSS/` (Stylesheets)

### 🎨 `auto-cleaner.css`
**Purpose**: Styling for auto-cleaner interface components
**Description**: CSS file containing styles for the auto-cleaner utility interface, including layout, colors, and responsive design elements for file management widgets.

### 🎨 `download-result.css`
**Purpose**: Styling for download result interface
**Description**: CSS file containing styles for download result display components, including progress indicators, status messages, and result formatting for download operations.

### 🎨 `main-widgets.css`
**Purpose**: Main widget styling system
**Description**: Comprehensive CSS file containing all styling for the main widget interface, including containers, buttons, forms, headers, and responsive layout system. Features modern CSS variables, 3D animations, custom scrollbars, and a complete dark theme design system. ✅ **ANALYSIS COMPLETE**

---

## 📁 `Docs/` (Documentation Folder)

### 📄 REPOSITORY_OVERVIEW.md
**Purpose**: Complete project overview and architecture documentation
**Description**: Comprehensive documentation covering project overview, architecture, features, platform support, installation guidelines, and technical details. Serves as the primary technical documentation for understanding the entire project structure.

### 📄 modules.md
**Purpose**: Detailed module system documentation
**Description**: Technical documentation for all modules in the project, including module descriptions, interdependencies, configuration files, external dependencies, extension points, and usage patterns. Provides in-depth technical information for developers.

### 📄 cell1.md
**Purpose**: Setup.py function-by-function guide
**Description**: Detailed documentation for the setup.py script, breaking down each function's purpose, parameters, behavior, and usage. Includes module utilization information and comprehensive examples for understanding the setup process.

### 📄 cell2-updated.md
**Purpose**: Updated webui-installer.py and launch.py analysis
**Description**: Comprehensive analysis of the two core scripts (webui-installer.py and launch.py) covering WebUI installation configuration and launch/tunnel management systems. Includes detailed function breakdowns, architectural analysis, and integration patterns.

### 📄 main-widgets-analysis.md
**Purpose**: Main-widgets CSS and JS components analysis
**Description**: Comprehensive analysis of the main-widgets components including CSS styling system and JavaScript interactive functionality. Covers design patterns, performance optimization, user experience design, and technical implementation details for the complete widget system.

### 📄 sdaigen-map.md
**Purpose**: Complete file map and directory structure
**Description**: This file - comprehensive map of all files in the project organized by folder with detailed descriptions of each file's purpose, functionality, and relationships. Serves as a navigation guide for understanding project structure.

---

## 📁 `JS/` (JavaScript)

### ⚡ `main-widgets.js`
**Purpose**: Main widget JavaScript functionality
**Description**: JavaScript file containing client-side functionality for widgets, including interactive behaviors, event handling, dynamic content updates, and user interface enhancements. Features container management, file operations (JSON import/export), notification systems, and Google Colab integration. ✅ **ANALYSIS COMPLETE**

---

## 📁 `__configs__/` (Configuration Files)

### 📁 `__configs__/A1111/` (Automatic1111 WebUI Configuration)
#### 📋 `_extensions.txt`
**Purpose**: Extension list for Automatic1111 WebUI
**Description**: Text file containing list of extensions to be installed with Automatic1111 WebUI, including URLs and local names for each extension. Organized by contributor (ANXETY, Gutris1, OTHER).

#### ⚙️ `config.json`
**Purpose**: Automatic1111 WebUI configuration
**Description**: JSON configuration file containing settings for Automatic1111 WebUI, including model paths, extension settings, UI preferences, and operational parameters.

#### 🎛️ `ui-config.json`
**Purpose**: Automatic1111 UI configuration
**Description**: JSON configuration file containing UI-specific settings for Automatic1111 WebUI, including interface layout, default values, and user interface preferences.

### 📁 `__configs__/Classic/` (Classic Forge WebUI Configuration)
#### 📋 `_extensions.txt`
**Purpose**: Extension list for Classic Forge WebUI
**Description**: Text file containing list of extensions to be installed with Classic Forge WebUI, similar to A1111 but optimized for Classic variant.

#### ⚙️ `config.json`
**Purpose**: Classic Forge WebUI configuration
**Description**: JSON configuration file containing settings for Classic Forge WebUI, with specific optimizations and settings for the Classic variant.

#### 🎛️ `ui-config.json`
**Purpose**: Classic Forge UI configuration
**Description**: JSON configuration file containing UI-specific settings for Classic Forge WebUI, tailored for the Classic interface variant.

### 📁 `__configs__/ComfyUI/` (ComfyUI Configuration)
#### 📋 `_extensions.txt`
**Purpose**: Custom nodes list for ComfyUI
**Description**: Text file containing list of custom nodes to be installed with ComfyUI, including various AI and processing nodes for workflow creation.

#### 📁 `__configs__/ComfyUI/Comfy-Manager/`
##### ⚙️ `config.ini`
**Purpose**: ComfyUI Manager configuration
**Description**: INI configuration file for ComfyUI Manager, containing settings for node management, updates, and repository configurations.

#### ⚙️ `comfy.settings.json`
**Purpose**: ComfyUI settings configuration
**Description**: JSON configuration file containing ComfyUI-specific settings, including default workflows, UI preferences, and operational parameters.

#### 🐍 `install-deps.py`
**Purpose**: ComfyUI dependencies installation script
**Description**: Python script for installing ComfyUI dependencies, including required packages and system dependencies for proper ComfyUI operation.

#### 📁 `__configs__/ComfyUI/workflows/`
##### 🔄 `anxety-workflow.json`
**Purpose**: Default ComfyUI workflow
**Description**: JSON file containing a pre-configured ComfyUI workflow created by ANXETY, serving as a starting template for users.

### 📁 `__configs__/Forge/` (Forge WebUI Configuration)
#### 📋 `_extensions.txt`
**Purpose**: Extension list for Forge WebUI
**Description**: Text file containing list of extensions to be installed with Forge WebUI, optimized for Forge variant with specific extension compatibility.

#### ⚙️ `config.json`
**Purpose**: Forge WebUI configuration
**Description**: JSON configuration file containing settings for Forge WebUI, with Forge-specific optimizations and performance settings.

#### 🎛️ `ui-config.json`
**Purpose**: Forge UI configuration
**Description**: JSON configuration file containing UI-specific settings for Forge WebUI, tailored for the Forge interface variant.

### 📁 `__configs__/ReForge/` (ReForge WebUI Configuration)
#### 📋 `_extensions.txt`
**Purpose**: Extension list for ReForge WebUI
**Description**: Text file containing list of extensions to be installed with ReForge WebUI, optimized for ReForge variant with specific extension compatibility.

#### ⚙️ `config.json`
**Purpose**: ReForge WebUI configuration
**Description**: JSON configuration file containing settings for ReForge WebUI, with ReForge-specific optimizations and enhanced settings.

#### 🎛️ `ui-config.json`
**Purpose**: ReForge UI configuration
**Description**: JSON configuration file containing UI-specific settings for ReForge WebUI, tailored for the ReForge interface variant.

### 📁 `__configs__/SD-UX/` (SD-UX WebUI Configuration)
#### 📋 `_extensions.txt`
**Purpose**: Extension list for SD-UX WebUI
**Description**: Text file containing list of extensions to be installed with SD-UX WebUI, optimized for SD-UX variant with specific extension compatibility.

#### ⚙️ `config.json`
**Purpose**: SD-UX WebUI configuration
**Description**: JSON configuration file containing settings for SD-UX WebUI, with SD-UX-specific optimizations and user experience settings.

#### 🎛️ `ui-config.json`
**Purpose**: SD-UX UI configuration
**Description**: JSON configuration file containing UI-specific settings for SD-UX WebUI, tailored for the SD-UX interface variant.

### 🖼️ `card-no-preview.png`
**Purpose**: Default no-preview image
**Description**: PNG image used as fallback when model previews are not available, displayed in model selection interfaces.

### 🐍 `gradio-tunneling.py`
**Purpose**: Gradio tunneling service script
**Description**: Python script providing tunneling functionality for Gradio-based interfaces, enabling remote access to local WebUI instances through Gradio's tunneling service.

### 🔊 `notification.mp3`
**Purpose**: Notification sound effect
**Description**: MP3 audio file used for notification sounds in the interface, providing audio feedback for user actions and system events.

### 📊 `styles.csv`
**Purpose**: Style definitions CSV
**Description**: CSV file containing style definitions and configurations for the WebUI, including prompt styles, negative prompts, and artistic style templates.

### 🐍 `tagcomplete-tags-parser.py`
**Purpose**: Tag completion parser script
**Description**: Python script for parsing and processing tag completion data, used by the TagComplete extension to provide autocomplete functionality for prompts.

### 🎨 `user.css`
**Purpose**: Custom user styles
**Description**: CSS file containing custom user-defined styles and theme modifications, allowing users to personalize the WebUI appearance beyond default themes.

---

## 📁 `modules/` (Core Python Modules)

### 🐍 `CivitaiAPI.py`
**Purpose**: CivitAI API integration module
**Description**: Comprehensive CivitAI API integration with advanced features for model management, including metadata extraction, preview image downloading, SHA256 verification, early access detection, and model information saving. Provides authentication-based access to CivitAI content.

### 🐍 `Manager.py`
**Purpose**: Download and Git management system
**Description**: Comprehensive download and Git management system with multi-platform support, handling multi-source downloading (CivitAI, HuggingFace, GitHub, Google Drive), Git repository management, batch processing, progress monitoring, and comprehensive error handling. Features advanced aria2c integration with colored progress output, intelligent URL routing, and robust error recovery mechanisms. ✅ **ANALYSIS COMPLETE**

### 🐍 `TunnelHub.py`
**Purpose**: Advanced tunneling system
**Description**: Advanced tunneling system for creating remote access to WebUI instances, supporting multiple protocols (Gradio, Pinggy, Cloudflared, Localtunnel, Ngrok, Zrok) with asynchronous management, URL extraction, and comprehensive logging.

### 🐍 `_season.py`
**Purpose**: Seasonal display system
**Description**: Seasonal display system with animated UI elements and multilingual support, providing season-based theming (Winter, Spring, Summer, Autumn) with particle effects, dynamic styling, and JavaScript-based animations.

### 🐍 `json_utils.py`
**Purpose**: Advanced JSON manipulation utilities
**Description**: Advanced JSON manipulation utilities with nested key support using dot notation, intelligent data merging, comprehensive error handling, colored logging output, and argument validation decorators. Most widely used module in the project.

### 🐍 `webui_utils.py`
**Purpose**: WebUI path management and configuration
**Description**: WebUI path management and configuration utilities, handling different WebUI types (A1111, ComfyUI, Forge, Classic, ReForge, SD-UX), path configuration, WebUI switching, and settings persistence.

### 🐍 `widget_factory.py`
**Purpose**: Core widget creation and management system
**Description**: Core widget creation and management system for Jupyter/Colab interfaces, creating and managing IPython widgets with consistent styling, CSS/JavaScript loading, layout management, and widget lifecycle handling.

---

## 📁 `notebook/` (Jupyter Notebook Files)

### 📓 `ANXETY_sdAIgen_EN.ipynb`
**Purpose**: English language Jupyter notebook
**Description**: Main Jupyter notebook for English users, containing the complete sdAIgen implementation with interactive widgets, setup procedures, and WebUI management functionality optimized for Google Colab and Kaggle platforms.

### 📓 `ANXETY_sdAIgen_RU.ipynb`
**Purpose**: Russian language Jupyter notebook
**Description**: Russian language version of the main Jupyter notebook, providing the same functionality as the English version but with all interface elements, instructions, and documentation translated for Russian-speaking users.

---

## 📁 `scripts/` (Main Scripts)

### 🐍 `_models-data.py`
**Purpose**: Standard model data definitions
**Description**: Python file containing comprehensive lists of standard SD 1.5 models, VAE files, and ControlNet models with download URLs and metadata. Includes curated selections of popular models organized by category with proper naming conventions.

### 🐍 `_xl-models-data.py`
**Purpose**: SDXL model data definitions
**Description**: Python file containing comprehensive lists of SDXL (Stable Diffusion XL) models, VAE files, and ControlNet models with download URLs and metadata. Similar structure to _models-data.py but specifically for SDXL format models.

### 🐍 `auto-cleaner.py`
**Purpose**: File cleanup utility
**Description**: Python script providing automated file cleanup functionality for WebUI installations, including temporary file removal, cache clearing, and disk space management with user-configurable cleanup rules.

### 🐍 `download-result.py`
**Purpose**: Download result processing and display
**Description**: Python script for processing and displaying download results, including progress tracking, success/failure reporting, and user interface components for download operations.

### 🐍 `launch.py`
**Purpose**: WebUI launch and tunneling management
**Description**: Main WebUI launch script with comprehensive tunneling management, handling WebUI startup, tunnel service configuration, environment setup, and session management. Supports multiple WebUI types with platform-specific optimizations.

### 🐍 `setup.py`
**Purpose**: Initial setup and file preparation
**Description**: Initial setup script that handles environment detection, file downloading, module management, and configuration setup. Downloads all necessary files, sets up the module system, and prepares the environment for WebUI operation.

### 🐍 `webui-installer.py`
**Purpose**: WebUI installation and configuration
**Description**: Comprehensive WebUI installation script that downloads and extracts WebUI archives, installs extensions, applies configuration files, and handles WebUI-specific setup requirements for different WebUI variants.

### 📁 `scripts/en/` (English Language Scripts)
#### 🐍 `downloading-en.py`
**Purpose**: English download interface functionality
**Description**: Comprehensive English language script providing complete download management system, including virtual environment setup, dependency installation, WebUI deployment, model downloading, Google Drive integration, and extension management. Features multi-platform download support (CivitAI, HuggingFace, GitHub, Google Drive), advanced error handling, and sophisticated progress monitoring. ✅ **ANALYSIS COMPLETE**

#### 🐍 `widgets-en.py`
**Purpose**: English widget interface
**Description**: English language script implementing the main widget interface, including model selection, configuration options, custom download functionality, and Google Drive integration for Colab environments.

### 📁 `scripts/ru/` (Russian Language Scripts)
#### 🐍 `downloading-ru.py`
**Purpose**: Russian download interface
**Description**: Russian language script providing download interface functionality, equivalent to downloading-en.py but with all interface elements and instructions translated for Russian-speaking users.

#### 🐍 `widgets-ru.py`
**Purpose**: Russian widget interface
**Description**: Russian language script implementing the main widget interface, equivalent to widgets-en.py but with all interface elements, instructions, and functionality translated for Russian-speaking users.

---

## 📁 File Organization Summary

### By Function Category:
- **🎨 Interface & Styling**: CSS/, JS/, .Docs/SVG/, .Docs/flags/
- **⚙️ Configuration**: __configs__/, settings management in modules/
- **🐍 Core Logic**: modules/ (all Python modules)
- **📓 User Interface**: notebook/ (Jupyter notebooks)
- **🔧 Utilities**: scripts/ (setup, installation, management)
- **📚 Documentation**: Docs/ (comprehensive documentation)

### By Language Support:
- **🇺🇸 English**: README.md, notebook/ANXETY_sdAIgen_EN.ipynb, scripts/en/
- **🇷🇺 Russian**: README-ru-RU.md, notebook/ANXETY_sdAIgen_RU.ipynb, scripts/ru/
- **🌐 Multilingual**: .Docs/SVG/, .Docs/flags/, _season.py

### By WebUI Support:
- **🎯 A1111**: __configs__/A1111/
- **🎯 ComfyUI**: __configs__/ComfyUI/
- **🎯 Forge**: __configs__/Forge/
- **🎯 Classic**: __configs__/Classic/
- **🎯 ReForge**: __configs__/ReForge/
- **🎯 SD-UX**: __configs__/SD-UX/

---

## 📊 Analysis Status Tracking

### Cell 2 Analysis (Completed) ✅
The following files have been comprehensively analyzed as part of Cell 2 analysis following the three-phase methodology (File Structure Analysis, Functional Decomposition, Interconnection Mapping):

#### Core Installation and Launch Scripts
- **🐍 `webui-installer.py`** - ✅ **ANALYSIS COMPLETE**
  - **Analysis Date**: Current session
  - **Methodology**: Phase 1, 2, and 3 analysis completed
  - **Documentation Location**: `cell2-updated.md` - Sections 1.1-1.3
  - **Key Insights**: WebUI installation system with async operations, multi-variant support, and comprehensive configuration management
  
- **🐍 `launch.py`** - ✅ **ANALYSIS COMPLETE**
  - **Analysis Date**: Current session
  - **Methodology**: Phase 1, 2, and 3 analysis completed
  - **Documentation Location**: `cell2-updated.md` - Sections 2.1-2.3
  - **Key Insights**: Advanced tunneling management, concurrent service testing, and robust error handling

#### User Interface and Configuration Files
- **🐍 `widgets-en.py`** - ✅ **ANALYSIS COMPLETE**
  - **Analysis Date**: Previous session
  - **Methodology**: Comprehensive widget and interface analysis
  - **Documentation Location**: `cell2-updated.md` - Section 3
  - **Key Insights**: Interactive widget system with Google Colab integration
  
- **📄 `settings.json`** - ✅ **ANALYSIS COMPLETE**
  - **Analysis Date**: Previous session
  - **Methodology**: Configuration structure and lifecycle analysis
  - **Documentation Location**: `cell2-updated.md` - Section 4
  - **Key Insights**: Centralized configuration hub with environment-specific settings

#### Cross-File Integration Analysis
- **🔗 Integration Analysis** - ✅ **COMPLETE**
  - **Documentation Location**: `cell2-updated.md` - Section 5
  - **Scope**: Execution flow dependencies, shared data dependencies, error handling integration, performance optimization integration
  - **Key Insights**: Sophisticated inter-phase coordination with graceful degradation and seamless user experience

### Next Analysis Priorities
Based on the comprehensive analysis plan and repository overview, the following files are prioritized for next analysis sessions:

#### ✅ **COMPLETED - Cell 3 Analysis**
- **🐍 `downloading-en.py`** - English download interface functionality ✅ **ANALYSIS COMPLETE**
- **🐍 `Manager.py`** - Download and Git management system ✅ **ANALYSIS COMPLETE**
  - **Documentation Location**: `cell3.md` - Complete comprehensive analysis
  - **Scope**: Virtual environment setup, dependency management, download operations, Git management, Google Drive integration
  - **Key Insights**: Sophisticated download management with multi-platform support, advanced error handling, and seamless integration with previous cells

#### Medium Priority (Cell 4 Candidates)
- **🐍 `CivitaiAPI.py`** - CivitAI API integration module
- **🐍 `TunnelHub.py`** - Advanced tunneling system
- **🐍 `json_utils.py`** - JSON manipulation utilities

#### Low Priority (Cell 5 Candidates)
- **🎨 `main-widgets.css`** - Main widget styling system ✅ **ANALYSIS COMPLETE**
- **⚡ `main-widgets.js`** - Main widget JavaScript functionality ✅ **ANALYSIS COMPLETE**

This comprehensive file map provides a complete overview of the sdAIgen project structure, making it easy to understand the purpose and location of each file in the system.