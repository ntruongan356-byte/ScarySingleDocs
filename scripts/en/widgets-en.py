# ~ widgets.py | by ScarySingleDocs ~

from widget_factory import WidgetFactory        # WIDGETS
from webui_utils import update_current_webui    # WEBUI
import json_utils as js                         # JSON

from IPython.display import display, Javascript
from google.colab import output
import ipywidgets as widgets
from pathlib import Path
import json
import os


osENV = os.environ

# Constants (auto-convert env vars to Path)
PATHS = {k: Path(v) for k, v in osENV.items() if k.endswith('_path')}   # k -> key; v -> value

HOME = PATHS['home_path']
SCR_PATH = PATHS['scr_path']
SETTINGS_PATH = PATHS['settings_path']
ENV_NAME = js.read(SETTINGS_PATH, 'ENVIRONMENT.env_name')

SCRIPTS = SCR_PATH / 'scripts'

CSS = SCR_PATH / 'CSS'
JS = SCR_PATH / 'JS'
widgets_css = CSS / 'main-widgets.css'
widgets_js = JS / 'main-widgets.js'

# Global state for widget toggles
gdrive_toggle_state = False


# ================ WIDGETS (Main Container) ================

def create_expandable_button(text, url):
    return factory.create_html(f'''
    <a href="{url}" target="_blank" class="button button_api">
        <span class="icon"><</span>
        <span class="text">{text}</span>
    </a>
    ''')

def read_model_data(file_path, data_type):
    """Reads model, VAE, LoRA, or ControlNet data from the specified file."""
    type_map = {
        'model': ('model_list', ['none']),
        'vae': ('vae_list', ['none', 'ALL']),
        'lora': ('lora_list', ['none', 'ALL']),
        'cnet': ('controlnet_list', ['none', 'ALL'])
    }
    key, prefixes = type_map[data_type]
    local_vars = {}

    with open(file_path) as f:
        exec(f.read(), {}, local_vars)

    names = list(local_vars[key].keys())
    return prefixes + names

WEBUI_SELECTION = {
    'A1111':   "--xformers --no-half-vae",
    'ComfyUI': "--dont-print-server",
    'Forge':   "--xformers --cuda-stream",              # Remove: --disable-xformers --opt-sdp-attention --pin-shared-memory
    'Classic': "--persistent-patches --cuda-stream",    # Remove: --xformers --pin-shared-memory
    'ReForge': "--xformers --cuda-stream",              # Remove: --pin-shared-memory
    'SD-UX':   "--xformers --no-half-vae"
}

# Initialize the WidgetFactory
factory = WidgetFactory()
HR = widgets.HTML('<hr>')

# --- MODEL ---
"""Create model selection widgets."""
model_header = factory.create_header('Model Selection')
model_options = read_model_data(f"{SCRIPTS}/_models-data.py", 'model')
inpainting_model_widget = factory.create_checkbox('Inpainting Models', False, class_names=['inpaint'], layout={'width': '250px'})
XL_models_widget = factory.create_checkbox('SDXL', False, class_names=['sdxl'])

switch_model_widget = factory.create_hbox([inpainting_model_widget, XL_models_widget])

# --- VAE ---
"""Create VAE selection widgets."""
vae_header = factory.create_header('VAE Selection')
vae_options = read_model_data(f"{SCRIPTS}/_models-data.py", 'vae')

# --- TABBED DOWNLOAD SYSTEM ---
"""Create tabbed download interface for Models, VAE, LoRA, and ControlNet."""

# Tab buttons
tab_models = factory.create_button('Models', class_names=['tab-button', 'active'])
tab_vae = factory.create_button('VAE', class_names=['tab-button'])
tab_lora = factory.create_button('LoRA', class_names=['tab-button'])
tab_controlnet = factory.create_button('ControlNet', class_names=['tab-button'])

tab_container = factory.create_hbox([tab_models, tab_vae, tab_lora, tab_controlnet], class_names=['tab-container'])

# Tab content containers
tab_content_models = factory.create_vbox([], class_names=['tab-content', 'active'])
tab_content_vae = factory.create_vbox([], class_names=['tab-content'])
tab_content_lora = factory.create_vbox([], class_names=['tab-content'])
tab_content_controlnet = factory.create_vbox([], class_names=['tab-content'])

# Create toggle buttons for each type
def create_toggle_buttons(data_type, options):
    """Create toggle buttons for a given data type."""
    buttons = []
    for option in options:
        if option not in ['none', 'ALL']:
            button = factory.create_button(option, class_names=['toggle-button', data_type])
            buttons.append(button)
    return buttons

# Generate toggle buttons for each tab
model_toggle_buttons = create_toggle_buttons('model', model_options)
vae_toggle_buttons = create_toggle_buttons('vae', vae_options)
lora_options = read_model_data(f"{SCRIPTS}/_models-data.py", 'lora')
lora_toggle_buttons = create_toggle_buttons('lora', lora_options)
controlnet_options = read_model_data(f"{SCRIPTS}/_models-data.py", 'cnet')
controlnet_toggle_buttons = create_toggle_buttons('controlnet', controlnet_options)

# Add toggle buttons to tab contents
tab_content_models.children = model_toggle_buttons
tab_content_vae.children = vae_toggle_buttons
tab_content_lora.children = lora_toggle_buttons
tab_content_controlnet.children = controlnet_toggle_buttons

# Tab switching function
def switch_tab(button):
    """Switch between tabs and update content."""
    tabs = [tab_models, tab_vae, tab_lora, tab_controlnet]
    contents = [tab_content_models, tab_content_vae, tab_content_lora, tab_content_controlnet]
    
    # Remove active class from all tabs and contents
    for tab, content in zip(tabs, contents):
        tab.remove_class('active')
        content.remove_class('active')
    
    # Add active class to clicked tab and corresponding content
    button.add_class('active')
    tab_index = tabs.index(button)
    contents[tab_index].add_class('active')

# Toggle button function
def toggle_button(button):
    """Toggle button state on/off."""
    # Use a custom attribute to track toggle state
    if not hasattr(button, '_is_active'):
        button._is_active = False
    
    button._is_active = not button._is_active
    
    if button._is_active:
        button.add_class('active')
    else:
        button.remove_class('active')

# Connect tab buttons to switch function
tab_models.on_click(switch_tab)
tab_vae.on_click(switch_tab)
tab_lora.on_click(switch_tab)
tab_controlnet.on_click(switch_tab)

# Connect all toggle buttons to toggle function
for button in model_toggle_buttons:
    button.on_click(toggle_button)
for button in vae_toggle_buttons:
    button.on_click(toggle_button)
for button in lora_toggle_buttons:
    button.on_click(toggle_button)
for button in controlnet_toggle_buttons:
    button.on_click(toggle_button)

# Download tabs container
download_tabs_container = factory.create_vbox(
    [tab_container, tab_content_models, tab_content_vae, tab_content_lora, tab_content_controlnet],
    class_names=['download-tabs-container']
)

# --- ADDITIONAL ---
"""Create additional configuration widgets."""
additional_header = factory.create_header('Additionally')
latest_webui_widget = factory.create_checkbox('Update WebUI', True)
latest_extensions_widget = factory.create_checkbox('Update Extensions', True)
check_custom_nodes_deps_widget = factory.create_checkbox('Check Custom-Nodes Dependencies', True)
change_webui_widget = factory.create_dropdown(list(WEBUI_SELECTION.keys()), 'WebUI:', 'A1111', layout={'width': 'auto'})
detailed_download_widget = factory.create_dropdown(['off', 'on'], 'Detailed Download:', 'off', layout={'width': 'auto'})
choose_changes_box = factory.create_hbox(
    [
        latest_webui_widget,
        latest_extensions_widget,
        check_custom_nodes_deps_widget,   # Only ComfyUI
        change_webui_widget,
        detailed_download_widget
    ],
    layout={'justify_content': 'space-between'}
)

controlnet_options = read_model_data(f"{SCRIPTS}/_models-data.py", 'cnet')
commit_hash_widget = factory.create_text('Commit Hash:', '', 'Switching between branches or commits.')

civitai_token_widget = factory.create_text('CivitAI Token:', '', 'Enter your CivitAi API token.')
civitai_button = create_expandable_button('Get CivitAI Token', 'https://civitai.com/user/account')
civitai_box = factory.create_hbox([civitai_token_widget, civitai_button])

huggingface_token_widget = factory.create_text('HuggingFace Token:')
huggingface_button = create_expandable_button('Get HuggingFace Token', 'https://huggingface.co/settings/tokens')
huggingface_box = factory.create_hbox([huggingface_token_widget, huggingface_button])

ngrok_token_widget = factory.create_text('Ngrok Token:')
ngrok_button = create_expandable_button('Get Ngrok Token', 'https://dashboard.ngrok.com/get-started/your-authtoken')
ngrok_box = factory.create_hbox([ngrok_token_widget, ngrok_button])

zrok_token_widget = factory.create_text('Zrok Token:')
zrok_button = create_expandable_button('Register Zrok Token', 'https://colab.research.google.com/drive/1d2sjWDJi_GYBUavrHSuQyHTDuLy36WpU')
zrok_box = factory.create_hbox([zrok_token_widget, zrok_button])

commandline_arguments_widget = factory.create_text('Arguments:', WEBUI_SELECTION['A1111'])

accent_colors_options = ['scarysingle', 'blue', 'green', 'peach', 'pink', 'red', 'yellow']
theme_accent_widget = factory.create_dropdown(accent_colors_options, 'Theme Accent:', 'scarysingle',
                                              layout={'width': 'auto', 'margin': '0 0 0 8px'})    # margin-left

additional_footer_box = factory.create_hbox([commandline_arguments_widget, theme_accent_widget])

additional_widget_list = [
    additional_header,
    choose_changes_box,
    HR,
    commit_hash_widget,
    civitai_box, huggingface_box, zrok_box, ngrok_box,
    HR,
    # commandline_arguments_widget,
    additional_footer_box
]

# --- CUSTOM DOWNLOAD ---
"""Create Custom-Download Selection widgets."""
custom_download_header_popup = factory.create_html('''
<div class="header" style="cursor: pointer;" onclick="toggleContainer()">Custom Download</div>
<div class="info">INFO</div>
<div class="popup">
    Separate multiple URLs with a comma/space.
    For a <span class="file_name">custom name</span> file/extension, specify it with <span class="braces">[ ]</span> after the URL without spaces.
    <span style="color: #ff9999">For files, be sure to specify</span> - <span class="extension">Filename Extension.</span>
    <div class="sample">
        <span class="sample_label">Example for File:</span>
        https://civitai.com/api/download/models/229782<span class="braces">[</span><span class="file_name">Detailer</span><span class="extension">.safetensors</span><span class="braces">]</span>
        <br>
        <span class="sample_label">Example for Extension:</span>
        https://github.com/hako-mikan/sd-webui-regional-prompter<span class="braces">[</span><span class="file_name">Regional-Prompter</span><span class="braces">]</span>
    </div>
</div>
''')

empowerment_widget = factory.create_checkbox('Empowerment', False, class_names=['empowerment'])
empowerment_output_widget = factory.create_textarea(
'', '', """Use special tags. Portable analog of "File (txt)"
Tags: model (ckpt), vae, lora, embed (emb), extension (ext), adetailer (ad), control (cnet), upscale (ups), clip, unet, vision (vis), encoder (enc), diffusion (diff), config (cfg)
Short tags: start with '$' without a space -> $ckpt
------ Example ------

# Lora
https://civitai.com/api/download/models/229782

$ext
https://github.com/hako-mikan/sd-webui-cd-tuner[CD-Tuner]
""")

Model_url_widget = factory.create_text('Model:')
Vae_url_widget = factory.create_text('Vae:')
LoRA_url_widget = factory.create_text('LoRa:')
Embedding_url_widget = factory.create_text('Embedding:')
Extensions_url_widget = factory.create_text('Extensions:')
ADetailer_url_widget = factory.create_text('ADetailer:')
custom_file_urls_widget = factory.create_text('File (txt):')

# --- Enhanced Save Button with Textured Text ---
"""Create enhanced save button with textured styling."""
save_button_html = factory.create_html('''
<button class="button button_save">
    <span class="button-text">Save</span>
</button>
''')

# ===================== Enhanced Side Container =====================
# --- Simplified Top Bar with Only Utility Buttons ---
"""Create clean top bar with only utility buttons, VAE moved to download tabs."""

# Enhanced utility buttons
BTN_STYLE = {'width': '36px', 'height': '36px'}
TOOLTIPS = ("Unmount Google Drive storage", "Mount Google Drive storage")

GD_status = js.read(SETTINGS_PATH, 'mountGDrive', False)
GDrive_button = factory.create_button('', layout=BTN_STYLE, class_names=['utility-button', 'gdrive-button'])
GDrive_button.tooltip = TOOLTIPS[not GD_status]
gdrive_toggle_state = GD_status

export_button = factory.create_button('', layout=BTN_STYLE, class_names=['utility-button', 'export-button'])
export_button.tooltip = "Export settings to JSON"

import_button = factory.create_button('', layout=BTN_STYLE, class_names=['utility-button', 'import-button'])
import_button.tooltip = "Import settings from JSON"

# Create simplified top bar layout - only utility buttons
top_bar_container = factory.create_hbox([
    GDrive_button, export_button, import_button
], class_names=['top-bar-container', 'utility-only'])

# Handle environment-specific visibility
if ENV_NAME != 'Google Colab':
    if hasattr(GDrive_button, 'layout') and hasattr(GDrive_button.layout, 'display'):
        GDrive_button.layout.display = 'none'
    if hasattr(export_button, 'layout') and hasattr(export_button.layout, 'display'):
        export_button.layout.display = 'none'
    if hasattr(import_button, 'layout') and hasattr(import_button.layout, 'display'):
        import_button.layout.display = 'none'
else:
    if GD_status:
        GDrive_button.add_class('active')

    def handle_toggle(btn):
        """Toggle Google Drive button state"""
        global gdrive_toggle_state
        gdrive_toggle_state = not gdrive_toggle_state
        
        if hasattr(btn, 'tooltip'):
            btn.tooltip = TOOLTIPS[not gdrive_toggle_state]
        
        if gdrive_toggle_state:
            btn.add_class('active')
        else:
            btn.remove_class('active')

    GDrive_button.on_click(handle_toggle)

# EXPORT
def export_settings(button=None, filter_empty=False):
    try:
        widgets_data = {}
        for key in SETTINGS_KEYS:
            value = globals()[f"{key}_widget"].value
            if not filter_empty or (value not in [None, '', False]):
                widgets_data[key] = value

        settings_data = {
            'widgets': widgets_data,
            # 'mountGDrive': gdrive_toggle_state
        }

        display(Javascript(f'downloadJson({json.dumps(settings_data)});'))
        show_notification("Settings exported successfully!", "success")
    except Exception as e:
        show_notification(f"Export failed: {str(e)}", "error")

# IMPORT

def import_settings(button=None):
    display(Javascript('openFilePicker();'))

# APPLY SETTINGS
def apply_imported_settings(data):
    try:
        success_count = 0
        total_count = 0

        if 'widgets' in data:
            for key, value in data['widgets'].items():
                total_count += 1
                if key in SETTINGS_KEYS and f"{key}_widget" in globals():
                    try:
                        globals()[f"{key}_widget"].value = value
                        success_count += 1
                    except:
                        pass

        if 'mountGDrive' in data:
            global gdrive_toggle_state
            gdrive_toggle_state = data['mountGDrive']
            if gdrive_toggle_state:
                GDrive_button.add_class('active')
            else:
                GDrive_button.remove_class('active')

        if success_count == total_count:
            show_notification("Settings imported successfully!", "success")
        else:
            show_notification(f"Imported {success_count}/{total_count} settings", "warning")

    except Exception as e:
        show_notification(f"Import failed: {str(e)}", "error")
        pass

# === NOTIFICATION for Export/Import ===
"""Create widget-popup displaying status of Export/Import settings."""
notification_popup = factory.create_html('', class_names=['notification-popup', 'hidden'])

def show_notification(message, message_type='info'):
    icon_map = {
        'success':  '✅',
        'error':    '❌',
        'info':     '💡',
        'warning':  '⚠️'
    }
    icon = icon_map.get(message_type, 'info')

    notification_popup.value = f'''
    <div class="notification {message_type}">
        <span class="notification-icon">{icon}</span>
        <span class="notification-text">{message}</span>
    </div>
    '''

    # Trigger re-show | Anxety-Tip: JS Script removes class only from DOM but not from widgets?!
    notification_popup.remove_class('visible')
    notification_popup.remove_class('hidden')
    notification_popup.add_class('visible')

    # Auto-hide PopUp After 2.5s
    display(Javascript("hideNotification(delay = 2500);"))

# REGISTER CALLBACK
"""
Registers the Python function 'apply_imported_settings' under the name 'importSettingsFromJS'
so it can be called from JavaScript via google.colab.kernel.invokeFunction(...)
"""
output.register_callback('importSettingsFromJS', apply_imported_settings)
output.register_callback('showNotificationFromJS', show_notification)

export_button.on_click(export_settings)
import_button.on_click(import_settings)


# =================== DISPLAY / SETTINGS ===================

factory.load_css(widgets_css)   # load CSS (widgets)
factory.load_js(widgets_js)     # load JS (widgets)

# === CREATE ELEGANT ACCORDION TAB SYSTEM ===
"""Create accordion tabs for Custom Download and Additionally sections."""

# Custom Download accordion tab
custom_download_header = factory.create_html('''
<div class="accordion-header">
    <h3>Custom Download</h3>
    <div class="accordion-toggle">▼</div>
</div>
''')

custom_download_content_widgets = [
    empowerment_widget,
    empowerment_output_widget,
    Model_url_widget,
    Vae_url_widget,
    LoRA_url_widget,
    Embedding_url_widget,
    Extensions_url_widget,
    ADetailer_url_widget,
    custom_file_urls_widget
]

custom_download_content = factory.create_vbox(
    custom_download_content_widgets,
    class_names=['accordion-content']
)

custom_download_tab = factory.create_vbox(
    [custom_download_header, custom_download_content],
    class_names=['accordion-tab', 'expanded']
)

# Advanced Settings accordion tab
advanced_settings_header = factory.create_html('''
<div class="accordion-header">
    <h3>Advanced Settings</h3>
    <div class="accordion-toggle">▼</div>
</div>
''')

advanced_settings_content = factory.create_vbox(
    additional_widget_list,
    class_names=['accordion-content']
)

advanced_settings_tab = factory.create_vbox(
    [advanced_settings_header, advanced_settings_content],
    class_names=['accordion-tab', 'collapsed']
)

# Accordion container - 50/50 split
accordion_container = factory.create_hbox(
    [custom_download_tab, advanced_settings_tab],
    class_names=['accordion-container']
)

# Enhanced layout structure - COMPLETELY FIXED
CONTAINERS_WIDTH = '1080px'

# Clean model selection section - compact layout
model_selection_section = factory.create_vbox([
    model_header,
    switch_model_widget
], class_names=['container', 'model-selection'])

# Clean download section with tabs
download_section = factory.create_vbox([
    factory.create_header('Download Selection'),
    download_tabs_container
], class_names=['container', 'download-section'])

widgetContainer = factory.create_vbox(
    [
        top_bar_container,
        model_selection_section,
        download_section,
        accordion_container,
        save_button_html
    ],
    class_names=['widgetContainer'],
    layout={'min_width': CONTAINERS_WIDTH, 'max_width': CONTAINERS_WIDTH}
)

sideContainer = factory.create_vbox(
    [notification_popup],
    class_names=['sideContainer']
)

mainContainer = factory.create_hbox(
    [widgetContainer, sideContainer],
    class_names=['mainContainer'],
    layout={'align_items': 'flex-start'}
)

factory.display(mainContainer)


# ==================== CALLBACK FUNCTION ===================

# Initialize visibility | hidden
if hasattr(check_custom_nodes_deps_widget, 'layout') and hasattr(check_custom_nodes_deps_widget.layout, 'display'):
    check_custom_nodes_deps_widget.layout.display = 'none'
empowerment_output_widget.add_class('empowerment-output')
empowerment_output_widget.add_class('hidden')

# Callback functions for XL options
def update_XL_options(change, widget):
    is_xl = change['new']
    
    data_file = '_xl-models-data.py' if is_xl else '_models-data.py'
    
    # Update toggle buttons with new options
    new_model_options = read_model_data(f"{SCRIPTS}/{data_file}", 'model')
    new_vae_options = read_model_data(f"{SCRIPTS}/{data_file}", 'vae')
    new_controlnet_options = read_model_data(f"{SCRIPTS}/{data_file}", 'cnet')
    new_lora_options = read_model_data(f"{SCRIPTS}/{data_file}", 'lora')
    
    # Clear existing toggle buttons
    tab_content_models.children = []
    tab_content_vae.children = []
    tab_content_controlnet.children = []
    tab_content_lora.children = []
    
    # Create new toggle buttons with updated options
    global model_toggle_buttons, vae_toggle_buttons, controlnet_toggle_buttons, lora_toggle_buttons
    model_toggle_buttons = create_toggle_buttons('model', new_model_options)
    vae_toggle_buttons = create_toggle_buttons('vae', new_vae_options)
    controlnet_toggle_buttons = create_toggle_buttons('controlnet', new_controlnet_options)
    lora_toggle_buttons = create_toggle_buttons('lora', new_lora_options)
    
    # Add new toggle buttons to tab contents
    tab_content_models.children = model_toggle_buttons
    tab_content_vae.children = vae_toggle_buttons
    tab_content_controlnet.children = controlnet_toggle_buttons
    tab_content_lora.children = lora_toggle_buttons
    
    # Connect new toggle buttons to toggle function
    for button in model_toggle_buttons:
        button.on_click(toggle_button)
    for button in vae_toggle_buttons:
        button.on_click(toggle_button)
    for button in controlnet_toggle_buttons:
        button.on_click(toggle_button)
    for button in lora_toggle_buttons:
        button.on_click(toggle_button)
    
    # Disable/enable inpainting checkbox based on SDXL state
    if is_xl:
        inpainting_model_widget.add_class('_disable')
        inpainting_model_widget.value = False
    else:
        inpainting_model_widget.remove_class('_disable')

# Callback functions for updating widgets
def update_change_webui(change, widget):
    webui = change['new']
    commandline_arguments_widget.value = WEBUI_SELECTION.get(webui, '')

    is_comfy = webui == 'ComfyUI'

    if hasattr(latest_extensions_widget, 'layout') and hasattr(latest_extensions_widget.layout, 'display'):
        latest_extensions_widget.layout.display = 'none' if is_comfy else ''
    latest_extensions_widget.value = not is_comfy
    if hasattr(check_custom_nodes_deps_widget, 'layout') and hasattr(check_custom_nodes_deps_widget.layout, 'display'):
        check_custom_nodes_deps_widget.layout.display = '' if is_comfy else 'none'
    if hasattr(theme_accent_widget, 'layout') and hasattr(theme_accent_widget.layout, 'display'):
        theme_accent_widget.layout.display = 'none' if is_comfy else ''
    Extensions_url_widget.description = 'Custom Nodes:' if is_comfy else 'Extensions:'

# Callback functions for Empowerment
def update_empowerment(change, widget):
    selected_emp = change['new']

    customDL_widgets = [
        Model_url_widget,
        Vae_url_widget,
        LoRA_url_widget,
        Embedding_url_widget,
        Extensions_url_widget,
        ADetailer_url_widget
    ]
    for widget in customDL_widgets:    # For switching animation
        widget.add_class('empowerment-text-field')

    # idk why, but that's the way it's supposed to be >_<'
    if selected_emp:
        for wg in customDL_widgets:
            wg.add_class('hidden')
        empowerment_output_widget.remove_class('hidden')
    else:
        for wg in customDL_widgets:
            wg.remove_class('hidden')
        empowerment_output_widget.add_class('hidden')

# Connecting widgets
factory.connect_widgets([(change_webui_widget, 'value')], update_change_webui)
factory.connect_widgets([(XL_models_widget, 'value')], update_XL_options)
factory.connect_widgets([(empowerment_widget, 'value')], update_empowerment)


# ================ Load / Save - Settings V4 ===============

SETTINGS_KEYS = [
      'XL_models', 'inpainting_model',
      # Additional
      'latest_webui', 'latest_extensions', 'check_custom_nodes_deps', 'change_webui', 'detailed_download',
      'commit_hash',
      'civitai_token', 'huggingface_token', 'zrok_token', 'ngrok_token', 'commandline_arguments', 'theme_accent',
      # CustomDL
      'empowerment', 'empowerment_output',
      'Model_url', 'Vae_url', 'LoRA_url', 'Embedding_url', 'Extensions_url', 'ADetailer_url',
      'custom_file_urls'
]

def save_toggle_button_states():
    """Save the active states of toggle buttons."""
    toggle_states = {}
    
    # Save model toggle states
    for i, button in enumerate(model_toggle_buttons):
        if hasattr(button, '_is_active'):
            toggle_states[f'model_toggle_{i}'] = button._is_active
    
    # Save vae toggle states
    for i, button in enumerate(vae_toggle_buttons):
        if hasattr(button, '_is_active'):
            toggle_states[f'vae_toggle_{i}'] = button._is_active
            
    # Save lora toggle states
    for i, button in enumerate(lora_toggle_buttons):
        if hasattr(button, '_is_active'):
            toggle_states[f'lora_toggle_{i}'] = button._is_active
            
    # Save controlnet toggle states
    for i, button in enumerate(controlnet_toggle_buttons):
        if hasattr(button, '_is_active'):
            toggle_states[f'controlnet_toggle_{i}'] = button._is_active
    
    js.save(SETTINGS_PATH, 'TOGGLE_STATES', toggle_states)

def load_toggle_button_states():
    """Load the active states of toggle buttons."""
    if not js.key_exists(SETTINGS_PATH, 'TOGGLE_STATES'):
        return
        
    toggle_states = js.read(SETTINGS_PATH, 'TOGGLE_STATES')
    
    # Load model toggle states
    for i, button in enumerate(model_toggle_buttons):
        state_key = f'model_toggle_{i}'
        if state_key in toggle_states and toggle_states[state_key]:
            button._is_active = True
            button.add_class('active')
    
    # Load vae toggle states
    for i, button in enumerate(vae_toggle_buttons):
        state_key = f'vae_toggle_{i}'
        if state_key in toggle_states and toggle_states[state_key]:
            button._is_active = True
            button.add_class('active')
            
    # Load lora toggle states
    for i, button in enumerate(lora_toggle_buttons):
        state_key = f'lora_toggle_{i}'
        if state_key in toggle_states and toggle_states[state_key]:
            button._is_active = True
            button.add_class('active')
            
    # Load controlnet toggle states
    for i, button in enumerate(controlnet_toggle_buttons):
        state_key = f'controlnet_toggle_{i}'
        if state_key in toggle_states and toggle_states[state_key]:
            button._is_active = True
            button.add_class('active')

def save_settings():
    """Save widget values to settings."""
    widgets_values = {key: globals()[f"{key}_widget"].value for key in SETTINGS_KEYS}
    js.save(SETTINGS_PATH, 'WIDGETS', widgets_values)
    js.save(SETTINGS_PATH, 'mountGDrive', True if gdrive_toggle_state else False)  # Save Status GDrive-btn

    update_current_webui(change_webui_widget.value)  # Update Selected WebUI in settings.json

def load_settings():
    """Load widget values from settings."""
    if js.key_exists(SETTINGS_PATH, 'WIDGETS'):
        widget_data = js.read(SETTINGS_PATH, 'WIDGETS')
        for key in SETTINGS_KEYS:
            if key in widget_data:
                globals()[f"{key}_widget"].value = widget_data.get(key, '')

    # Load Status GDrive-btn
    GD_status = js.read(SETTINGS_PATH, 'mountGDrive', False)
    global gdrive_toggle_state
    gdrive_toggle_state = (GD_status == True)
    if gdrive_toggle_state:
        GDrive_button.add_class('active')
    else:
        GDrive_button.remove_class('active')

def save_data(button=None):
    """Handle save button click."""
    # Save toggle button states before saving settings
    save_toggle_button_states()
    save_settings()
    
    # Close the main container (this will close all child widgets)
    factory.close([mainContainer], class_names=['hide'], delay=0.8)

# Add JavaScript for accordion functionality and enhanced button interactions
accordion_js = """
// Enhanced Accordion Tab Functionality
function initializeAccordion() {
    const accordionTabs = document.querySelectorAll('.accordion-tab');
    const accordionHeaders = document.querySelectorAll('.accordion-header');
    
    // Set initial state - first tab expanded by default
    if (accordionTabs.length > 0) {
        accordionTabs[0].classList.add('expanded');
        accordionTabs[0].classList.remove('collapsed');
        
        // Set all others as collapsed
        for (let i = 1; i < accordionTabs.length; i++) {
            accordionTabs[i].classList.add('collapsed');
            accordionTabs[i].classList.remove('expanded');
        }
    }
    
    accordionHeaders.forEach((header, index) => {
        header.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const tab = this.parentElement;
            const isExpanded = tab.classList.contains('expanded');
            
            // Always allow toggle - either collapse current or expand clicked
            accordionTabs.forEach(t => {
                t.classList.remove('expanded');
                t.classList.add('collapsed');
            });
            
            // Expand clicked tab if it wasn't already expanded
            if (!isExpanded) {
                tab.classList.remove('collapsed');
                tab.classList.add('expanded');
            }
        });
    });
}

// Enhanced Button Click Handler
function setupEnhancedButtons() {
    document.addEventListener('click', function(e) {
        if (e.target.closest('.button_save')) {
            // Handle save button with textured styling
            const button = e.target.closest('.button_save');
            const buttonText = button.querySelector('.button-text');
            if (buttonText) {
                buttonText.classList.add('expanding');
                setTimeout(() => buttonText.classList.remove('expanding'), 800);
            }
            
            // Trigger Python save function
            if (typeof google !== 'undefined' && google.colab && google.colab.kernel) {
                google.colab.kernel.invokeFunction('notebook.save_data_js', [], {});
            }
        }
    });
}

// Initialize when DOM is ready
function initializeWidgets() {
    initializeAccordion();
    setupEnhancedButtons();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(initializeWidgets, 1000);
    });
} else {
    setTimeout(initializeWidgets, 1000);
}
"""

# Register the enhanced save function for JS callback
output.register_callback('notebook.save_data_js', save_data)

# Load JavaScript for enhanced functionality
display(Javascript(accordion_js))

load_settings()
load_toggle_button_states()