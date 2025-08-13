#!/usr/bin/env python3
"""
Enhanced Visual Feedback System (V3)
Sophisticated visual feedback mechanisms with sanguine color scheme integration

Features:
- Advanced notification system with multiple types and animations
- Real-time status indicators with smooth transitions
- Interactive loading animations and progress feedback
- Toast notifications with auto-dismiss
- Visual connection status indicators
- Sophisticated hover effects and micro-interactions
- Screen reader accessibility support
- Cloud GPU environment optimizations
"""

import ipywidgets as widgets
from IPython.display import display, HTML, Javascript
import time
import json
from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import threading
import asyncio


class NotificationType(Enum):
    """Notification types with distinct styling"""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    LOADING = "loading"
    PROGRESS = "progress"


class AnimationType(Enum):
    """Animation types for visual feedback"""
    FADE_IN = "fadeIn"
    SLIDE_IN = "slideIn"
    BOUNCE = "bounce"
    PULSE = "pulse"
    SHAKE = "shake"
    GLOW = "glow"


@dataclass
class NotificationConfig:
    """Configuration for notifications"""
    message: str
    notification_type: NotificationType
    duration: float = 4000  # milliseconds
    animation: AnimationType = AnimationType.SLIDE_IN
    dismissible: bool = True
    persistent: bool = False
    callback: Optional[Callable] = None
    extra_data: Dict[str, Any] = field(default_factory=dict)


class EnhancedVisualFeedback:
    """Sophisticated visual feedback system for widgets"""
    
    def __init__(self):
        self.notification_container = None
        self.status_indicators = {}
        self.active_notifications = {}
        self.animation_queue = []
        self.feedback_history = []
        
        # Color scheme (sanguine theme)
        self.colors = {
            'primary': '#8B0000',      # Dark red
            'accent': '#DC143C',       # Crimson
            'glow': '#FF6B6B',         # Light red glow
            'success': '#46FF46',      # Bright green
            'warning': '#FFA500',      # Orange
            'error': '#FF4444',        # Bright red
            'info': '#4A90E2',         # Blue
            'loading': '#DC143C',      # Crimson for loading
            'progress': '#8B0000',     # Dark red for progress
            'background': 'rgba(139, 0, 0, 0.05)',
            'text': '#2C2C2C',
            'text_light': '#666666'
        }
        
        # Initialize the feedback system
        self._initialize_system()
    
    def _initialize_system(self):
        """Initialize the visual feedback system"""
        # Create notification container
        self.notification_container = widgets.HTML(
            value='<div id="notification-container"></div>',
            layout=widgets.Layout(
                position='fixed',
                top='20px',
                right='20px',
                z_index='9999',
                pointer_events='none'
            )
        )
        
        # Inject CSS styles
        self._inject_styles()
        
        # Initialize JavaScript functions
        self._inject_javascript()
    
    def _inject_styles(self):
        """Inject CSS styles for visual feedback"""
        css_styles = f"""
        <style>
        /* Enhanced Visual Feedback Styles */
        .notification-container {{
            position: fixed !important;
            top: 20px !important;
            right: 20px !important;
            z-index: 9999 !important;
            pointer-events: none !important;
            max-width: 400px;
            width: auto;
        }}
        
        .notification {{
            background: linear-gradient(135deg, {self.colors['background']}, rgba(220, 20, 60, 0.08));
            border-left: 4px solid {self.colors['accent']};
            border-radius: 8px;
            padding: 16px 20px;
            margin-bottom: 12px;
            box-shadow: 0 4px 20px rgba(139, 0, 0, 0.15), 0 2px 8px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 14px;
            line-height: 1.5;
            position: relative;
            overflow: hidden;
            pointer-events: auto;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .notification::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, {self.colors['accent']}, {self.colors['glow']});
            transform: translateX(-100%);
            animation: progressBar 0.8s ease-out forwards;
        }}
        
        .notification.success {{
            border-left-color: {self.colors['success']};
        }}
        
        .notification.error {{
            border-left-color: {self.colors['error']};
        }}
        
        .notification.warning {{
            border-left-color: {self.colors['warning']};
        }}
        
        .notification.info {{
            border-left-color: {self.colors['info']};
        }}
        
        .notification.loading {{
            border-left-color: {self.colors['loading']};
        }}
        
        .notification-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 8px;
            font-weight: 600;
            color: {self.colors['primary']};
        }}
        
        .notification-icon {{
            font-size: 18px;
            margin-right: 10px;
        }}
        
        .notification-close {{
            background: none;
            border: none;
            color: {self.colors['text_light']};
            cursor: pointer;
            font-size: 18px;
            padding: 0;
            opacity: 0.7;
            transition: opacity 0.2s ease;
        }}
        
        .notification-close:hover {{
            opacity: 1;
        }}
        
        .notification-message {{
            color: {self.colors['text']};
            margin: 0;
        }}
        
        .notification-actions {{
            margin-top: 12px;
            display: flex;
            gap: 8px;
        }}
        
        .notification-action {{
            background: {self.colors['accent']};
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        .notification-action:hover {{
            background: {self.colors['primary']};
            transform: translateY(-1px);
        }}
        
        /* Status Indicators */
        .status-indicator {{
            display: inline-flex;
            align-items: center;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
            transition: all 0.3s ease;
        }}
        
        .status-indicator.connected {{
            background: linear-gradient(135deg, {self.colors['success']}, #00DD00);
            color: white;
        }}
        
        .status-indicator.connecting {{
            background: linear-gradient(135deg, {self.colors['warning']}, #FFB700);
            color: white;
            animation: pulse 2s infinite;
        }}
        
        .status-indicator.disconnected {{
            background: linear-gradient(135deg, {self.colors['error']}, #FF6B6B);
            color: white;
        }}
        
        .status-indicator.loading {{
            background: linear-gradient(135deg, {self.colors['loading']}, {self.colors['glow']});
            color: white;
            animation: pulse 1.5s infinite;
        }}
        
        /* Progress Elements */
        .enhanced-progress {{
            width: 100%;
            height: 8px;
            background: rgba(139, 0, 0, 0.1);
            border-radius: 4px;
            overflow: hidden;
            position: relative;
        }}
        
        .enhanced-progress-bar {{
            height: 100%;
            background: linear-gradient(90deg, {self.colors['primary']}, {self.colors['accent']}, {self.colors['glow']});
            border-radius: 4px;
            transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }}
        
        .enhanced-progress-bar::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            bottom: 0;
            right: 0;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            animation: shimmer 2s infinite;
        }}
        
        /* Loading Spinner */
        .loading-spinner {{
            width: 20px;
            height: 20px;
            border: 2px solid rgba(139, 0, 0, 0.2);
            border-top: 2px solid {self.colors['accent']};
            border-radius: 50%;
            animation: spin 1s linear infinite;
            display: inline-block;
            margin-right: 8px;
        }}
        
        /* Glow Effect */
        .glow-effect {{
            animation: glow 2s ease-in-out infinite alternate;
        }}
        
        /* Animations */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(-20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @keyframes slideIn {{
            from {{ opacity: 0; transform: translateX(300px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        
        @keyframes bounce {{
            0%, 20%, 53%, 80%, 100% {{ transform: translateY(0); }}
            40%, 43% {{ transform: translateY(-20px); }}
            70% {{ transform: translateY(-10px); }}
        }}
        
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}
        
        @keyframes shake {{
            0%, 100% {{ transform: translateX(0); }}
            25% {{ transform: translateX(-5px); }}
            75% {{ transform: translateX(5px); }}
        }}
        
        @keyframes glow {{
            from {{ box-shadow: 0 0 20px rgba(139, 0, 0, 0.5); }}
            to {{ box-shadow: 0 0 30px rgba(220, 20, 60, 0.8), 0 0 40px rgba(255, 107, 107, 0.3); }}
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        @keyframes progressBar {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(0); }}
        }}
        
        @keyframes shimmer {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(100%); }}
        }}
        
        /* Hover Effects */
        .interactive-element {{
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .interactive-element:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(139, 0, 0, 0.2);
        }}
        
        .button-hover-effect {{
            position: relative;
            overflow: hidden;
        }}
        
        .button-hover-effect::before {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }}
        
        .button-hover-effect:hover::before {{
            width: 300px;
            height: 300px;
        }}
        
        /* Responsive Design */
        @media (max-width: 480px) {{
            .notification-container {{
                left: 10px;
                right: 10px;
                top: 10px;
                max-width: none;
            }}
            
            .notification {{
                padding: 12px 16px;
                font-size: 13px;
            }}
        }}
        </style>
        """
        
        display(HTML(css_styles))
    
    def _inject_javascript(self):
        """Inject JavaScript functions for dynamic feedback"""
        js_code = """
        <script>
        // Enhanced Visual Feedback JavaScript Functions
        window.EnhancedFeedback = {
            notificationId: 0,
            
            // Create notification element
            createNotification: function(config) {
                const id = 'notification-' + (++this.notificationId);
                const notification = document.createElement('div');
                notification.id = id;
                notification.className = `notification ${config.type} ${config.animation}`;
                notification.style.animation = `${config.animation} 0.4s cubic-bezier(0.4, 0, 0.2, 1)`;
                
                const icon = this.getIcon(config.type);
                const closeButton = config.dismissible ? 
                    `<button class="notification-close" onclick="EnhancedFeedback.dismissNotification('${id}')">&times;</button>` : '';
                
                notification.innerHTML = `
                    <div class="notification-header">
                        <span class="notification-icon">${icon}</span>
                        ${closeButton}
                    </div>
                    <div class="notification-message">${config.message}</div>
                    ${config.actions ? this.createActions(config.actions, id) : ''}
                `;
                
                return notification;
            },
            
            // Show notification
            showNotification: function(config) {
                let container = document.getElementById('notification-container');
                if (!container) {
                    container = document.createElement('div');
                    container.id = 'notification-container';
                    container.className = 'notification-container';
                    document.body.appendChild(container);
                }
                
                const notification = this.createNotification(config);
                container.appendChild(notification);
                
                // Auto-dismiss
                if (!config.persistent && config.duration > 0) {
                    setTimeout(() => {
                        this.dismissNotification(notification.id);
                    }, config.duration);
                }
                
                return notification.id;
            },
            
            // Dismiss notification
            dismissNotification: function(id) {
                const notification = document.getElementById(id);
                if (notification) {
                    notification.style.animation = 'fadeOut 0.3s ease-in-out';
                    notification.style.transform = 'translateX(300px)';
                    notification.style.opacity = '0';
                    
                    setTimeout(() => {
                        if (notification.parentNode) {
                            notification.parentNode.removeChild(notification);
                        }
                    }, 300);
                }
            },
            
            // Get icon for notification type
            getIcon: function(type) {
                const icons = {
                    'success': '✅',
                    'error': '❌',
                    'warning': '⚠️',
                    'info': 'ℹ️',
                    'loading': '<div class="loading-spinner"></div>',
                    'progress': '📊'
                };
                return icons[type] || 'ℹ️';
            },
            
            // Create action buttons
            createActions: function(actions, notificationId) {
                const actionButtons = actions.map(action => 
                    `<button class="notification-action" onclick="${action.callback}; EnhancedFeedback.dismissNotification('${notificationId}');">
                        ${action.label}
                    </button>`
                ).join('');
                
                return `<div class="notification-actions">${actionButtons}</div>`;
            },
            
            // Update progress indicator
            updateProgress: function(elementId, progress, message) {
                const element = document.getElementById(elementId);
                if (element) {
                    const progressBar = element.querySelector('.enhanced-progress-bar');
                    const messageEl = element.querySelector('.progress-message');
                    
                    if (progressBar) {
                        progressBar.style.width = progress + '%';
                    }
                    
                    if (messageEl && message) {
                        messageEl.textContent = message;
                    }
                }
            },
            
            // Create status indicator
            createStatusIndicator: function(status, message) {
                return `<span class="status-indicator ${status}">${message}</span>`;
            },
            
            // Add glow effect
            addGlowEffect: function(elementId) {
                const element = document.getElementById(elementId);
                if (element) {
                    element.classList.add('glow-effect');
                }
            },
            
            // Remove glow effect
            removeGlowEffect: function(elementId) {
                const element = document.getElementById(elementId);
                if (element) {
                    element.classList.remove('glow-effect');
                }
            },
            
            // Animate element
            animateElement: function(elementId, animation) {
                const element = document.getElementById(elementId);
                if (element) {
                    element.style.animation = `${animation} 0.6s ease-in-out`;
                    
                    setTimeout(() => {
                        element.style.animation = '';
                    }, 600);
                }
            }
        };
        </script>
        """
        
        display(HTML(js_code))
    
    def show_notification(self, 
                         message: str, 
                         notification_type: NotificationType = NotificationType.INFO,
                         duration: float = 4000,
                         animation: AnimationType = AnimationType.SLIDE_IN,
                         dismissible: bool = True,
                         persistent: bool = False,
                         actions: Optional[List[Dict[str, str]]] = None) -> str:
        """Show a notification with enhanced visual feedback"""
        
        config = {
            'message': message,
            'type': notification_type.value,
            'duration': duration,
            'animation': animation.value,
            'dismissible': dismissible,
            'persistent': persistent,
            'actions': actions or []
        }
        
        js_call = f"""
        <script>
        EnhancedFeedback.showNotification({json.dumps(config)});
        </script>
        """
        
        display(HTML(js_call))
        
        # Store in history
        self.feedback_history.append({
            'timestamp': time.time(),
            'type': notification_type.value,
            'message': message,
            'config': config
        })
        
        return f"notification-{int(time.time() * 1000)}"
    
    def show_success(self, message: str, duration: float = 3000) -> str:
        """Show success notification"""
        return self.show_notification(message, NotificationType.SUCCESS, duration, AnimationType.BOUNCE)
    
    def show_error(self, message: str, duration: float = 5000) -> str:
        """Show error notification"""
        return self.show_notification(message, NotificationType.ERROR, duration, AnimationType.SHAKE)
    
    def show_warning(self, message: str, duration: float = 4000) -> str:
        """Show warning notification"""
        return self.show_notification(message, NotificationType.WARNING, duration)
    
    def show_info(self, message: str, duration: float = 3000) -> str:
        """Show info notification"""
        return self.show_notification(message, NotificationType.INFO, duration)
    
    def show_loading(self, message: str, persistent: bool = True) -> str:
        """Show loading notification"""
        return self.show_notification(message, NotificationType.LOADING, 0, 
                                    AnimationType.FADE_IN, dismissible=False, persistent=persistent)
    
    def dismiss_notification(self, notification_id: str):
        """Dismiss a specific notification"""
        js_call = f"""
        <script>
        EnhancedFeedback.dismissNotification('{notification_id}');
        </script>
        """
        display(HTML(js_call))
    
    def create_status_indicator(self, 
                              status: str, 
                              message: str, 
                              element_id: Optional[str] = None) -> widgets.HTML:
        """Create a status indicator widget"""
        indicator_id = element_id or f"status-{int(time.time() * 1000)}"
        
        status_html = f"""
        <div id="{indicator_id}" class="status-indicator {status}">
            {message}
        </div>
        """
        
        indicator = widgets.HTML(value=status_html)
        self.status_indicators[indicator_id] = indicator
        
        return indicator
    
    def update_status_indicator(self, indicator_id: str, status: str, message: str):
        """Update an existing status indicator"""
        if indicator_id in self.status_indicators:
            indicator = self.status_indicators[indicator_id]
            indicator.value = f'<div id="{indicator_id}" class="status-indicator {status}">{message}</div>'
        else:
            # Update via JavaScript if not in our registry
            js_call = f"""
            <script>
            const element = document.getElementById('{indicator_id}');
            if (element) {{
                element.className = 'status-indicator {status}';
                element.textContent = '{message}';
            }}
            </script>
            """
            display(HTML(js_call))
    
    def create_enhanced_progress(self, 
                               initial_progress: float = 0, 
                               message: str = "Processing...",
                               element_id: Optional[str] = None) -> widgets.HTML:
        """Create an enhanced progress indicator"""
        progress_id = element_id or f"progress-{int(time.time() * 1000)}"
        
        progress_html = f"""
        <div id="{progress_id}" class="enhanced-progress-container">
            <div class="progress-message" style="margin-bottom: 8px; color: {self.colors['primary']}; font-weight: 600;">
                {message}
            </div>
            <div class="enhanced-progress">
                <div class="enhanced-progress-bar" style="width: {initial_progress}%;"></div>
            </div>
            <div class="progress-percentage" style="margin-top: 4px; color: {self.colors['text_light']}; font-size: 12px;">
                {initial_progress:.1f}%
            </div>
        </div>
        """
        
        return widgets.HTML(value=progress_html)
    
    def update_progress(self, element_id: str, progress: float, message: Optional[str] = None):
        """Update progress indicator"""
        js_call = f"""
        <script>
        EnhancedFeedback.updateProgress('{element_id}', {progress}, {json.dumps(message) if message else 'null'});
        
        // Update percentage display
        const container = document.getElementById('{element_id}');
        if (container) {{
            const percentageEl = container.querySelector('.progress-percentage');
            if (percentageEl) {{
                percentageEl.textContent = '{progress:.1f}%';
            }}
        }}
        </script>
        """
        display(HTML(js_call))
    
    def add_glow_effect(self, element_id: str):
        """Add glow effect to an element"""
        js_call = f"""
        <script>
        EnhancedFeedback.addGlowEffect('{element_id}');
        </script>
        """
        display(HTML(js_call))
    
    def remove_glow_effect(self, element_id: str):
        """Remove glow effect from an element"""
        js_call = f"""
        <script>
        EnhancedFeedback.removeGlowEffect('{element_id}');
        </script>
        """
        display(HTML(js_call))
    
    def animate_element(self, element_id: str, animation: AnimationType):
        """Animate an element with specified animation"""
        js_call = f"""
        <script>
        EnhancedFeedback.animateElement('{element_id}', '{animation.value}');
        </script>
        """
        display(HTML(js_call))
    
    def create_interactive_button(self, 
                                description: str, 
                                callback: Callable,
                                button_style: str = "",
                                tooltip: str = "",
                                icon: str = "") -> widgets.Button:
        """Create a button with enhanced hover effects"""
        
        button = widgets.Button(
            description=f"{icon} {description}".strip(),
            button_style=button_style,
            tooltip=tooltip,
            layout=widgets.Layout(margin='4px'),
            style={'font_weight': '600'}
        )
        
        # Add custom CSS class for hover effects
        button.add_class('button-hover-effect')
        button.add_class('interactive-element')
        
        button.on_click(callback)
        
        return button
    
    def show_connection_status(self, status: str, details: str = "") -> str:
        """Show connection status with appropriate styling"""
        status_messages = {
            'connected': f"🔗 Connected {details}",
            'connecting': f"⏳ Connecting... {details}",
            'disconnected': f"❌ Disconnected {details}",
            'error': f"⚠️ Connection Error {details}"
        }
        
        message = status_messages.get(status, f"ℹ️ {status} {details}")
        
        if status == 'connected':
            return self.show_success(message)
        elif status == 'connecting':
            return self.show_loading(message)
        elif status in ['disconnected', 'error']:
            return self.show_error(message)
        else:
            return self.show_info(message)
    
    def display_feedback_stats(self) -> widgets.HTML:
        """Display feedback system statistics"""
        total_feedback = len(self.feedback_history)
        
        if total_feedback == 0:
            stats_html = "<p>No feedback history available.</p>"
        else:
            type_counts = {}
            for item in self.feedback_history:
                item_type = item['type']
                type_counts[item_type] = type_counts.get(item_type, 0) + 1
            
            stats_list = []
            for feedback_type, count in type_counts.items():
                stats_list.append(f"{feedback_type.title()}: {count}")
            
            stats_html = f"""
            <div style="background: {self.colors['background']}; border: 1px solid {self.colors['accent']}; 
                        border-radius: 8px; padding: 16px; margin: 8px 0;">
                <h4 style="color: {self.colors['primary']}; margin: 0 0 12px 0;">Feedback Statistics</h4>
                <p style="color: {self.colors['text']}; margin: 0;">
                    Total Notifications: {total_feedback}<br>
                    {' | '.join(stats_list)}
                </p>
            </div>
            """
        
        return widgets.HTML(value=stats_html)
    
    def display(self):
        """Display the notification container"""
        display(self.notification_container)


# Usage functions and demo
def create_visual_feedback_system() -> EnhancedVisualFeedback:
    """Factory function to create enhanced visual feedback system"""
    return EnhancedVisualFeedback()


def demo_visual_feedback():
    """Demo function to showcase the visual feedback system"""
    print("Creating Enhanced Visual Feedback Demo...")
    
    feedback = create_visual_feedback_system()
    feedback.display()
    
    # Demo container with various feedback examples
    demo_container = widgets.VBox([
        widgets.HTML("<h3 style='color: #8B0000;'>Visual Feedback System Demo</h3>"),
        
        # Notification buttons
        widgets.HBox([
            feedback.create_interactive_button("Show Success", 
                lambda b: feedback.show_success("Operation completed successfully!")),
            feedback.create_interactive_button("Show Error", 
                lambda b: feedback.show_error("An error occurred while processing.")),
            feedback.create_interactive_button("Show Warning", 
                lambda b: feedback.show_warning("Please check your configuration.")),
            feedback.create_interactive_button("Show Info", 
                lambda b: feedback.show_info("New model available for download."))
        ]),
        
        # Status indicators
        widgets.HTML("<h4 style='color: #DC143C; margin: 16px 0 8px 0;'>Status Indicators</h4>"),
        widgets.HBox([
            feedback.create_status_indicator("connected", "API Connected"),
            feedback.create_status_indicator("loading", "Loading Models..."),
            feedback.create_status_indicator("disconnected", "Offline")
        ]),
        
        # Progress indicator
        widgets.HTML("<h4 style='color: #DC143C; margin: 16px 0 8px 0;'>Progress Indicator</h4>"),
        feedback.create_enhanced_progress(45, "Downloading model..."),
        
        # Statistics
        widgets.HTML("<h4 style='color: #DC143C; margin: 16px 0 8px 0;'>Feedback Statistics</h4>"),
        feedback.display_feedback_stats()
    ])
    
    display(demo_container)
    return feedback


if __name__ == "__main__":
    # Demo mode
    demo_visual_feedback()