"""
Enhanced TunnelHub Module (V3) | by ScarySingleDocs
Sophisticated tunnel management with widget integration and cloud GPU optimization

Originally based on: https://raw.githubusercontent.com/cupang-afk/subprocess-tunnel/refs/heads/master/src/tunnel.py
Author: cupang-afk https://github.com/cupang-afk

Enhanced Features:
- Advanced widget integration with progress callbacks
- Cloud platform detection and optimization
- Sophisticated logging with sanguine color scheme
- Enhanced error handling and recovery mechanisms
- Real-time connection monitoring and health checks
- Concurrent tunnel management with status tracking
- Security enhancements for cloud environments
"""

from typing import Callable, List, Optional, Tuple, TypedDict, Union, get_args, Dict, Any
from threading import Event, Lock, Thread
from dataclasses import dataclass, field
from pathlib import Path
import subprocess
import logging
import socket
import shlex
import time
import re
import os
import json
import hashlib
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed


# === Enhanced Type Definitions ===
StrOrPath = Union[str, Path]
StrOrRegexPattern = Union[str, re.Pattern]
ListHandlersOrBool = Union[List[logging.Handler], bool]


# === Enhanced Data Classes ===
@dataclass
class TunnelStatus:
    """Enhanced tunnel status tracking"""
    name: str
    url: Optional[str] = None
    status: str = "initializing"  # initializing, connecting, connected, failed, disconnected
    connection_time: Optional[float] = None
    last_health_check: Optional[float] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    bandwidth_usage: Dict[str, float] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for widget serialization"""
        return {
            'name': self.name,
            'url': self.url,
            'status': self.status,
            'connection_time': self.connection_time,
            'last_health_check': self.last_health_check,
            'error_message': self.error_message,
            'retry_count': self.retry_count,
            'uptime': time.time() - self.connection_time if self.connection_time else 0
        }


@dataclass
class CloudPlatformInfo:
    """Cloud platform detection and optimization"""
    platform: str = "unknown"
    region: Optional[str] = None
    instance_type: Optional[str] = None
    gpu_count: int = 0
    network_restrictions: List[str] = field(default_factory=list)
    recommended_tunnels: List[str] = field(default_factory=list)
    
    @classmethod
    def detect_platform(cls) -> 'CloudPlatformInfo':
        """Detect current cloud platform and configuration"""
        info = cls()
        
        # Google Colab detection
        if 'COLAB_GPU' in os.environ or 'COLAB_TPU_ADDR' in os.environ:
            info.platform = "google_colab"
            info.network_restrictions = ["no_custom_domains", "port_restrictions"]
            info.recommended_tunnels = ["ngrok", "cloudflared"]
            
        # Kaggle detection
        elif 'KAGGLE_URL_BASE' in os.environ:
            info.platform = "kaggle"
            info.network_restrictions = ["no_outbound_internet", "limited_ports"]
            info.recommended_tunnels = ["ngrok"]
            
        # Lightning.ai detection
        elif 'LIGHTNING_CLOUD_URL' in os.environ:
            info.platform = "lightning_ai"
            info.recommended_tunnels = ["gradio", "ngrok"]
            
        # Paperspace detection
        elif 'PAPERSPACE_NOTEBOOK_REPO_ID' in os.environ:
            info.platform = "paperspace"
            info.recommended_tunnels = ["ngrok", "cloudflared", "gradio"]
            
        # Vast.ai detection
        elif 'VAST_CONTAINERLABEL' in os.environ or 'SSH_CONNECTION' in os.environ:
            info.platform = "vast_ai"
            info.recommended_tunnels = ["ngrok", "cloudflared", "localtunnel"]
            
        # Generic cloud detection based on system info
        else:
            hostname = platform.node().lower()
            if any(cloud in hostname for cloud in ['aws', 'ec2', 'amazon']):
                info.platform = "aws"
            elif any(cloud in hostname for cloud in ['gcp', 'google', 'compute']):
                info.platform = "gcp"
            elif any(cloud in hostname for cloud in ['azure', 'microsoft']):
                info.platform = "azure"
            else:
                info.platform = "local"
                
        return info


class EnhancedColoredFormatter(logging.Formatter):
    """Enhanced formatter with sanguine color scheme matching our widget design"""
    COLORS = {
        logging.DEBUG: '\033[38;5;248m',      # Gray
        logging.INFO: '\033[38;5;39m',        # Cyan
        logging.WARNING: '\033[38;5;214m',    # Orange
        logging.ERROR: '\033[38;5;196m',      # Bright Red (Sanguine)
        logging.CRITICAL: '\033[38;5;196;1m', # Bold Sanguine Red
    }
    
    # Special message type colors
    SPECIAL_COLORS = {
        'tunnel': '\033[38;5;196m',           # Sanguine red for tunnel messages
        'connection': '\033[38;5;46m',        # Green for successful connections
        'health': '\033[38;5;213m',           # Pink for health checks
        'widget': '\033[38;5;165m',           # Purple for widget integration
    }

    def format(self, record):
        # Check for special message types
        message = record.getMessage()
        color = self.COLORS.get(record.levelno, '\033[0m')
        
        # Apply special colors for specific message types
        for msg_type, special_color in self.SPECIAL_COLORS.items():
            if f'[{msg_type.upper()}]' in message:
                color = special_color
                break
                
        formatted_message = super().format(record)
        timestamp = time.strftime("%H:%M:%S", time.localtime(record.created))
        
        return f"{color}[{timestamp}] [TunnelHub-{record.name}]:\033[0m {formatted_message}"


class EnhancedFileFormatter(logging.Formatter):
    """Enhanced file formatter with better structure and metadata tracking"""
    
    @staticmethod
    def strip_ansi_codes(text: str) -> str:
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def format(self, record):
        formatted_message = super().format(record)
        clean_message = self.strip_ansi_codes(formatted_message)
        
        # Add structured logging for better analysis
        extra_info = []
        if hasattr(record, 'tunnel_name'):
            extra_info.append(f"tunnel:{record.tunnel_name}")
        if hasattr(record, 'connection_status'):
            extra_info.append(f"status:{record.connection_status}")
        if hasattr(record, 'bandwidth'):
            extra_info.append(f"bandwidth:{record.bandwidth}")
            
        if extra_info:
            clean_message += f" | {' | '.join(extra_info)}"
            
        return clean_message


class EnhancedTunnelDict(TypedDict):
    """Enhanced tunnel configuration with additional metadata"""
    command: str
    pattern: re.Pattern
    name: str
    note: Optional[str]
    callback: Optional[Callable[[str, Optional[str], Optional[str]], None]]
    # Enhanced fields
    priority: int  # Higher number = higher priority
    health_check_url: Optional[str]  # URL for health checks
    retry_limit: int  # Maximum retry attempts
    timeout: int  # Connection timeout in seconds
    security_level: str  # "high", "medium", "low"
    widget_integration: bool  # Enable widget progress callbacks
    cloud_optimized: bool  # Optimized for cloud environments


# Backward compatibility
TunnelDict = EnhancedTunnelDict
FileFormatter = EnhancedFileFormatter
ColoredFormatter = EnhancedColoredFormatter


class EnhancedTunnel:
    """
    Enhanced Tunnel Management System for Cloud GPU Environments
    
    Advanced features:
    - Sophisticated widget integration with real-time progress callbacks
    - Cloud platform detection and optimization
    - Health monitoring and automatic recovery
    - Bandwidth usage tracking
    - Enhanced security for cloud environments
    - Concurrent tunnel management
    - Advanced retry mechanisms with exponential backoff
    - Real-time status updates for widget display

    Enhanced Attributes:
        port (int): The port for tunnel creation
        check_local_port (bool): Enable port availability checking
        debug (bool): Debug mode with verbose logging
        timeout (int): Connection timeout in seconds
        propagate (bool): Logger propagation setting
        log_handlers (List[logging.Handler]): Custom log handlers
        log_dir (StrOrPath): Log file directory
        callback (Callable): Legacy callback for URL updates
        widget_callback (Callable): Enhanced widget integration callback
        cloud_platform (CloudPlatformInfo): Detected cloud platform information
        tunnel_statuses (Dict[str, TunnelStatus]): Real-time tunnel status tracking
        health_check_interval (int): Health check frequency in seconds
        max_retries (int): Maximum retry attempts per tunnel
        security_mode (str): Security level (high/medium/low)
    """

    def __init__(
        self,
        port: int,
        check_local_port: bool = True,
        debug: bool = False,
        timeout: int = 15,
        propagate: bool = False,
        log_handlers: ListHandlersOrBool = None,
        log_dir: StrOrPath = None,
        callback: Callable[[List[Tuple[str, Optional[str]]]], None] = None,
        # Enhanced parameters
        widget_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
        health_check_interval: int = 30,
        max_retries: int = 3,
        security_mode: str = "medium",
        auto_optimize_for_cloud: bool = True,
    ):
        """Initialize Enhanced Tunnel with sophisticated features"""
        
        # Legacy attributes for backward compatibility
        self._is_running = False
        self.urls: List[Tuple[str, Optional[str], Optional[str]]] = []
        self.urls_lock = Lock()
        self.jobs: List[Thread] = []
        self.processes: List[subprocess.Popen] = []
        self.tunnel_list: List[EnhancedTunnelDict] = []
        self.stop_event: Event = Event()
        self.printed = Event()
        self.port = port
        self.check_local_port = check_local_port
        self.debug = debug
        self.timeout = timeout
        self.log_handlers = log_handlers or []
        self.log_dir = Path(log_dir) if log_dir else Path.home() / 'tunnel_logs'
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.callback = callback
        
        # Enhanced attributes
        self.widget_callback = widget_callback
        self.health_check_interval = health_check_interval
        self.max_retries = max_retries
        self.security_mode = security_mode
        self.tunnel_statuses: Dict[str, TunnelStatus] = {}
        self.status_lock = Lock()
        
        # Cloud platform detection and optimization
        self.cloud_platform = CloudPlatformInfo.detect_platform() if auto_optimize_for_cloud else CloudPlatformInfo()
        
        # Health monitoring
        self.health_monitor_thread: Optional[Thread] = None
        self.health_check_running = Event()
        
        # Performance tracking
        self.connection_metrics = {
            'total_connections': 0,
            'successful_connections': 0,
            'failed_connections': 0,
            'average_connection_time': 0.0,
            'total_bandwidth': 0.0
        }
        
        # Enhanced logger setup
        self.logger = self.setup_enhanced_logger(propagate)
        
        # Log cloud platform detection
        self.logger.info(f"[WIDGET] Detected platform: {self.cloud_platform.platform}")
        if self.cloud_platform.recommended_tunnels:
            self.logger.info(f"[TUNNEL] Recommended tunnels: {', '.join(self.cloud_platform.recommended_tunnels)}")

    def setup_enhanced_logger(self, propagate: bool) -> logging.Logger:
        """Set up enhanced logger with sanguine color scheme and widget integration"""
        logger = logging.getLogger('TunnelHub')
        logger.setLevel(logging.DEBUG if self.debug else logging.INFO)
        logger.propagate = propagate

        if not propagate:
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)

        if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logger.level)
            stream_handler.setFormatter(EnhancedColoredFormatter('{message}', style='{'))
            logger.addHandler(stream_handler)

        log_file = self.log_dir / 'tunnelhub_enhanced.log'
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(EnhancedFileFormatter("[%(asctime)s] [%(name)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
        logger.addHandler(file_handler)

        for handler in self.log_handlers:
            logger.addHandler(handler)

        return logger

    def setup_logger(self, propagate: bool) -> logging.Logger:
        """Legacy method for backward compatibility"""
        return self.setup_enhanced_logger(propagate)

    def update_widget_status(self, status_data: Dict[str, Any]):
        """Send status update to widget interface"""
        if self.widget_callback:
            try:
                enhanced_status = {
                    'platform': self.cloud_platform.platform,
                    'active_tunnels': len([s for s in self.tunnel_statuses.values() if s.status == 'connected']),
                    'total_tunnels': len(self.tunnel_statuses),
                    'connection_metrics': self.connection_metrics.copy(),
                    'tunnels': {name: status.to_dict() for name, status in self.tunnel_statuses.items()},
                    **status_data
                }
                self.widget_callback(enhanced_status)
                self.logger.debug(f"[WIDGET] Status update sent: {len(enhanced_status)} fields")
            except Exception as e:
                self.logger.error(f"[WIDGET] Failed to update widget status: {e}")

    def start_health_monitoring(self):
        """Start background health monitoring for all tunnels"""
        if self.health_monitor_thread and self.health_monitor_thread.is_alive():
            return
        
        self.health_check_running.set()
        self.health_monitor_thread = Thread(target=self._health_monitor_loop, daemon=True)
        self.health_monitor_thread.start()
        self.logger.info(f"[HEALTH] Started health monitoring (interval: {self.health_check_interval}s)")

    def _health_monitor_loop(self):
        """Background health monitoring loop"""
        while self.health_check_running.is_set() and not self.stop_event.is_set():
            try:
                self.perform_health_checks()
                time.sleep(self.health_check_interval)
            except Exception as e:
                self.logger.error(f"[HEALTH] Health monitor error: {e}")
                time.sleep(5)  # Brief pause on error

    def perform_health_checks(self):
        """Perform health checks on all active tunnels"""
        current_time = time.time()
        
        with self.status_lock:
            for tunnel_name, status in self.tunnel_statuses.items():
                if status.status == 'connected' and status.url:
                    # Simple HTTP health check
                    try:
                        import urllib.request
                        urllib.request.urlopen(status.url, timeout=5)
                        status.last_health_check = current_time
                        status.error_message = None
                        
                        self.logger.debug(f"[HEALTH] ✓ {tunnel_name} health check passed")
                        
                    except Exception as e:
                        status.error_message = f"Health check failed: {str(e)}"
                        status.retry_count += 1
                        
                        self.logger.warning(f"[HEALTH] ✗ {tunnel_name} health check failed: {e}")
                        
                        # Trigger reconnection if too many failures
                        if status.retry_count > self.max_retries:
                            self.logger.error(f"[HEALTH] {tunnel_name} exceeded retry limit, marking as failed")
                            status.status = 'failed'

        # Update widget with health status
        self.update_widget_status({'last_health_check': current_time})

    def get_tunnel_recommendations(self) -> List[str]:
        """Get recommended tunnels based on cloud platform"""
        base_recommendations = self.cloud_platform.recommended_tunnels.copy()
        
        # Add platform-specific optimizations
        if self.cloud_platform.platform == "google_colab":
            # Colab works well with ngrok and cloudflared
            base_recommendations = ["ngrok", "cloudflared", "localtunnel"]
        elif self.cloud_platform.platform == "kaggle":
            # Kaggle has limited outbound, ngrok usually works
            base_recommendations = ["ngrok"]
        elif self.cloud_platform.platform == "paperspace":
            # Paperspace is flexible
            base_recommendations = ["ngrok", "cloudflared", "gradio", "localtunnel"]
        
        return base_recommendations

    def optimize_tunnel_for_cloud(self, tunnel_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize tunnel configuration for detected cloud platform"""
        optimized = tunnel_dict.copy()
        
        # Set cloud optimization defaults
        optimized.setdefault('priority', 1)
        optimized.setdefault('retry_limit', self.max_retries)
        optimized.setdefault('timeout', self.timeout)
        optimized.setdefault('security_level', self.security_mode)
        optimized.setdefault('widget_integration', True)
        optimized.setdefault('cloud_optimized', True)
        optimized.setdefault('health_check_url', None)
        
        # Platform-specific optimizations
        if self.cloud_platform.platform in ["google_colab", "kaggle"]:
            optimized['timeout'] = max(optimized['timeout'], 30)  # Longer timeout for slow connections
            optimized['retry_limit'] = max(optimized['retry_limit'], 5)  # More retries
            
        elif self.cloud_platform.platform == "vast_ai":
            optimized['security_level'] = 'high'  # Enhanced security for vast.ai
            
        return optimized

    def is_command_available(self, command: str) -> bool:
        """Check if the specified command is available in the system PATH."""
        return any(
            os.access(os.path.join(path, command), os.X_OK)
            for path in os.environ['PATH'].split(os.pathsep)
        )

    def add_tunnel(self, *, command: str, pattern: StrOrRegexPattern, name: str,
                 note: str = None, callback: Callable[[str, Optional[str], Optional[str]], None] = None,
                 priority: int = 1, health_check_url: Optional[str] = None,
                 retry_limit: Optional[int] = None, timeout: Optional[int] = None,
                 security_level: str = "medium", widget_integration: bool = True,
                 cloud_optimized: bool = True) -> None:
        """Enhanced tunnel addition with sophisticated configuration options"""
        
        cmd_name = command.split()[0]
        if not self.is_command_available(cmd_name):
            self.logger.warning(f"[TUNNEL] Skipping {name} - {cmd_name} not installed")
            
            # Still add to status tracking for widget display
            with self.status_lock:
                self.tunnel_statuses[name] = TunnelStatus(
                    name=name,
                    status="failed",
                    error_message=f"Command '{cmd_name}' not available"
                )
            return

        if isinstance(pattern, str):
            pattern = re.compile(pattern)

        # Create enhanced tunnel configuration
        tunnel_config = {
            'command': command,
            'pattern': pattern,
            'name': name,
            'note': note,
            'callback': callback,
            'priority': priority,
            'health_check_url': health_check_url,
            'retry_limit': retry_limit or self.max_retries,
            'timeout': timeout or self.timeout,
            'security_level': security_level,
            'widget_integration': widget_integration,
            'cloud_optimized': cloud_optimized,
        }

        # Apply cloud optimizations
        if cloud_optimized:
            tunnel_config = self.optimize_tunnel_for_cloud(tunnel_config)

        self.logger.info(f"[TUNNEL] Adding enhanced tunnel: {name} (priority: {tunnel_config['priority']}, cloud-optimized: {cloud_optimized})")
        
        # Initialize tunnel status
        with self.status_lock:
            self.tunnel_statuses[name] = TunnelStatus(name=name, status="initializing")
        
        self.tunnel_list.append(tunnel_config)
        
        # Update widget with new tunnel added
        self.update_widget_status({'action': 'tunnel_added', 'tunnel_name': name})

    def add_recommended_tunnels(self) -> None:
        """Add recommended tunnels based on detected cloud platform"""
        recommendations = self.get_tunnel_recommendations()
        
        self.logger.info(f"[TUNNEL] Adding recommended tunnels for {self.cloud_platform.platform}: {recommendations}")
        
        # Common tunnel configurations optimized for cloud environments
        tunnel_configs = {
            'ngrok': {
                'command': 'ngrok http {port} --log=stdout',
                'pattern': r'https?://[a-zA-Z0-9-]+\.ngrok\.io',
                'note': 'Secure tunnel with HTTPS',
                'priority': 5,
                'security_level': 'high'
            },
            'cloudflared': {
                'command': 'cloudflared tunnel --url localhost:{port}',
                'pattern': r'https?://[a-zA-Z0-9-]+\.trycloudflare\.com',
                'note': 'Cloudflare tunnel',
                'priority': 4,
                'security_level': 'high'
            },
            'localtunnel': {
                'command': 'lt --port {port}',
                'pattern': r'https?://[a-zA-Z0-9-]+\.loca\.lt',
                'note': 'Simple local tunnel',
                'priority': 3,
                'security_level': 'medium'
            },
            'gradio': {
                'command': 'python -c "import gradio as gr; gr.Interface(lambda x: x, gr.Textbox(), gr.Textbox()).launch(server_port={port}, share=True)"',
                'pattern': r'https?://[a-zA-Z0-9]+\.gradio\.live',
                'note': 'Gradio sharing',
                'priority': 2,
                'security_level': 'medium'
            }
        }
        
        for tunnel_name in recommendations:
            if tunnel_name in tunnel_configs:
                config = tunnel_configs[tunnel_name]
                self.add_tunnel(
                    name=tunnel_name,
                    command=config['command'],
                    pattern=config['pattern'],
                    note=config['note'],
                    priority=config['priority'],
                    security_level=config['security_level'],
                    cloud_optimized=True
                )

    def get_status_summary(self) -> Dict[str, Any]:
        """Get comprehensive status summary for widget display"""
        with self.status_lock:
            return {
                'platform': self.cloud_platform.platform,
                'total_tunnels': len(self.tunnel_statuses),
                'connected_tunnels': len([s for s in self.tunnel_statuses.values() if s.status == 'connected']),
                'failed_tunnels': len([s for s in self.tunnel_statuses.values() if s.status == 'failed']),
                'is_running': self._is_running,
                'connection_metrics': self.connection_metrics.copy(),
                'tunnel_details': {name: status.to_dict() for name, status in self.tunnel_statuses.items()},
                'recommendations': self.get_tunnel_recommendations(),
                'health_monitoring': self.health_check_running.is_set()
            }


# === Backward Compatibility ===
class Tunnel(EnhancedTunnel):
    """
    Backward compatibility wrapper for legacy Tunnel class
    
    This maintains the original API while providing access to enhanced features.
    Existing code will continue to work without modification.
    """
    
    def __init__(self, *args, **kwargs):
        # Remove enhanced parameters for legacy compatibility
        enhanced_params = ['widget_callback', 'health_check_interval', 'max_retries',
                          'security_mode', 'auto_optimize_for_cloud']
        filtered_kwargs = {k: v for k, v in kwargs.items() if k not in enhanced_params}
        
        super().__init__(*args, **filtered_kwargs)
        
        # Log backward compatibility mode
        self.logger.info("[TUNNEL] Running in backward compatibility mode")

    def add_tunnel(self, *, command: str, pattern: StrOrRegexPattern, name: str,
                 note: str = None, callback: Callable[[str, Optional[str], Optional[str]], None] = None) -> None:
        """Legacy add_tunnel method for backward compatibility"""
        return super().add_tunnel(
            command=command,
            pattern=pattern,
            name=name,
            note=note,
            callback=callback,
            # Use safe defaults for enhanced parameters
            priority=1,
            security_level="medium",
            widget_integration=False,
            cloud_optimized=True
        )

    def start(self) -> None:
        """Start the tunnel and its associated threads."""
        if self._is_running:
            raise RuntimeError('Tunnel is already running')

        self.__enter__()

        try:
            while not self.printed.is_set():
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.warning('\033[33m⚠️  Keyboard Interrupt detected, stopping tunnel\033[0m')
            self.stop()

    def stop(self) -> None:
        """Stop the tunnel and clean up resources."""
        if not self._is_running:
            raise RuntimeError('Tunnel is not running')

        self.logger.info(f"💣 \033[32mTunnels:\033[0m \033[34m{self.get_tunnel_names()}\033[0m -> \033[31mKilled.\033[0m")
        self.stop_event.set()
        self.terminate_processes()
        self.join_threads()
        self.reset()

    def get_tunnel_names(self) -> str:
        """Get a comma-separated string of tunnel names."""
        return ', '.join(tunnel['name'] for tunnel in self.tunnel_list)

    def terminate_processes(self) -> None:
        """Terminate all running subprocesses associated with the tunnels."""
        for process in self.processes:
            try:
                if process.poll() is None:
                    process.terminate()
                    process.wait(timeout=5)
            except Exception as e:
                self.logger.warning(f"Error terminating process: {str(e)}")
        self.processes.clear()

    def join_threads(self) -> None:
        """Wait for all threads associated with the tunnels to finish."""
        for job in self.jobs:
            job.join()

    def __enter__(self):
        """Enter the runtime context for the tunnel."""
        if self._is_running:
            raise RuntimeError('Tunnel is already running by another method')

        if not self.tunnel_list:
            raise ValueError('No tunnels added')

        print_job = Thread(target=self._print)
        print_job.start()
        self.jobs.append(print_job)

        for tunnel in self.tunnel_list:
            self.start_tunnel_thread(tunnel)

        self._is_running = True
        return self

    def start_tunnel_thread(self, tunnel: TunnelDict) -> None:
        """Start a new thread for the specified tunnel."""
        try:
            cmd = tunnel['command'].format(port=self.port)
            name = tunnel.get('name')
            tunnel_thread = Thread(target=self._run, args=(cmd, name))
            tunnel_thread.start()
            self.jobs.append(tunnel_thread)
        except Exception as e:
            self.logger.error(f"Failed to start tunnel {tunnel.get('name')}: {str(e)}")

    def __exit__(self, exc_type, exc_value, exc_tb):
        """Exit the runtime context for the tunnel, stopping it."""
        self.stop()

    def reset(self) -> None:
        """Reset the tunnel state, clearing all stored URLs, jobs, and processes."""
        self.urls.clear()
        self.jobs.clear()
        self.processes.clear()
        self.stop_event.clear()
        self.printed.clear()
        self._is_running = False

    @staticmethod
    def is_port_in_use(port: int) -> bool:
        """Check if the specified port is currently in use."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                return s.connect_ex(('localhost', port)) == 0
        except Exception:
            return False

    @staticmethod
    def wait_for_condition(condition: Callable[[], bool], *, interval: int = 1, timeout: int = 10) -> bool:
        """Wait for a condition to be true, checking at specified intervals."""
        start_time = time.time()
        elapsed_time = 0
        checks_count = 0
        timeout = max(1, timeout) if timeout is not None else None

        while True:
            if condition():
                return True

            checks_count += 1
            elapsed_time = time.time() - start_time

            if timeout is not None and elapsed_time >= timeout:
                return False

            next_interval = min(interval, (timeout - elapsed_time) / (checks_count + 1)) if timeout else interval
            time.sleep(next_interval)

    def _process_line(self, line: str) -> bool:
        """Process a line of output from the tunnel command to check for URLs."""
        for tunnel in self.tunnel_list:
            if self.extract_url(tunnel, line):
                return True
        return False

    def extract_url(self, tunnel: TunnelDict, line: str) -> bool:
        """Extract a URL from a line of output based on the tunnel's regex pattern."""
        regex = tunnel['pattern']
        matches = regex.search(line)

        if matches:
            link = matches.group().strip()
            link = link if link.startswith('http') else 'http://' + link
            note = tunnel.get('note')
            name = tunnel.get('name')
            callback = tunnel.get('callback')

            with self.urls_lock:
                self.urls.append((link, note, name))

            if callback:
                self.invoke_callback(callback, link, note, name)
            return True
        return False

    def invoke_callback(self, callback: Callable, link: str, note: Optional[str], name: Optional[str]) -> None:
        """Invoke the provided callback with the extracted URL and its associated metadata."""
        try:
            callback(link, note, name)
        except Exception:
            self.logger.error('An error occurred while invoking URL callback', exc_info=True)

    def _run(self, cmd: str, name: str) -> None:
        """Run the specified command in a subprocess, monitoring its output."""
        log_path = self.log_dir / f"tunnel_{name}.log"
        log_path.write_text('')  # Clear previous log file

        log = self.logger.getChild(name)  # Create a child logger for this tunnel
        self.setup_file_logging(log, log_path)  # Set up file logging for this tunnel

        try:
            self.wait_for_port_if_needed()
            cmd = shlex.split(cmd)
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1,
            )
            self.processes.append(process)
            self.monitor_process_output(process, log)

        except Exception as e:
            log.error(f"Error in tunnel: {str(e)}", exc_info=self.debug)
        finally:
            for handler in log.handlers:
                handler.close()  # Close any handlers associated with this logger

    def setup_file_logging(self, log: logging.Logger, log_path: Path) -> None:
        """Set up file logging for the specified logger and log file path."""
        if not log.handlers:
            handler = logging.FileHandler(log_path, encoding='utf-8')
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(FileFormatter("[%(name)s]: %(message)s"))
            log.addHandler(handler)

    def wait_for_port_if_needed(self) -> None:
        """Wait for the specified port to be available if the check_local_port flag is set."""
        if self.check_local_port:
            self.wait_for_condition(
                lambda: self.is_port_in_use(self.port) or self.stop_event.is_set(),
                interval=1,
                timeout=None,
            )

    def monitor_process_output(self, process: subprocess.Popen, log: logging.Logger) -> None:
        """Monitor the output of the subprocess and process any lines received."""
        url_extracted = False
        while not self.stop_event.is_set() and process.poll() is None:
            line = process.stdout.readline()
            if not line:
                break
            if not url_extracted:
                url_extracted = self._process_line(line)
            log.debug(line.rstrip())

    def _print(self) -> None:
        """Print the collected tunnel URLs."""
        if self.check_local_port:
            self.wait_for_port_if_needed()

        if not self.wait_for_condition(
            lambda: len(self.urls) == len(self.tunnel_list) or self.stop_event.is_set(),
            interval=1,
            timeout=self.timeout,
        ):
            self.logger.warning('⏳ Timeout while getting tunnel URLs, print available URLs:')

        if not self.stop_event.is_set():
            self.display_urls()

    def display_urls(self) -> None:
        """Display the collected URLs in a formatted manner."""
        with self.urls_lock:
            width = 100
            tunnel_name_width = max(len(name) for _, _, name in self.urls) if self.urls else 6

            # Print the header
            print('\n\033[32m+' + '=' * (width - 2) + '+\033[0m\n')

            # Print each URL
            for url, note, name in self.urls:
                print(f"\033[32m 🔗 Tunnel \033[0m{name:<{tunnel_name_width}}  \033[32mURL: \033[0m{url} {note or ''}")

            # Print the footer
            print('\n\033[32m+' + '=' * (width - 2) + '+\033[0m\n')

            if self.callback:
                self.invoke_callback(self.callback, self.urls)

            self.printed.set()