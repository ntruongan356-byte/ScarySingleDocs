# sdAIgen Repository Overview

## Project Overview

The sdAIgen project is a comprehensive Stable Diffusion WebUI notebook designed to run on Google Colab and Kaggle platforms. Here are the key features and components:

### 🌟 Main Features
- **Multiplatform notebook**: Google Colab, Kaggle.
- **Widgets for easy interaction**.
- **Preset custom**: Settings + Styles + UI Theme
- **Download previews** for models, LoRa and embedding (CivitAi) | There are limitations for Kaggle.
- **Choosing WebUI** between A1111, ComfyUI, Forge, Classic (Forge), ReForge, SD-UX.
- **Exclusive to Google Colab**: Connection to GDrive and buttons to export/import widget settings~ | Main Widgets

### 📚 Installed Extensions

| ✔️ — Installed | ❌ — Not Installed | 🔄 — Integrated Version | † — Only in Kaggle |
|---------------|-------------------|-------------------------|-------------------|

| Extension | A1111 | Forge | Classic | ReForge | SD-UX |
|-----------|-------|-------|---------|---------|-------|
| adetailer | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| ScarySingleDocs-theme | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| Aspect-Ratio-Helper | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| Civitai-Browser-plus | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| Civitai-Extension | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| ControlNet | ✔️ | 🔄 | 🔄 | 🔄 | ✔️ |
| Encrypt-Image | ✔️† | ✔️† | ✔️† | ✔️† | ✔️† |
| Image-Info | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| Image-Viewer | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| Infinite-Image-Browsing | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| Regional-Prompter | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| SD-Couple | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| SD-Hub | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| State | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| SuperMerger | ✔️ | ✔️ | ❌ | ✔️ | ✔️ |
| Tag-Complete | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| Umi-AI-Wildcards | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| WD14-Tagger | ✔️ | ✔️ | ❌ | ✔️ | ✔️ |
| webui_timer | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

### 🧩 Installed Custom-Nodes | ComfyUI
- Advanced-ControlNet
- ComfyUI-Custom-Scripts
- ComfyUI-Impact-Pack
- ComfyUI-Impact-Subpack
- ComfyUI-Manager
- ComfyUI-Model-Manager
- ControlNet-AUX
- Efficiency-Nodes
- UltimateSDUpscale
- WAS-Nodes
- WD14-Tagger

### 📁 Repository Structure
The repository contains several key components:

#### Notebook files (`/notebook/`):
- `ScarySingleDocs_sdAIgen_EN.ipynb` - English version
- `ScarySingleDocs_sdAIgen_RU.ipynb` - Russian version

#### Widget system (`/modules/`):
- `widget_factory.py` - Core widget creation system
- `webui_utils.py` - WebUI utilities
- `Manager.py` - Download and installation manager
- `CivitaiAPI.py` - CivitAI API integration

#### Scripts (`/scripts/`):
- Language-specific widgets (`en/`, `ru/`)
- Launch scripts and utilities
- Auto-cleaner and download-result tools

#### Configurations (`/__configs__/`):
- Separate config folders for each WebUI variant
- Pre-configured settings and extensions lists

### 🧩 Installed Extensions
The project includes numerous extensions for each WebUI variant:
- **adetailer** - Automatic detailer
- **Civitai-Browser-plus** - Enhanced Civitai browsing
- **ControlNet** - ControlNet support
- **Infinite-Image-Browsing** - Image gallery management
- **Tag-Complete** - Auto-completion for prompts
- **SuperMerger** - Model merging capabilities
- And many more...

### 🎨 Customization Options
- **Theme support**: Custom UI themes with accent color options
- **Model management**: Easy selection and downloading of models, VAEs, ControlNets
- **Token management**: Support for CivitAI, HuggingFace, Ngrok, and Zrok tokens
- **Custom downloads**: Flexible download system with URL support

## Directory Structure

### `__configs__`
Files for interface customization, styles, and configuration scripts.

- **install-deps.py**: Automatic dependency installer for custom ComfyUI nodes.
- **gradio-tunneling.py**: Replaces the original main.py of the library to obtain a tunnel URL.
- **tagcomplete-tags-parser.py**: This script parses CSV files from the archive repository for the TagComplete extension.

### `CSS`
CSS styles for widgets.

- **download-result.css**: Styles for the download-result widget.
- **auto-cleaner.css**: Styles for the auto-cleaner widget.
- **main-widgets.css**: Styles for the main widgets.

### `JS`
JavaScript functionality for Widgets.

- **main-widgets.js**: JS script for collapsing/expanding the customDL section (Main Widgets).

### `modules`
Backend functionality modules.

- **CivitaiAPI.py**: Handler for interacting with the Civitai API.
- **webui_utils.py**: Module for writing time to a txt file (UI timer) and setting directory paths.
- **json_utils.py**: Tools for processing JSON data.
- **TunnelHub.py**: Module for creating and handling tunnels, outputs URL links.
- **widget_factory.py**: IPyWidgets factory generator.
- **Manager.py**: Module with m_download and m_clone functions for downloading files and cloning git repositories.
- **__season.py**: Nice text display at startup (used in setup.py).

### `scripts`
Main notebook scripts.

- **_models-data.py**: Metadata for SD-1.5 models (URLs/names).
- **_xl-models-data.py**: Metadata for XL models (URLs/names).
- **launch.py**: Main script for launching WebUI, configuring tunnels, configs, and command-line arguments.
- **auto-cleaner.py**: System for automatic model file cleaning.
- **download-result.py**: Widget for displaying downloaded files.
- **setup.py**: Initial setup and files preparation.
- **webui-installer.py**: Unpacks WebUI archives, downloads configs and extensions/nodes.

#### `scripts/en`
Localization scripts.

- **downloading-en.py**: Main script for downloading VENV, libraries, models, and displaying data (download-result.py).
- **widgets-en.py**: Script for displaying main widgets.

## Widgets

### Basics - Base:

#### Model Selection
- **Model**: A list of available models to choose from. Each model follows this format: `<Number>.<Model Name> [Style] [Version] (+ INP)`
  - `<Number>` - the ordinal number of the model for downloading multiple models simultaneously.
  - `<Model Name>` - the name of the model under which it will be saved.
  - `[Style]` - the default style of the model.
  - `[Version]` - the version of the model specified by the author.
  - `+INP` - indicates the presence of an inpainting version. It will be downloaded only if the "Inpainting model" checkbox is activated.
- **Model Number**: Field for entering model numbers from the list, separated by commas/spaces or written together for downloading.
- **Inpainting Model**: Required only for models marked + INP
  - This checkbox is not available for SDXL
- **SDXL**: A toggle between SD 1.5 and XL models (including VAE and CNET).

#### Exclusive (Google Colab):
- **GDrive button**: connects Google Drive to NoteBook, creating symbolic links to Models, Vae and LoRa.
  - An sdAIgen folder will be automatically created in your Drive - Model files will be placed in it
- **Buttons Export and Import widget settings to JSON format.** (Saves all widget values)

#### VAE Selection
Similar to Models.

#### Additional
- **WebUI Update and Extensions Update**: Do not require explanation.
- **Change WebUI**: A toggle between available interfaces.
- **Detailed Download**: Allows tracking of the download process: link, save location, file name (if specified), preview image URL of the model (only for CivitAI).
- **ControlNet and ControlNet Number**: Do not require explanation (similar to models and VAE).
- **Commit Hash**: For Git users. By specifying the hash of the desired commit, you can revert WebUI to a previous or newer version.
- **CivitAI Token**: For downloading paid models and/or models requiring registration on the site.
- **HuggingFace Token**: Specify the token for downloading a private model from Hugging Face.
- **Ngrok Token**: Specify the Ngrok token for creating an additional tunnel.
- **Zrok Token**: An alternative for tunneling with Ngrok.
- **Arguments**: Parameters for launching WebUI. If unsure, it's better not to change anything or refer to the WIKI.

#### Custom Download
Used for downloading files: models, VAE, LoRa, Embed, ADetailer, or extensions. Specify links in the appropriate fields, separating them with commas or spaces.
You can specify the name of the saved file in square brackets `[]` after the link without spaces.
For convenience, it is recommended to use "File (TXT)" — Read more about it HERE.
- **Empowerment**: A toggle between text fields and the portable version of "File (TXT)".

## File_txt

### FILE (TXT):
- **Info**: Simultaneous processing of multiple files.txt is supported. Specify links separated by commas or spaces.

### How to Use file.txt?
It's simple: specify links to files after a tag starting with `#`, which denotes the directory for saving the file. Supported tags: Presented in the table below. Short tags are simplified versions of regular tags that start with `$` without a space, for example, `$ckpt`.
You can also specify the name under which you want to save the file (similar to what is described in INFO in the widgets).

### Example of Use:
```
# Example
Info: All links after the tag will relate to this tag until the next found tag. This means you can specify links in one line (separated by commas or spaces) or on subsequent lines for convenience.
```

### Table of Available Tags for "File (txt)"

| Tags | Short Tags | Path (A1111/Forge/Classic) | Path (ComfyUI) |
|------|------------|----------------------------|----------------|
| model | $ckpt | ~/WEBUI/models/Stable-diffusion | ~/ComfyUI/models/checkpoints |
| vae | $vae | ~/WEBUI/models/VAE | ~/ComfyUI/models/vae |
| lora | $lora | ~/WEBUI/models/Lora | ~/ComfyUI/models/loras |
| embed | $emb | ~/WEBUI/embeddings | ~/ComfyUI/models/embeddings |
| extension | $ext | ~/WEBUI/extensions | ~/ComfyUI/custom_nodes |
| adetailer | $ad | ~/WEBUI/models/adetailer | ~/ComfyUI/models/ultralytics |
| control | $cnet | ~/WEBUI/models/ControlNet | ~/ComfyUI/models/controlnet |
| upscale | $ups | ~/WEBUI/models/ESRGAN | ~/ComfyUI/models/upscale_models |
| clip | $clip | ~/WEBUI/models/text_encoder | ~/ComfyUI/models/clip |
| unet | $unet | ~/WEBUI/models/text_encoder (jointly) | ~/ComfyUI/models/unet |
| vision | $vis | ~/WEBUI/models/clip_vision | ~/ComfyUI/models/clip_vision |
| encoder | $enc | ~/WEBUI/models/text_encoder | ~/ComfyUI/models/text_encoders |
| diffusion | $diff | ~/WEBUI/models/diffusion_models | ~/ComfyUI/models/diffusion_models |
| config | $cfg | ~/WEBUI/ (root) | ~/ComfyUI/user/default |

## Additional Resources

- **WebUIs and Configs Repository**: https://huggingface.co/NagisaNao/ScarySingleDocs/tree/main - The repo for the webUis and their configs and the venv the notebook uses.