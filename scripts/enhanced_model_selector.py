#!/usr/bin/env python3
"""
Enhanced Multi-Model Selection Interface (V3)
Sophisticated UX for selecting multiple models with advanced filtering and batch operations

Features:
- Smart categorization with emoji indicators
- Advanced search and filtering capabilities
- Batch operations (select all, clear all, category selection)
- Model comparison and rating system
- Visual feedback with sanguine color scheme
- Cloud GPU environment optimizations
- Progress tracking for selections
"""

import ipywidgets as widgets
from IPython.display import display, HTML, Javascript
import json
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from pathlib import Path
import re
import time

# Import our enhanced LoRA data
import sys
sys.path.append(str(Path(__file__).parent))

try:
    from _models_data import lora_data
    from _xl_models_data import xl_lora_data
except ImportError:
    # Fallback mock data for testing
    lora_data = {}
    xl_lora_data = {}


@dataclass
class ModelInfo:
    """Enhanced model information structure"""
    name: str
    category: str
    description: str
    size: str
    rating: float
    tags: List[str]
    download_url: str
    preview_url: Optional[str] = None
    compatibility: List[str] = field(default_factory=lambda: ["SD1.5"])
    nsfw_level: int = 0
    popularity_score: int = 0
    last_updated: Optional[str] = None
    
    def matches_search(self, query: str) -> bool:
        """Check if model matches search query"""
        query_lower = query.lower()
        return (
            query_lower in self.name.lower() or
            query_lower in self.description.lower() or
            any(query_lower in tag.lower() for tag in self.tags)
        )
    
    def matches_filters(self, filters: Dict[str, Any]) -> bool:
        """Check if model matches active filters"""
        if filters.get('category') and filters['category'] != 'all':
            if self.category != filters['category']:
                return False
        
        if filters.get('rating_min'):
            if self.rating < filters['rating_min']:
                return False
        
        if filters.get('compatibility') and filters['compatibility'] != 'all':
            if filters['compatibility'] not in self.compatibility:
                return False
        
        if filters.get('nsfw_filter') and not filters.get('show_nsfw', False):
            if self.nsfw_level > 2:
                return False
        
        return True


class EnhancedModelSelector:
    """Sophisticated multi-model selection interface"""
    
    def __init__(self, model_type: str = "lora", callback: Optional[Callable] = None):
        self.model_type = model_type
        self.callback = callback
        self.selected_models: Dict[str, ModelInfo] = {}
        self.filtered_models: List[ModelInfo] = []
        self.all_models: List[ModelInfo] = []
        
        # UI Components
        self.search_box = None
        self.category_filter = None
        self.rating_filter = None
        self.compatibility_filter = None
        self.model_grid = None
        self.selection_summary = None
        self.batch_controls = None
        self.progress_bar = None
        
        # Load model data
        self._load_model_data()
        
        # Initialize UI
        self._create_interface()
    
    def _load_model_data(self):
        """Load and process model data"""
        raw_data = lora_data if self.model_type == "lora" else xl_lora_data
        
        for category, models in raw_data.items():
            for model_key, model_data in models.items():
                if isinstance(model_data, dict):
                    model_info = ModelInfo(
                        name=model_data.get('name', model_key),
                        category=category,
                        description=model_data.get('description', ''),
                        size=model_data.get('size', 'Unknown'),
                        rating=model_data.get('rating', 4.0),
                        tags=model_data.get('tags', []),
                        download_url=model_data.get('url', ''),
                        preview_url=model_data.get('preview', None),
                        compatibility=model_data.get('compatibility', ['SD1.5']),
                        nsfw_level=model_data.get('nsfw_level', 0),
                        popularity_score=model_data.get('popularity', 0)
                    )
                    self.all_models.append(model_info)
        
        # Sort by popularity and rating
        self.all_models.sort(key=lambda x: (x.popularity_score, x.rating), reverse=True)
        self.filtered_models = self.all_models.copy()
    
    def _create_interface(self):
        """Create the enhanced model selection interface"""
        # Header with title and summary
        header = self._create_header()
        
        # Search and filtering controls
        search_filters = self._create_search_and_filters()
        
        # Batch operation controls
        batch_controls = self._create_batch_controls()
        
        # Progress indicator
        self.progress_bar = widgets.IntProgress(
            value=0,
            min=0,
            max=100,
            description='Selection:',
            bar_style='info',
            style={'bar_color': '#DC143C', 'description_width': 'initial'},
            layout=widgets.Layout(width='100%')
        )
        
        # Model grid
        self.model_grid = self._create_model_grid()
        
        # Selection summary
        self.selection_summary = self._create_selection_summary()
        
        # Main container with sanguine styling
        self.main_container = widgets.VBox([
            header,
            search_filters,
            batch_controls,
            self.progress_bar,
            self.model_grid,
            self.selection_summary
        ], layout=widgets.Layout(
            border='2px solid #8B0000',
            border_radius='8px',
            padding='16px',
            background_color='rgba(139, 0, 0, 0.05)',
            width='100%'
        ))
    
    def _create_header(self) -> widgets.Widget:
        """Create header with title and info"""
        title_html = f"""
        <div style="text-align: center; margin-bottom: 16px;">
            <h2 style="color: #8B0000; font-family: 'Cinzel', serif; margin: 0;">
                🎨 Enhanced {self.model_type.upper()} Selection
            </h2>
            <p style="color: #DC143C; font-family: 'Inter', sans-serif; margin: 8px 0;">
                Select multiple models with advanced filtering and batch operations
            </p>
        </div>
        """
        return widgets.HTML(value=title_html)
    
    def _create_search_and_filters(self) -> widgets.Widget:
        """Create search box and filter controls"""
        # Search box with enhanced styling
        self.search_box = widgets.Text(
            placeholder="🔍 Search models by name, description, or tags...",
            description="",
            style={'description_width': '0px'},
            layout=widgets.Layout(width='100%', margin='0 0 8px 0')
        )
        self.search_box.observe(self._on_search_change, names='value')
        
        # Category filter
        categories = ['all'] + list(set(model.category for model in self.all_models))
        self.category_filter = widgets.Dropdown(
            options=[(cat.replace('_', ' ').title(), cat) for cat in categories],
            value='all',
            description='Category:',
            style={'description_width': '80px'},
            layout=widgets.Layout(width='200px')
        )
        self.category_filter.observe(self._on_filter_change, names='value')
        
        # Rating filter
        self.rating_filter = widgets.FloatSlider(
            value=0.0,
            min=0.0,
            max=5.0,
            step=0.5,
            description='Min Rating:',
            style={'description_width': '80px', 'handle_color': '#DC143C'},
            layout=widgets.Layout(width='200px')
        )
        self.rating_filter.observe(self._on_filter_change, names='value')
        
        # Compatibility filter
        compatibility_options = [
            ('All Models', 'all'),
            ('SD 1.5', 'SD1.5'),
            ('SDXL', 'SDXL'),
            ('SD 2.x', 'SD2')
        ]
        self.compatibility_filter = widgets.Dropdown(
            options=compatibility_options,
            value='all',
            description='Compatible:',
            style={'description_width': '80px'},
            layout=widgets.Layout(width='150px')
        )
        self.compatibility_filter.observe(self._on_filter_change, names='value')
        
        # NSFW filter
        self.nsfw_toggle = widgets.Checkbox(
            value=False,
            description='Show NSFW',
            style={'description_width': 'initial'}
        )
        self.nsfw_toggle.observe(self._on_filter_change, names='value')
        
        filters_row = widgets.HBox([
            self.category_filter,
            self.rating_filter,
            self.compatibility_filter,
            self.nsfw_toggle
        ], layout=widgets.Layout(justify_content='space-between', margin='8px 0'))
        
        return widgets.VBox([self.search_box, filters_row])
    
    def _create_batch_controls(self) -> widgets.Widget:
        """Create batch operation controls"""
        # Batch operation buttons with sanguine styling
        select_all_btn = widgets.Button(
            description="Select All",
            button_style="",
            tooltip="Select all visible models",
            layout=widgets.Layout(width='120px'),
            style={'button_color': '#DC143C', 'text_color': 'white'}
        )
        select_all_btn.on_click(lambda b: self._batch_select_all())
        
        clear_all_btn = widgets.Button(
            description="Clear All",
            button_style="",
            tooltip="Clear all selections",
            layout=widgets.Layout(width='120px'),
            style={'button_color': '#8B0000', 'text_color': 'white'}
        )
        clear_all_btn.on_click(lambda b: self._batch_clear_all())
        
        invert_btn = widgets.Button(
            description="Invert",
            button_style="",
            tooltip="Invert current selection",
            layout=widgets.Layout(width='120px'),
            style={'button_color': '#FF6B6B', 'text_color': 'white'}
        )
        invert_btn.on_click(lambda b: self._batch_invert())
        
        # Category-specific selection
        select_category_btn = widgets.Button(
            description="Select Category",
            button_style="",
            tooltip="Select all models in current category",
            layout=widgets.Layout(width='140px'),
            style={'button_color': '#B22222', 'text_color': 'white'}
        )
        select_category_btn.on_click(lambda b: self._batch_select_category())
        
        batch_controls = widgets.HBox([
            select_all_btn,
            clear_all_btn,
            invert_btn,
            select_category_btn
        ], layout=widgets.Layout(
            justify_content='center',
            margin='8px 0',
            border='1px solid #DC143C',
            border_radius='4px',
            padding='8px'
        ))
        
        return batch_controls
    
    def _create_model_grid(self) -> widgets.Widget:
        """Create scrollable model grid"""
        self.model_checkboxes = {}
        self.model_cards = []
        
        # Create initial model cards
        self._update_model_grid()
        
        # Container with scroll
        grid_container = widgets.VBox(
            self.model_cards,
            layout=widgets.Layout(
                height='400px',
                overflow='auto',
                border='1px solid #DC143C',
                border_radius='4px',
                padding='8px'
            )
        )
        
        return grid_container
    
    def _create_model_card(self, model: ModelInfo) -> widgets.Widget:
        """Create individual model card"""
        # Model selection checkbox
        checkbox = widgets.Checkbox(
            value=False,
            description="",
            layout=widgets.Layout(width='30px')
        )
        checkbox.observe(lambda change, m=model: self._on_model_toggle(change, m), names='value')
        self.model_checkboxes[model.name] = checkbox
        
        # Rating stars
        stars = "⭐" * int(model.rating) + "☆" * (5 - int(model.rating))
        
        # Compatibility badges
        compat_badges = " ".join([
            f"<span style='background: #DC143C; color: white; padding: 2px 6px; border-radius: 3px; font-size: 10px;'>{comp}</span>"
            for comp in model.compatibility
        ])
        
        # Model info HTML
        info_html = f"""
        <div style="
            background: linear-gradient(135deg, rgba(139,0,0,0.1), rgba(220,20,60,0.05));
            border: 1px solid rgba(139,0,0,0.3);
            border-radius: 6px;
            padding: 12px;
            margin: 4px 0;
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <h4 style="color: #8B0000; margin: 0; font-family: 'Inter', sans-serif; font-size: 14px;">
                    {model.category.replace('_', ' ').title()} • {model.name}
                </h4>
                <div style="color: #DC143C; font-size: 12px;">{stars} {model.rating:.1f}/5.0</div>
            </div>
            <p style="color: #666; margin: 6px 0; font-size: 12px; line-height: 1.4;">
                {model.description[:150]}{'...' if len(model.description) > 150 else ''}
            </p>
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px;">
                <div style="color: #8B0000;">Size: {model.size}</div>
                <div>{compat_badges}</div>
            </div>
            {f"<div style='color: #FF6B6B; font-size: 10px; margin-top: 4px;'>Tags: {', '.join(model.tags[:3])}</div>" if model.tags else ""}
        </div>
        """
        
        info_widget = widgets.HTML(value=info_html)
        
        # Card container
        card = widgets.HBox([
            checkbox,
            info_widget
        ], layout=widgets.Layout(
            align_items='flex-start',
            margin='2px 0'
        ))
        
        return card
    
    def _create_selection_summary(self) -> widgets.Widget:
        """Create selection summary panel"""
        summary_html = f"""
        <div style="
            background: linear-gradient(90deg, rgba(139,0,0,0.1), rgba(220,20,60,0.05));
            border: 2px solid #DC143C;
            border-radius: 8px;
            padding: 16px;
            margin-top: 16px;
            text-align: center;
        ">
            <h3 style="color: #8B0000; margin: 0 0 12px 0; font-family: 'Cinzel', serif;">
                📊 Selection Summary
            </h3>
            <div id="selection-summary-content" style="color: #DC143C; font-family: 'Inter', sans-serif;">
                <div style="font-size: 18px; margin-bottom: 8px;">
                    <strong>0 models selected</strong>
                </div>
                <div style="font-size: 14px; color: #666;">
                    No models selected yet
                </div>
            </div>
        </div>
        """
        
        return widgets.HTML(value=summary_html)
    
    def _update_model_grid(self):
        """Update the model grid with filtered models"""
        self.model_cards.clear()
        self.model_checkboxes.clear()
        
        for model in self.filtered_models:
            card = self._create_model_card(model)
            self.model_cards.append(card)
        
        if hasattr(self, 'model_grid') and self.model_grid:
            self.model_grid.children = self.model_cards
    
    def _apply_filters(self):
        """Apply current search and filter settings"""
        search_query = self.search_box.value if self.search_box else ""
        
        filters = {
            'category': self.category_filter.value if self.category_filter else 'all',
            'rating_min': self.rating_filter.value if self.rating_filter else 0.0,
            'compatibility': self.compatibility_filter.value if self.compatibility_filter else 'all',
            'show_nsfw': self.nsfw_toggle.value if self.nsfw_toggle else False
        }
        
        self.filtered_models = [
            model for model in self.all_models
            if model.matches_search(search_query) and model.matches_filters(filters)
        ]
        
        self._update_model_grid()
        self._update_progress()
    
    def _on_search_change(self, change):
        """Handle search box changes"""
        self._apply_filters()
    
    def _on_filter_change(self, change):
        """Handle filter changes"""
        self._apply_filters()
    
    def _on_model_toggle(self, change, model: ModelInfo):
        """Handle individual model selection toggle"""
        if change['new']:
            self.selected_models[model.name] = model
        else:
            self.selected_models.pop(model.name, None)
        
        self._update_selection_summary()
        self._update_progress()
        
        if self.callback:
            self.callback(list(self.selected_models.values()))
    
    def _batch_select_all(self):
        """Select all visible models"""
        for model in self.filtered_models:
            if model.name in self.model_checkboxes:
                self.model_checkboxes[model.name].value = True
    
    def _batch_clear_all(self):
        """Clear all selections"""
        for checkbox in self.model_checkboxes.values():
            checkbox.value = False
    
    def _batch_invert(self):
        """Invert current selection"""
        for checkbox in self.model_checkboxes.values():
            checkbox.value = not checkbox.value
    
    def _batch_select_category(self):
        """Select all models in current category filter"""
        if self.category_filter and self.category_filter.value != 'all':
            target_category = self.category_filter.value
            for model in self.filtered_models:
                if model.category == target_category and model.name in self.model_checkboxes:
                    self.model_checkboxes[model.name].value = True
    
    def _update_selection_summary(self):
        """Update the selection summary display"""
        count = len(self.selected_models)
        
        if count == 0:
            summary_text = "No models selected yet"
            details = ""
        else:
            categories = {}
            total_size = 0
            
            for model in self.selected_models.values():
                categories[model.category] = categories.get(model.category, 0) + 1
                # Simple size parsing (assuming format like "144 MB")
                try:
                    size_str = model.size.replace('GB', '000').replace('MB', '').replace(' ', '')
                    if size_str.replace('.', '').isdigit():
                        total_size += float(size_str)
                except:
                    pass
            
            category_summary = ", ".join([f"{cat}: {cnt}" for cat, cnt in categories.items()])
            size_display = f"{total_size:.1f} MB" if total_size < 1000 else f"{total_size/1000:.1f} GB"
            
            summary_text = f"{count} models selected"
            details = f"Categories: {category_summary}<br>Est. Size: {size_display}"
        
        summary_html = f"""
        <div style="font-size: 18px; margin-bottom: 8px;">
            <strong>{summary_text}</strong>
        </div>
        <div style="font-size: 14px; color: #666;">
            {details}
        </div>
        """
        
        if hasattr(self, 'selection_summary') and self.selection_summary:
            # Update the summary content
            current_html = self.selection_summary.value
            updated_html = re.sub(
                r'<div id="selection-summary-content"[^>]*>.*?</div>',
                f'<div id="selection-summary-content" style="color: #DC143C; font-family: \'Inter\', sans-serif;">{summary_html}</div>',
                current_html,
                flags=re.DOTALL
            )
            self.selection_summary.value = updated_html
    
    def _update_progress(self):
        """Update progress bar based on selection"""
        if hasattr(self, 'progress_bar') and self.progress_bar:
            total_visible = len(self.filtered_models)
            selected_visible = len([m for m in self.selected_models.values() if m in self.filtered_models])
            
            if total_visible > 0:
                progress = int((selected_visible / total_visible) * 100)
                self.progress_bar.value = progress
                self.progress_bar.description = f'Selection: {selected_visible}/{total_visible}'
            else:
                self.progress_bar.value = 0
                self.progress_bar.description = 'Selection: 0/0'
    
    def get_selected_models(self) -> List[ModelInfo]:
        """Get list of currently selected models"""
        return list(self.selected_models.values())
    
    def get_selection_summary(self) -> Dict[str, Any]:
        """Get detailed selection summary"""
        models = list(self.selected_models.values())
        
        return {
            'count': len(models),
            'categories': {cat: len([m for m in models if m.category == cat]) 
                          for cat in set(m.category for m in models)},
            'average_rating': sum(m.rating for m in models) / len(models) if models else 0.0,
            'compatibility': list(set(comp for m in models for comp in m.compatibility)),
            'models': [{'name': m.name, 'category': m.category, 'url': m.download_url} for m in models]
        }
    
    def display(self):
        """Display the enhanced model selector"""
        # Apply initial styling with CSS injection
        style_css = """
        <style>
        .widget-hbox .widget-label { color: #8B0000 !important; font-weight: bold; }
        .widget-dropdown select { border: 2px solid #DC143C !important; }
        .widget-text input { border: 2px solid #DC143C !important; }
        .widget-checkbox input[type="checkbox"]:checked { 
            background-color: #DC143C !important; 
            border-color: #8B0000 !important; 
        }
        .widget-button { 
            transition: all 0.3s ease !important;
        }
        .widget-button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(139,0,0,0.3) !important;
        }
        </style>
        """
        
        display(HTML(style_css))
        display(self.main_container)
        
        # Initialize with current filters
        self._apply_filters()


# Usage example and testing function
def create_enhanced_model_selector(model_type: str = "lora", callback: Optional[Callable] = None) -> EnhancedModelSelector:
    """Factory function to create enhanced model selector"""
    return EnhancedModelSelector(model_type=model_type, callback=callback)


def demo_model_selector():
    """Demo function to showcase the enhanced model selector"""
    def selection_callback(selected_models):
        print(f"Selection updated: {len(selected_models)} models selected")
        for model in selected_models:
            print(f"  - {model.name} ({model.category})")
    
    print("Creating Enhanced Model Selector Demo...")
    selector = create_enhanced_model_selector(callback=selection_callback)
    selector.display()
    
    return selector


if __name__ == "__main__":
    # Demo mode
    demo_model_selector()