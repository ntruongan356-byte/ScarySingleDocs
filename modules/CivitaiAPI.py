"""
Enhanced CivitAi API Module (V3) | by ScarySingleDocs
Optimized for sophisticated widget integration and cloud GPU environments
"""

from urllib.parse import urlparse, parse_qs, urlencode
from typing import Optional, Union, Tuple, Dict, Any, List, Callable
from dataclasses import dataclass, field
from pathlib import Path
from PIL import Image
import requests
import json
import os
import re
import io
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed


# === Enhanced Logger Utility ===
class APILogger:
    """Sophisticated logger with progress tracking for widget integration"""
    def __init__(self, verbose: bool = True, progress_callback: Optional[Callable] = None):
        self.verbose = verbose
        self.progress_callback = progress_callback
        self.download_stats = {
            'total_files': 0,
            'completed_files': 0,
            'failed_files': 0,
            'total_bytes': 0,
            'downloaded_bytes': 0
        }

    def log(self, msg: str, level: str = "info", progress: Optional[float] = None):
        if not self.verbose and level != "error":
            return
            
        # Enhanced color scheme matching our sanguine theme
        colors = {
            "error": "\033[38;5;196m",      # Bright red
            "success": "\033[38;5;46m",     # Bright green
            "warning": "\033[38;5;214m",    # Orange
            "info": "\033[38;5;39m",        # Cyan
            "download": "\033[38;5;196m",   # Sanguine red
            "progress": "\033[38;5;213m"    # Pink
        }
        
        reset = "\033[0m"
        timestamp = time.strftime("%H:%M:%S")
        
        print(f"{colors.get(level, colors['info'])}[{timestamp}] API {level.title()}:{reset} {msg}")
        
        # Send progress update to widget if callback provided
        if self.progress_callback and progress is not None:
            self.progress_callback(progress, msg, level)

    def update_download_progress(self, filename: str, downloaded: int, total: int):
        """Update download progress with sophisticated tracking"""
        if total > 0:
            percentage = (downloaded / total) * 100
            self.log(f"Downloading {filename}: {percentage:.1f}% ({downloaded}/{total} bytes)",
                    "progress", percentage)

    def log_download_complete(self, filename: str, size: int, duration: float):
        """Log successful download with statistics"""
        speed = size / duration / 1024 / 1024 if duration > 0 else 0
        self.download_stats['completed_files'] += 1
        self.download_stats['downloaded_bytes'] += size
        
        self.log(f"✓ {filename} downloaded successfully ({size/1024/1024:.1f}MB in {duration:.1f}s @ {speed:.1f}MB/s)",
                "success")

    def log_download_error(self, filename: str, error: str):
        """Log download error with enhanced formatting"""
        self.download_stats['failed_files'] += 1
        self.log(f"✗ Failed to download {filename}: {error}", "error")

    def get_stats_summary(self) -> Dict[str, Any]:
        """Get comprehensive download statistics"""
        return {
            'total_files': self.download_stats['total_files'],
            'completed_files': self.download_stats['completed_files'],
            'failed_files': self.download_stats['failed_files'],
            'success_rate': (self.download_stats['completed_files'] / max(1, self.download_stats['total_files'])) * 100,
            'total_downloaded': self.download_stats['downloaded_bytes'] / 1024 / 1024,  # MB
        }


# === Enhanced Model Data ===
@dataclass
class ModelData:
    """Enhanced model data with progress tracking and widget integration"""
    download_url: str
    clean_url: str
    model_name: str
    model_type: str
    version_id: str
    model_id: str
    image_url: Optional[str] = None
    image_name: Optional[str] = None
    early_access: bool = False
    base_model: Optional[str] = None
    trained_words: Optional[List[str]] = None
    sha256: Optional[str] = None
    
    # Enhanced metadata for widget integration
    file_size: Optional[int] = None
    download_status: str = "pending"  # pending, downloading, completed, failed
    download_progress: float = 0.0
    download_speed: float = 0.0
    estimated_time: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    rating: Optional[float] = None
    nsfw_level: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for widget serialization"""
        return {
            'model_name': self.model_name,
            'model_type': self.model_type,
            'base_model': self.base_model,
            'version_id': self.version_id,
            'model_id': self.model_id,
            'file_size': self.file_size,
            'download_status': self.download_status,
            'download_progress': self.download_progress,
            'tags': self.tags,
            'rating': self.rating,
            'trained_words': self.trained_words or []
        }

    def update_progress(self, progress: float, speed: float = 0.0):
        """Update download progress with speed calculation"""
        self.download_progress = min(100.0, max(0.0, progress))
        self.download_speed = speed
        
        if speed > 0 and self.file_size and self.file_size > 0:
            remaining_bytes = self.file_size * (100 - progress) / 100
            remaining_seconds = remaining_bytes / (speed * 1024 * 1024)  # speed in MB/s
            
            if remaining_seconds > 60:
                self.estimated_time = f"{remaining_seconds/60:.1f}m"
            else:
                self.estimated_time = f"{remaining_seconds:.0f}s"
        else:
            # Set a default ETA when file size is unknown
            self.estimated_time = "Calculating..." if speed > 0 else None


# === Enhanced Main API ===
class CivitAiAPI:
    """
    Enhanced CivitAI API with sophisticated download management and widget integration
    
    Features:
    - Progress tracking with callbacks
    - Concurrent downloads
    - Intelligent retry mechanisms
    - Caching for better performance
    - Enhanced error handling
    - Widget integration support
    """

    BASE_URL = 'https://civitai.com/api/v1'
    SUPPORTED_TYPES = {'Checkpoint', 'TextualInversion', 'LORA', 'Hypernetwork', 'AestheticGradient'}
    IS_KAGGLE = 'KAGGLE_URL_BASE' in os.environ
    
    # Enhanced configuration
    MAX_CONCURRENT_DOWNLOADS = 3
    RETRY_ATTEMPTS = 3
    RETRY_DELAY = 2.0
    CHUNK_SIZE = 8192
    TIMEOUT = 30

    def __init__(self,
                 token: Optional[str] = None,
                 log: bool = True,
                 progress_callback: Optional[Callable] = None,
                 max_workers: int = 3):
        self.token = token or '65b66176dcf284b266579de57fbdc024'  # Default token
        self.logger = APILogger(verbose=log, progress_callback=progress_callback)
        self.progress_callback = progress_callback
        self.max_workers = min(max_workers, self.MAX_CONCURRENT_DOWNLOADS)
        
        # Cache for API responses
        self._cache = {}
        self._cache_timeout = 300  # 5 minutes
        
        # Active downloads tracking
        self.active_downloads = {}
        self.download_lock = threading.Lock()
        
        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ScarySingleDocs/3.0 (Enhanced Widget Integration)',
            'Accept': 'application/json',
        })
        
        if self.token:
            self.session.headers['Authorization'] = f'Bearer {self.token}'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Clean up resources"""
        if hasattr(self, 'session'):
            self.session.close()

    # === Core Helpers ===
    def _build_url(self, endpoint: str) -> str:
        """Construct full API URL for given endpoint"""
        return f"{self.BASE_URL}/{endpoint}"

    # === Enhanced Caching System ===
    def _get_cache_key(self, url: str) -> str:
        """Generate cache key for URL"""
        import hashlib
        return hashlib.md5(url.encode()).hexdigest()

    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cache entry is still valid"""
        if cache_key not in self._cache:
            return False
        
        entry_time = self._cache[cache_key].get('timestamp', 0)
        return time.time() - entry_time < self._cache_timeout

    def _get_from_cache(self, cache_key: str) -> Optional[Dict]:
        """Get data from cache if valid"""
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]['data']
        return None

    def _store_in_cache(self, cache_key: str, data: Dict):
        """Store data in cache with timestamp"""
        self._cache[cache_key] = {
            'data': data,
            'timestamp': time.time()
        }

    def _get(self, url: str, use_cache: bool = True) -> Optional[Dict]:
        """Enhanced GET request with caching and retry logic"""
        # Check cache first
        if use_cache:
            cache_key = self._get_cache_key(url)
            cached_data = self._get_from_cache(cache_key)
            if cached_data:
                self.logger.log(f"Cache hit for: {url}", "info")
                return cached_data
        
        # Make request with retry logic
        for attempt in range(self.RETRY_ATTEMPTS):
            try:
                self.logger.log(f"API request (attempt {attempt + 1}): {url}", "info")
                response = self.session.get(url, timeout=self.TIMEOUT)
                response.raise_for_status()
                
                result = response.json()
                
                # Store in cache
                if use_cache:
                    self._store_in_cache(cache_key, result)
                
                return result
                
            except requests.exceptions.RequestException as e:
                self.logger.log(f"API request attempt {attempt + 1} failed: {str(e)}", "warning")
                if attempt < self.RETRY_ATTEMPTS - 1:
                    time.sleep(self.RETRY_DELAY * (attempt + 1))  # Exponential backoff
                else:
                    self.logger.log(f"All API request attempts failed for: {url}", "error")
        
        return None

    def _extract_version_id(self, url: str) -> Optional[str]:
        """Extract version ID from various CivitAI URL formats"""
        if not url.startswith(('http://', 'https://')):
            self.logger.log("Invalid URL format", "error")
            return None

        if 'modelVersionId=' in url:
            return url.split('modelVersionId=')[1].split('&')[0]

        if 'civitai.com/models/' in url:
            model_id = url.split('/models/')[1].split('/')[0].split('?')[0]
            if model_id.isdigit():
                model_data = self._get(self._build_url(f"models/{model_id}"))
                return model_data.get('modelVersions', [{}])[0].get('id') if model_data else None

        if '/api/download/models/' in url:
            return url.split('/api/download/models/')[1].split('?')[0]

        self.logger.log(f"Unsupported URL format: {url}", "error")
        return None

    def _process_url(self, download_url: str) -> Tuple[str, str]:
        """Sanitize and sign download URL"""
        parsed = urlparse(download_url)
        query = parse_qs(parsed.query)
        query.pop('token', None)
        clean_url = parsed._replace(query=urlencode(query, doseq=True)).geturl()
        final_url = f"{clean_url}?token={self.token}" if self.token else clean_url
        return clean_url, final_url

    def _get_preview(self, images: List[Dict], name: str, resize: Optional[int] = 512) -> Tuple[Optional[str], Optional[str]]:
        """Extract a valid preview image URL and filename, with optional resizing via width in URL"""
        for img in images:
            url = img.get('url', '')
            if self.IS_KAGGLE and img.get('nsfwLevel', 0) >= 4:
                continue
            if any(url.lower().endswith(ext) for ext in ['.gif', '.mp4', '.webm']):
                continue
            ext = url.split('.')[-1].split('?')[0]
            if resize is not None:
                # Replace /width=XXXX/ with /width=resize/ if present
                url = re.sub(r"/width=\d+/", f"/width={resize}/", url)
            return url, f"{Path(name).stem}.preview.{ext}"
        return None, None

    def _parse_model_name(self, data: Dict, filename: Optional[str]) -> Tuple[str, str]:
        """Generate final model filename from metadata"""
        name = data['files'][0]['name']
        ext = name.split('.')[-1]
        if filename and '.' not in filename:
            filename += f".{ext}"
        return data['model']['type'], filename or name

    def _early_access_check(self, data: Dict) -> bool:
        """Check if model is gated behind Early Access"""
        ea = data.get('availability') == 'EarlyAccess' or data.get('earlyAccessEndsAt')
        if ea:
            model_id = data.get('modelId')
            version_id = data.get('id')
            self.logger.log(f"Requires Early Access: https://civitai.com/models/{model_id}?modelVersionId={version_id}", "warning")
        return ea

    def get_sha256(self, data: Optional[dict] = None, version_id: Optional[str] = None) -> Optional[str]:
        """
        Get the model's sha256 hash from version data or by version_id.
        If data is not provided, it will be loaded using version_id.
        """
        if data is None and version_id is not None:
            data = self._get(self._build_url(f"model-versions/{version_id}"))
        if not data:
            return None
        return data.get("files", [{}])[0].get("hashes", {}).get("SHA256")

    # === sdAIgen ===
    def validate_download(self, url: str, file_name: Optional[str] = None) -> Optional[ModelData]:
        version_id = self._extract_version_id(url)
        if not version_id:
            return None

        data = self._get(self._build_url(f"model-versions/{version_id}"))
        if not data:
            return None

        if self._early_access_check(data):
            return None

        model_type, name = self._parse_model_name(data, file_name)
        clean_url, full_url = self._process_url(data['downloadUrl'])

        preview_url, preview_name = (None, None)
        if model_type in self.SUPPORTED_TYPES:
            preview_url, preview_name = self._get_preview(data.get('images', []), name)

        return ModelData(
            download_url=full_url,
            clean_url=clean_url,
            model_name=name,
            model_type=model_type,
            version_id=data['id'],
            model_id=data['modelId'],
            early_access=False,
            image_url=preview_url,
            image_name=preview_name,
            base_model=data.get("baseModel"),
            trained_words=data.get("trainedWords"),
            sha256=self.get_sha256(data)
        )

    # === General ===
    def get_model_data(self, url: str) -> Optional[Dict[str, Any]]:
        """Fetch full model version metadata from CivitAI by URL"""
        version_id = self._extract_version_id(url)
        if not version_id:
            self.logger.log(f"Cannot get model data — failed to extract version ID from URL: {url}", "error")
            return None

        data = self._get(self._build_url(f"model-versions/{version_id}"))
        if not data:
            self.logger.log(f"Failed to retrieve model version data for ID: {version_id}", "error")

        return data

    def get_model_versions(self, model_id: str) -> Optional[List[Dict]]:
        """Get all available versions of a model by ID"""
        data = self._get(self._build_url(f"models/{model_id}"))
        return data.get("modelVersions") if data else None

    def find_by_sha256(self, sha256: str) -> Optional[Dict]:
        """Find model version data by SHA256 hash"""
        return self._get(self._build_url(f"model-versions/by-hash/{sha256}"))

    def download_preview_image(self, model_data: ModelData, save_path: Optional[Union[str, Path]] = None, resize: bool = False):
        """
        Download and save model preview image.

        Args:
            model_data: ModelData object with preview metadata
            save_path: Directory path (str or Path) where image will be saved. Defaults to current directory.
            resize: If True, resize image to 512px max (default: False)
        """
        if model_data is None:
            self.logger.log("ModelData is None — skipping download_preview_image", "warning")
            return

        if not model_data.image_url:
            self.logger.log("No preview image URL available", "warning")
            return

        save_dir = Path(save_path) if save_path else Path.cwd()
        save_dir.mkdir(parents=True, exist_ok=True)
        file_path = save_dir / model_data.image_name

        if file_path.exists():
            return

        try:
            res = requests.get(model_data.image_url, timeout=30)
            res.raise_for_status()
            img_data = self._resize_image(res.content) if resize else io.BytesIO(res.content)
            file_path.write_bytes(img_data.read())
            self.logger.log(f"Saved preview: {file_path}", "success")
        except Exception as e:
            self.logger.log(f"Failed to download preview: {e}", "error")

    def _resize_image(self, raw: bytes, size: int = 512) -> io.BytesIO:
        """Resize image to target size while preserving aspect ratio"""
        try:
            img = Image.open(io.BytesIO(raw))
            w, h = img.size
            new_size = (size, int(h * size / w)) if w > h else (int(w * size / h), size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            output = io.BytesIO()
            img.save(output, format='PNG')
            output.seek(0)
            return output
        except Exception as e:
            self.logger.log(f"Resize failed: {e}", "warning")
            return io.BytesIO(raw)

    def save_model_info(self, model_data: ModelData, save_path: Optional[Union[str, Path]] = None):
        """
        Save model metadata to a JSON file.

        Args:
            model_data: ModelData object
            save_path: Directory path (str or Path) to save metadata. Defaults to current directory.
        """
        if model_data is None:
            self.logger.log("ModelData is None — skipping save_model_info", "warning")
            return

        save_dir = Path(save_path) if save_path else Path.cwd()
        save_dir.mkdir(parents=True, exist_ok=True)
        info_file = save_dir / f"{Path(model_data.model_name).stem}.json"

        if info_file.exists():
            return

        base_mapping = {
            'SD 1': 'SD1', 'SD 1.5': 'SD1', 'SD 2': 'SD2', 'SD 3': 'SD3',
            'SDXL': 'SDXL', 'Pony': 'SDXL', 'Illustrious': 'SDXL',
        }
        info = {
            "model_type": model_data.model_type,
            "sd_version": next((v for k, v in base_mapping.items() if k in (model_data.base_model or '')), ''),
            "modelId": model_data.model_id,
            "modelVersionId": model_data.version_id,
            "activation_text": ', '.join(model_data.trained_words or []),
            "sha256": model_data.sha256
        }

        try:
            info_file.write_text(json.dumps(info, indent=4))
            self.logger.log(f"Saved model info: {info_file}", "success")
        except Exception as e:
            self.logger.log(f"Failed to save info: {e}", "error")

    # === Enhanced Download Methods ===
    def download_model_with_progress(self,
                                   model_data: ModelData,
                                   save_path: Union[str, Path],
                                   progress_callback: Optional[Callable[[float, str], None]] = None) -> bool:
        """
        Download model with sophisticated progress tracking and widget integration
        
        Args:
            model_data: Enhanced ModelData object
            save_path: Path to save the downloaded file
            progress_callback: Optional callback for progress updates (progress, status_message)
        
        Returns:
            bool: True if download successful, False otherwise
        """
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        if save_path.exists():
            self.logger.log(f"File already exists: {save_path}", "info")
            model_data.download_status = "completed"
            model_data.download_progress = 100.0
            if progress_callback:
                progress_callback(100.0, "File already exists")
            return True
        
        try:
            model_data.download_status = "downloading"
            start_time = time.time()
            
            # Make request with stream=True for progress tracking
            response = self.session.get(model_data.download_url, stream=True, timeout=self.TIMEOUT)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            model_data.file_size = total_size
            downloaded_size = 0
            
            self.logger.log(f"Starting download: {model_data.model_name} ({total_size / (1024*1024):.1f} MB)", "download")
            
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        
                        # Calculate progress and speed
                        if total_size > 0:
                            progress = (downloaded_size / total_size) * 100
                            elapsed_time = time.time() - start_time
                            speed = downloaded_size / (elapsed_time * 1024 * 1024) if elapsed_time > 0 else 0  # MB/s
                            
                            model_data.update_progress(progress, speed)
                            
                            # Widget progress callback
                            if progress_callback:
                                status_msg = f"Downloading... {speed:.1f} MB/s"
                                if model_data.estimated_time:
                                    status_msg += f" (ETA: {model_data.estimated_time})"
                                progress_callback(progress, status_msg)
                            
                            # Logger progress update
                            if int(progress) % 10 == 0:  # Update every 10%
                                self.logger.update_download_progress(model_data.model_name, downloaded_size, total_size)
            
            # Download completed
            duration = time.time() - start_time
            model_data.download_status = "completed"
            model_data.download_progress = 100.0
            
            self.logger.log_download_complete(model_data.model_name, downloaded_size, duration)
            
            if progress_callback:
                progress_callback(100.0, "Download completed successfully!")
            
            return True
            
        except Exception as e:
            model_data.download_status = "failed"
            self.logger.log_download_error(model_data.model_name, str(e))
            
            if progress_callback:
                progress_callback(0.0, f"Download failed: {str(e)}")
            
            # Clean up partial file
            if save_path.exists():
                save_path.unlink()
            
            return False

    def download_multiple_models(self,
                                model_list: List[Tuple[ModelData, Path]],
                                progress_callback: Optional[Callable[[int, int, str], None]] = None) -> Dict[str, bool]:
        """
        Download multiple models concurrently with progress tracking
        
        Args:
            model_list: List of (ModelData, save_path) tuples
            progress_callback: Optional callback for overall progress (completed, total, current_model)
        
        Returns:
            Dict mapping model names to success status
        """
        results = {}
        
        def download_single(model_data: ModelData, save_path: Path) -> bool:
            """Single model download wrapper"""
            with self.download_lock:
                self.active_downloads[model_data.model_name] = {
                    'status': 'downloading',
                    'progress': 0.0,
                    'start_time': time.time()
                }
            
            def model_progress_callback(progress: float, status: str):
                with self.download_lock:
                    if model_data.model_name in self.active_downloads:
                        self.active_downloads[model_data.model_name]['progress'] = progress
                        self.active_downloads[model_data.model_name]['status'] = status
            
            success = self.download_model_with_progress(model_data, save_path, model_progress_callback)
            
            with self.download_lock:
                if model_data.model_name in self.active_downloads:
                    self.active_downloads[model_data.model_name]['status'] = 'completed' if success else 'failed'
                    if not success:
                        del self.active_downloads[model_data.model_name]
            
            return success
        
        # Initialize download stats
        total_models = len(model_list)
        completed_models = 0
        
        self.logger.download_stats['total_files'] = total_models
        
        # Execute downloads with thread pool
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_model = {
                executor.submit(download_single, model_data, save_path): model_data.model_name
                for model_data, save_path in model_list
            }
            
            for future in as_completed(future_to_model):
                model_name = future_to_model[future]
                try:
                    success = future.result()
                    results[model_name] = success
                    completed_models += 1
                    
                    if progress_callback:
                        progress_callback(completed_models, total_models, model_name)
                    
                    self.logger.log(f"Model {completed_models}/{total_models} complete: {model_name} ({'✓' if success else '✗'})", "info")
                    
                except Exception as e:
                    results[model_name] = False
                    self.logger.log(f"Unexpected error downloading {model_name}: {e}", "error")
        
        # Final statistics
        stats = self.logger.get_stats_summary()
        self.logger.log(f"Download batch complete: {stats['completed_files']}/{stats['total_files']} successful ({stats['success_rate']:.1f}%)", "info")
        
        return results

    def get_download_status(self, model_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get current download status for widget display
        
        Args:
            model_name: Specific model name, or None for all active downloads
        
        Returns:
            Dictionary with download status information
        """
        with self.download_lock:
            if model_name:
                return self.active_downloads.get(model_name, {})
            
            return {
                'active_downloads': dict(self.active_downloads),
                'total_active': len(self.active_downloads),
                'statistics': self.logger.get_stats_summary()
            }

    def cancel_download(self, model_name: str) -> bool:
        """
        Cancel an active download
        
        Args:
            model_name: Name of the model to cancel
        
        Returns:
            bool: True if cancellation was successful
        """
        with self.download_lock:
            if model_name in self.active_downloads:
                self.active_downloads[model_name]['status'] = 'cancelled'
                self.logger.log(f"Download cancelled: {model_name}", "warning")
                return True
            
            return False

    def clear_cache(self):
        """Clear the API response cache"""
        self._cache.clear()
        self.logger.log("API cache cleared", "info")

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics for monitoring"""
        valid_entries = sum(1 for key in self._cache.keys() if self._is_cache_valid(key))
        
        return {
            'total_entries': len(self._cache),
            'valid_entries': valid_entries,
            'expired_entries': len(self._cache) - valid_entries,
            'cache_timeout': self._cache_timeout,
            'memory_usage_mb': len(str(self._cache)) / (1024 * 1024)  # Rough estimate
        }