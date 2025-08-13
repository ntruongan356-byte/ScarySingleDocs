#!/usr/bin/env python3
"""
Cloud GPU Environment Compatibility System (V3)
Comprehensive compatibility layer for various cloud notebook environments

Supported Platforms:
- Google Colab (Free & Pro)
- Kaggle Notebooks
- Lightning.ai Studios
- Paperspace Gradient
- Vast.ai Instances
- AWS SageMaker
- Azure ML Studio
- Generic cloud instances

Features:
- Environment detection and adaptation
- Platform-specific optimizations
- Responsive layout adjustments
- Network limitation handling
- Resource constraint awareness
- Performance optimizations
- Fallback mechanisms
"""

import os
import platform
import sys
import json
import time
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from pathlib import Path
import ipywidgets as widgets
from IPython.display import display, HTML, Javascript
import subprocess
import socket
import psutil
import requests


@dataclass
class CloudEnvironment:
    """Cloud environment configuration"""
    platform: str
    provider: str
    region: Optional[str] = None
    instance_type: Optional[str] = None
    
    # Resource constraints
    max_memory_gb: float = 16.0
    max_storage_gb: float = 100.0
    cpu_cores: int = 4
    gpu_available: bool = False
    gpu_memory_gb: float = 0.0
    
    # Network limitations
    outbound_internet: bool = True
    custom_domains: bool = True
    port_restrictions: List[int] = field(default_factory=list)
    tunnel_support: List[str] = field(default_factory=list)
    
    # UI constraints
    max_viewport_width: int = 1200
    max_viewport_height: int = 800
    mobile_optimized: bool = False
    
    # Feature support
    javascript_enabled: bool = True
    websocket_support: bool = True
    file_upload_limit_mb: int = 200
    
    # Performance settings
    widget_update_throttle_ms: int = 100
    animation_reduced: bool = False
    lazy_loading: bool = True


class CloudCompatibilityManager:
    """Manages compatibility across different cloud environments"""
    
    def __init__(self):
        self.environment = self._detect_environment()
        self.adaptations = []
        self.performance_metrics = {
            'load_time': 0.0,
            'memory_usage': 0.0,
            'widget_count': 0,
            'api_response_time': 0.0
        }
        
        # Apply environment-specific optimizations
        self._apply_optimizations()
    
    def _detect_environment(self) -> CloudEnvironment:
        """Detect current cloud environment and its capabilities"""
        env = CloudEnvironment(platform="unknown", provider="unknown")
        
        # Google Colab detection
        if self._is_google_colab():
            env.platform = "google_colab"
            env.provider = "Google"
            env.max_memory_gb = 12.7  # Colab free tier
            env.gpu_available = 'COLAB_GPU' in os.environ
            env.gpu_memory_gb = 15.0 if env.gpu_available else 0.0
            env.custom_domains = False
            env.port_restrictions = [i for i in range(1, 1024) if i not in [8080, 8888]]
            env.tunnel_support = ["ngrok", "cloudflared", "localtunnel"]
            env.max_viewport_width = 1000
            env.widget_update_throttle_ms = 200  # Slower updates for Colab
            
        # Kaggle Notebooks
        elif self._is_kaggle():
            env.platform = "kaggle"
            env.provider = "Kaggle"
            env.max_memory_gb = 13.0
            env.gpu_available = True
            env.gpu_memory_gb = 16.0
            env.outbound_internet = False  # Limited internet access
            env.custom_domains = False
            env.tunnel_support = ["ngrok"]  # Limited tunnel options
            env.file_upload_limit_mb = 500
            
        # Lightning.ai
        elif self._is_lightning_ai():
            env.platform = "lightning_ai" 
            env.provider = "Lightning AI"
            env.max_memory_gb = 32.0
            env.gpu_available = True
            env.gpu_memory_gb = 24.0
            env.tunnel_support = ["ngrok", "gradio", "cloudflared"]
            env.max_viewport_width = 1400
            
        # Paperspace Gradient
        elif self._is_paperspace():
            env.platform = "paperspace"
            env.provider = "Paperspace"
            env.max_memory_gb = 8.0
            env.gpu_available = True
            env.gpu_memory_gb = 8.0
            env.tunnel_support = ["ngrok", "cloudflared", "localtunnel", "gradio"]
            
        # Vast.ai
        elif self._is_vast_ai():
            env.platform = "vast_ai"
            env.provider = "Vast.ai"
            env.max_memory_gb = 32.0  # Variable based on instance
            env.gpu_available = True
            env.gpu_memory_gb = 24.0  # Variable
            env.tunnel_support = ["ngrok", "cloudflared", "localtunnel"]
            
        # AWS SageMaker
        elif self._is_aws_sagemaker():
            env.platform = "sagemaker"
            env.provider = "AWS"
            env.max_memory_gb = 16.0
            env.gpu_available = True
            env.tunnel_support = ["ngrok", "cloudflared"]
            
        # Azure ML Studio
        elif self._is_azure_ml():
            env.platform = "azure_ml"
            env.provider = "Microsoft Azure"
            env.max_memory_gb = 14.0
            env.gpu_available = True
            env.tunnel_support = ["ngrok", "cloudflared"]
            
        # Generic cloud detection
        else:
            env = self._detect_generic_cloud()
        
        # Get actual system resources
        env = self._update_system_resources(env)
        
        return env
    
    def _is_google_colab(self) -> bool:
        """Check if running in Google Colab"""
        return any([
            'COLAB_GPU' in os.environ,
            'COLAB_TPU_ADDR' in os.environ,
            '/usr/local/lib/python' in sys.path[0] and 'colab' in sys.path[0].lower(),
            os.path.exists('/content')
        ])
    
    def _is_kaggle(self) -> bool:
        """Check if running in Kaggle"""
        return any([
            'KAGGLE_URL_BASE' in os.environ,
            'KAGGLE_USER_SECRETS_TOKEN' in os.environ,
            os.path.exists('/kaggle')
        ])
    
    def _is_lightning_ai(self) -> bool:
        """Check if running in Lightning.ai"""
        return any([
            'LIGHTNING_CLOUD_URL' in os.environ,
            'LIGHTNING_APP_NAME' in os.environ,
            os.path.exists('/teamspace')
        ])
    
    def _is_paperspace(self) -> bool:
        """Check if running in Paperspace"""
        return any([
            'PAPERSPACE_NOTEBOOK_REPO_ID' in os.environ,
            'PS_API_KEY' in os.environ,
            os.path.exists('/notebooks')
        ])
    
    def _is_vast_ai(self) -> bool:
        """Check if running in Vast.ai"""
        return any([
            'VAST_CONTAINERLABEL' in os.environ,
            'SSH_CONNECTION' in os.environ and 'vast' in platform.node().lower(),
            os.path.exists('/root') and 'vast' in platform.node().lower()
        ])
    
    def _is_aws_sagemaker(self) -> bool:
        """Check if running in AWS SageMaker"""
        return any([
            'SM_TRAINING_ENV' in os.environ,
            'SAGEMAKER_PROGRAM' in os.environ,
            os.path.exists('/opt/ml')
        ])
    
    def _is_azure_ml(self) -> bool:
        """Check if running in Azure ML"""
        return any([
            'AZUREML_RUN_ID' in os.environ,
            'AML_PARAMETER_job_name' in os.environ,
            os.path.exists('/mnt/azureml')
        ])
    
    def _detect_generic_cloud(self) -> CloudEnvironment:
        """Detect generic cloud environment"""
        env = CloudEnvironment(platform="generic_cloud", provider="Unknown")
        
        # Check common cloud indicators
        hostname = platform.node().lower()
        if any(cloud in hostname for cloud in ['aws', 'ec2', 'amazon']):
            env.provider = "AWS"
        elif any(cloud in hostname for cloud in ['gcp', 'google', 'compute']):
            env.provider = "Google Cloud"
        elif any(cloud in hostname for cloud in ['azure', 'microsoft']):
            env.provider = "Microsoft Azure"
        elif any(cloud in hostname for cloud in ['digital', 'ocean']):
            env.provider = "DigitalOcean"
        elif os.path.exists('/proc/version'):
            # Check for cloud-specific kernel info
            with open('/proc/version', 'r') as f:
                version_info = f.read().lower()
                if 'aws' in version_info:
                    env.provider = "AWS"
                elif 'gcp' in version_info or 'google' in version_info:
                    env.provider = "Google Cloud"
                elif 'azure' in version_info:
                    env.provider = "Microsoft Azure"
        
        # Default tunnel support for generic cloud
        env.tunnel_support = ["ngrok", "cloudflared", "localtunnel", "gradio"]
        
        return env
    
    def _update_system_resources(self, env: CloudEnvironment) -> CloudEnvironment:
        """Update environment with actual system resources"""
        try:
            # Memory
            memory_info = psutil.virtual_memory()
            env.max_memory_gb = memory_info.total / (1024**3)
            
            # CPU
            env.cpu_cores = psutil.cpu_count()
            
            # GPU detection
            try:
                import subprocess
                result = subprocess.run(['nvidia-smi', '--query-gpu=memory.total', '--format=csv,noheader,nounits'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    gpu_memory = int(result.stdout.strip())
                    env.gpu_available = True
                    env.gpu_memory_gb = gpu_memory / 1024
            except:
                pass
            
            # Disk space
            disk_info = psutil.disk_usage('/')
            env.max_storage_gb = disk_info.total / (1024**3)
            
        except Exception as e:
            print(f"Warning: Could not detect system resources: {e}")
        
        return env
    
    def _apply_optimizations(self):
        """Apply environment-specific optimizations"""
        optimizations = []
        
        # Memory-constrained environments
        if self.environment.max_memory_gb < 8:
            optimizations.append("low_memory_mode")
            self.environment.lazy_loading = True
            self.environment.widget_update_throttle_ms = 300
        
        # Limited bandwidth environments
        if not self.environment.outbound_internet or self.environment.platform == "kaggle":
            optimizations.append("offline_mode")
            self.environment.animation_reduced = True
        
        # Mobile/small screen optimization
        if self.environment.max_viewport_width < 1000:
            optimizations.append("mobile_layout")
            self.environment.mobile_optimized = True
        
        # GPU-accelerated environments
        if self.environment.gpu_available:
            optimizations.append("gpu_acceleration")
        
        # Network-restricted environments
        if not self.environment.custom_domains:
            optimizations.append("tunnel_required")
        
        self.adaptations = optimizations
    
    def get_widget_layout_config(self) -> Dict[str, Any]:
        """Get optimized widget layout configuration"""
        config = {
            'max_width': f"{min(self.environment.max_viewport_width, 1200)}px",
            'container_padding': '16px' if not self.environment.mobile_optimized else '8px',
            'font_size': '14px' if not self.environment.mobile_optimized else '12px',
            'grid_columns': 3 if not self.environment.mobile_optimized else 1,
            'animation_duration': '0.3s' if not self.environment.animation_reduced else '0.1s',
            'update_throttle': self.environment.widget_update_throttle_ms,
            'lazy_loading': self.environment.lazy_loading
        }
        
        return config
    
    def get_performance_css(self) -> str:
        """Get performance-optimized CSS"""
        layout_config = self.get_widget_layout_config()
        
        css = f"""
        <style>
        /* Cloud Environment Optimized CSS */
        .cloud-optimized-container {{
            max-width: {layout_config['max_width']};
            margin: 0 auto;
            padding: {layout_config['container_padding']};
            font-size: {layout_config['font_size']};
            transition-duration: {layout_config['animation_duration']};
        }}
        
        .responsive-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 16px;
            grid-auto-rows: min-content;
        }}
        
        /* Mobile optimization */
        @media (max-width: 768px) {{
            .cloud-optimized-container {{
                padding: 8px;
                font-size: 12px;
            }}
            
            .responsive-grid {{
                grid-template-columns: 1fr;
                gap: 8px;
            }}
            
            .widget-button {{
                width: 100%;
                margin: 4px 0;
            }}
            
            .tabbed-interface .tab-content {{
                padding: 8px;
            }}
        }}
        
        /* Low memory mode */
        .low-memory-mode * {{
            will-change: auto;
            transform: none;
            animation: none !important;
        }}
        
        /* Reduced animation mode */
        .reduced-animations * {{
            animation-duration: 0.1s !important;
            transition-duration: 0.1s !important;
        }}
        
        /* High contrast mode for cloud environments */
        .cloud-high-contrast {{
            filter: contrast(1.2) brightness(1.1);
        }}
        
        /* Network-optimized images */
        .network-optimized img {{
            loading: lazy;
            decoding: async;
        }}
        
        /* GPU acceleration where available */
        .gpu-accelerated {{
            will-change: transform;
            backface-visibility: hidden;
            perspective: 1000px;
        }}
        
        /* Platform-specific adjustments */
        .platform-{self.environment.platform} {{
            /* Platform-specific styles will be added here */
        }}
        
        /* Colab-specific */
        .platform-google_colab .widget-container {{
            max-width: 950px;
        }}
        
        /* Kaggle-specific */
        .platform-kaggle .notification {{
            font-size: 13px;
        }}
        
        /* Lightning.ai-specific */
        .platform-lightning_ai .enhanced-grid {{
            gap: 20px;
        }}
        </style>
        """
        
        return css
    
    def get_javascript_polyfills(self) -> str:
        """Get JavaScript polyfills for compatibility"""
        js_code = f"""
        <script>
        // Cloud Environment Compatibility JavaScript
        window.CloudEnvironment = {{
            platform: '{self.environment.platform}',
            provider: '{self.environment.provider}',
            adaptations: {json.dumps(self.adaptations)},
            config: {json.dumps(self.get_widget_layout_config())},
            
            // Throttled update function
            throttledUpdate: (function() {{
                let timeout;
                return function(func, delay = {self.environment.widget_update_throttle_ms}) {{
                    clearTimeout(timeout);
                    timeout = setTimeout(func, delay);
                }};
            }})(),
            
            // Check if feature is supported
            isFeatureSupported: function(feature) {{
                const features = {{
                    'websockets': {str(self.environment.websocket_support).lower()},
                    'javascript': {str(self.environment.javascript_enabled).lower()},
                    'custom_domains': {str(self.environment.custom_domains).lower()},
                    'outbound_internet': {str(self.environment.outbound_internet).lower()}
                }};
                return features[feature] || false;
            }},
            
            // Get recommended tunnel services
            getRecommendedTunnels: function() {{
                return {json.dumps(self.environment.tunnel_support)};
            }},
            
            // Performance monitoring
            startPerformanceMonitoring: function() {{
                if (typeof performance !== 'undefined') {{
                    window.cloudPerfStart = performance.now();
                }}
            }},
            
            endPerformanceMonitoring: function() {{
                if (typeof performance !== 'undefined' && window.cloudPerfStart) {{
                    const duration = performance.now() - window.cloudPerfStart;
                    console.log(`Cloud widget load time: ${{duration.toFixed(2)}}ms`);
                    return duration;
                }}
                return 0;
            }},
            
            // Responsive layout handler
            handleResize: function() {{
                const container = document.querySelector('.cloud-optimized-container');
                if (container) {{
                    const width = window.innerWidth;
                    if (width < 768) {{
                        container.classList.add('mobile-layout');
                    }} else {{
                        container.classList.remove('mobile-layout');
                    }}
                }}
            }},
            
            // Initialize cloud optimizations
            initialize: function() {{
                // Add platform class to body
                document.body.classList.add('platform-{self.environment.platform}');
                
                // Add adaptation classes
                {json.dumps(self.adaptations)}.forEach(function(adaptation) {{
                    document.body.classList.add(adaptation.replace('_', '-'));
                }});
                
                // Setup resize handler
                window.addEventListener('resize', this.handleResize);
                this.handleResize();
                
                // Start performance monitoring
                this.startPerformanceMonitoring();
                
                console.log('Cloud compatibility initialized for:', this.platform);
            }}
        }};
        
        // Auto-initialize when DOM is ready
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', function() {{
                CloudEnvironment.initialize();
            }});
        }} else {{
            CloudEnvironment.initialize();
        }}
        </script>
        """
        
        return js_code
    
    def create_compatibility_report(self) -> widgets.HTML:
        """Create a compatibility report widget"""
        
        # Environment info
        env_info = f"""
        <div style="background: linear-gradient(135deg, rgba(139,0,0,0.1), rgba(220,20,60,0.05)); 
                    border: 2px solid #DC143C; border-radius: 12px; padding: 20px; margin: 16px 0;">
            <h3 style="color: #8B0000; margin: 0 0 16px 0; font-family: 'Cinzel', serif;">
                🌐 Cloud Environment Report
            </h3>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 16px; margin-bottom: 16px;">
                <div>
                    <h4 style="color: #DC143C; margin: 0 0 8px 0;">Environment</h4>
                    <p style="margin: 4px 0; color: #333;">Platform: <strong>{self.environment.platform}</strong></p>
                    <p style="margin: 4px 0; color: #333;">Provider: <strong>{self.environment.provider}</strong></p>
                    <p style="margin: 4px 0; color: #333;">Region: <strong>{self.environment.region or 'Unknown'}</strong></p>
                </div>
                
                <div>
                    <h4 style="color: #DC143C; margin: 0 0 8px 0;">Resources</h4>
                    <p style="margin: 4px 0; color: #333;">Memory: <strong>{self.environment.max_memory_gb:.1f} GB</strong></p>
                    <p style="margin: 4px 0; color: #333;">CPU Cores: <strong>{self.environment.cpu_cores}</strong></p>
                    <p style="margin: 4px 0; color: #333;">GPU: <strong>{'Available' if self.environment.gpu_available else 'Not Available'}</strong>
                    {f' ({self.environment.gpu_memory_gb:.1f} GB)' if self.environment.gpu_available else ''}</p>
                </div>
                
                <div>
                    <h4 style="color: #DC143C; margin: 0 0 8px 0;">Network</h4>
                    <p style="margin: 4px 0; color: #333;">Internet: <strong>{'Full' if self.environment.outbound_internet else 'Limited'}</strong></p>
                    <p style="margin: 4px 0; color: #333;">Custom Domains: <strong>{'Yes' if self.environment.custom_domains else 'No'}</strong></p>
                    <p style="margin: 4px 0; color: #333;">Tunnels: <strong>{len(self.environment.tunnel_support)} supported</strong></p>
                </div>
            </div>
            
            <div style="border-top: 1px solid rgba(220,20,60,0.3); padding-top: 16px;">
                <h4 style="color: #DC143C; margin: 0 0 8px 0;">Active Optimizations</h4>
                <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                    {self._generate_optimization_badges()}
                </div>
            </div>
        </div>
        """
        
        return widgets.HTML(value=env_info)
    
    def _generate_optimization_badges(self) -> str:
        """Generate optimization badges HTML"""
        badges = []
        
        for optimization in self.adaptations:
            badge_text = optimization.replace('_', ' ').title()
            badges.append(f"""
                <span style="background: #DC143C; color: white; padding: 4px 8px; 
                            border-radius: 12px; font-size: 11px; font-weight: 600;">
                    {badge_text}
                </span>
            """)
        
        return ''.join(badges) if badges else '<span style="color: #666; font-style: italic;">No specific optimizations applied</span>'
    
    def get_tunnel_recommendations(self) -> List[Dict[str, str]]:
        """Get tunnel service recommendations for current environment"""
        recommendations = []
        
        tunnel_configs = {
            'ngrok': {
                'name': 'ngrok',
                'description': 'Secure tunnels with HTTPS',
                'priority': 'high',
                'setup_difficulty': 'easy',
                'free_tier': 'yes'
            },
            'cloudflared': {
                'name': 'Cloudflare Tunnel',
                'description': 'Fast and reliable tunneling',
                'priority': 'high',
                'setup_difficulty': 'medium',
                'free_tier': 'yes'
            },
            'localtunnel': {
                'name': 'LocalTunnel',
                'description': 'Simple local tunnel solution',
                'priority': 'medium',
                'setup_difficulty': 'easy',
                'free_tier': 'yes'
            },
            'gradio': {
                'name': 'Gradio Share',
                'description': 'Built-in sharing for ML demos',
                'priority': 'medium',
                'setup_difficulty': 'easy',
                'free_tier': 'yes'
            }
        }
        
        for tunnel_name in self.environment.tunnel_support:
            if tunnel_name in tunnel_configs:
                config = tunnel_configs[tunnel_name].copy()
                
                # Platform-specific adjustments
                if self.environment.platform == 'kaggle' and tunnel_name != 'ngrok':
                    config['priority'] = 'low'  # Kaggle works best with ngrok
                elif self.environment.platform == 'google_colab' and tunnel_name in ['ngrok', 'cloudflared']:
                    config['priority'] = 'high'  # Colab works well with these
                
                recommendations.append(config)
        
        # Sort by priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        return recommendations
    
    def apply_responsive_styling(self):
        """Apply responsive styling to the current environment"""
        # Inject performance CSS
        display(HTML(self.get_performance_css()))
        
        # Inject JavaScript polyfills
        display(HTML(self.get_javascript_polyfills()))
    
    def test_compatibility(self) -> Dict[str, Any]:
        """Test compatibility features and return results"""
        results = {
            'environment_detected': True,
            'javascript_working': False,
            'network_accessible': False,
            'gpu_detected': self.environment.gpu_available,
            'memory_sufficient': self.environment.max_memory_gb >= 4,
            'tunnel_options': len(self.environment.tunnel_support),
            'performance_score': 0
        }
        
        # Test JavaScript
        try:
            display(HTML("""
            <script>
            window.jsTestResult = true;
            console.log('JavaScript compatibility test passed');
            </script>
            """))
            results['javascript_working'] = True
        except:
            results['javascript_working'] = False
        
        # Test network access
        if self.environment.outbound_internet:
            try:
                response = requests.get('https://httpbin.org/status/200', timeout=5)
                results['network_accessible'] = response.status_code == 200
            except:
                results['network_accessible'] = False
        
        # Calculate performance score
        score = 0
        if results['memory_sufficient']: score += 25
        if results['gpu_detected']: score += 25
        if results['javascript_working']: score += 25
        if results['tunnel_options'] > 0: score += 25
        
        results['performance_score'] = score
        
        return results
    
    def display_compatibility_dashboard(self):
        """Display comprehensive compatibility dashboard"""
        # Apply styling first
        self.apply_responsive_styling()
        
        # Create dashboard components
        report_widget = self.create_compatibility_report()
        
        # Test results
        test_results = self.test_compatibility()
        test_widget = self._create_test_results_widget(test_results)
        
        # Tunnel recommendations
        tunnel_recommendations = self.get_tunnel_recommendations()
        tunnel_widget = self._create_tunnel_widget(tunnel_recommendations)
        
        # Performance metrics
        metrics_widget = self._create_metrics_widget()
        
        # Main dashboard
        dashboard = widgets.VBox([
            widgets.HTML("""
            <div class="cloud-optimized-container">
                <h2 style="color: #8B0000; text-align: center; font-family: 'Cinzel', serif; margin-bottom: 24px;">
                    🚀 Enhanced Widget System - Cloud Compatibility Dashboard
                </h2>
            </div>
            """),
            report_widget,
            test_widget,
            tunnel_widget,
            metrics_widget
        ], layout=widgets.Layout(width='100%'))
        
        display(dashboard)
    
    def _create_test_results_widget(self, results: Dict[str, Any]) -> widgets.HTML:
        """Create test results widget"""
        test_items = []
        
        for test_name, result in results.items():
            if test_name == 'performance_score':
                continue
                
            status = "✅" if result else "❌"
            color = "#46FF46" if result else "#FF4444"
            
            test_items.append(f"""
            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid rgba(220,20,60,0.1);">
                <span style="color: #333;">{test_name.replace('_', ' ').title()}</span>
                <span style="color: {color}; font-weight: bold;">{status} {result}</span>
            </div>
            """)
        
        score_color = "#46FF46" if results['performance_score'] >= 75 else "#FFA500" if results['performance_score'] >= 50 else "#FF4444"
        
        test_html = f"""
        <div style="background: rgba(139,0,0,0.05); border: 1px solid #DC143C; border-radius: 8px; padding: 16px; margin: 16px 0;">
            <h4 style="color: #8B0000; margin: 0 0 16px 0;">🧪 Compatibility Test Results</h4>
            {''.join(test_items)}
            <div style="margin-top: 16px; padding: 12px; background: rgba(220,20,60,0.1); border-radius: 6px; text-align: center;">
                <strong style="color: {score_color};">Performance Score: {results['performance_score']}/100</strong>
            </div>
        </div>
        """
        
        return widgets.HTML(value=test_html)
    
    def _create_tunnel_widget(self, recommendations: List[Dict[str, str]]) -> widgets.HTML:
        """Create tunnel recommendations widget"""
        if not recommendations:
            tunnel_html = """
            <div style="background: rgba(139,0,0,0.05); border: 1px solid #DC143C; border-radius: 8px; padding: 16px; margin: 16px 0;">
                <h4 style="color: #8B0000; margin: 0 0 16px 0;">🌐 Tunnel Recommendations</h4>
                <p style="color: #666; font-style: italic;">No tunnel services recommended for this environment.</p>
            </div>
            """
        else:
            tunnel_items = []
            for tunnel in recommendations:
                priority_color = {"high": "#46FF46", "medium": "#FFA500", "low": "#FF4444"}.get(tunnel['priority'], '#666')
                
                tunnel_items.append(f"""
                <div style="border: 1px solid rgba(220,20,60,0.2); border-radius: 6px; padding: 12px; margin: 8px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <h5 style="color: #8B0000; margin: 0;">{tunnel['name']}</h5>
                        <span style="background: {priority_color}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 10px;">
                            {tunnel['priority'].upper()}
                        </span>
                    </div>
                    <p style="color: #333; margin: 4px 0; font-size: 13px;">{tunnel['description']}</p>
                    <div style="display: flex; justify-content: space-between; font-size: 11px; color: #666;">
                        <span>Setup: {tunnel['setup_difficulty'].title()}</span>
                        <span>Free Tier: {tunnel['free_tier'].title()}</span>
                    </div>
                </div>
                """)
            
            tunnel_html = f"""
            <div style="background: rgba(139,0,0,0.05); border: 1px solid #DC143C; border-radius: 8px; padding: 16px; margin: 16px 0;">
                <h4 style="color: #8B0000; margin: 0 0 16px 0;">🌐 Recommended Tunnel Services</h4>
                {''.join(tunnel_items)}
            </div>
            """
        
        return widgets.HTML(value=tunnel_html)
    
    def _create_metrics_widget(self) -> widgets.HTML:
        """Create performance metrics widget"""
        metrics_html = f"""
        <div style="background: rgba(139,0,0,0.05); border: 1px solid #DC143C; border-radius: 8px; padding: 16px; margin: 16px 0;">
            <h4 style="color: #8B0000; margin: 0 0 16px 0;">📊 Performance Metrics</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px;">
                <div style="text-align: center; padding: 12px; background: rgba(220,20,60,0.1); border-radius: 6px;">
                    <div style="font-size: 24px; font-weight: bold; color: #8B0000;">{self.performance_metrics['widget_count']}</div>
                    <div style="font-size: 12px; color: #666;">Active Widgets</div>
                </div>
                <div style="text-align: center; padding: 12px; background: rgba(220,20,60,0.1); border-radius: 6px;">
                    <div style="font-size: 24px; font-weight: bold; color: #8B0000;">{self.performance_metrics['load_time']:.2f}s</div>
                    <div style="font-size: 12px; color: #666;">Load Time</div>
                </div>
                <div style="text-align: center; padding: 12px; background: rgba(220,20,60,0.1); border-radius: 6px;">
                    <div style="font-size: 24px; font-weight: bold; color: #8B0000;">{self.performance_metrics['memory_usage']:.1f}MB</div>
                    <div style="font-size: 12px; color: #666;">Memory Usage</div>
                </div>
            </div>
        </div>
        """
        
        return widgets.HTML(value=metrics_html)


# Factory function and demo
def create_cloud_compatibility_manager() -> CloudCompatibilityManager:
    """Factory function to create cloud compatibility manager"""
    return CloudCompatibilityManager()


def demo_cloud_compatibility():
    """Demo function to showcase cloud compatibility features"""
    print("Creating Cloud Compatibility Demo...")
    
    manager = create_cloud_compatibility_manager()
    manager.display_compatibility_dashboard()
    
    return manager


if __name__ == "__main__":
    # Demo mode
    demo_cloud_compatibility()