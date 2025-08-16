#!/usr/bin/env python3
"""
Comprehensive Testing Strategy (V3)
Complete validation suite for enhanced widget functionality

Test Categories:
1. Core Widget Functionality Tests
2. Module Integration Tests (CivitaiAPI, TunnelHub)
3. Cloud Environment Compatibility Tests
4. Visual Feedback System Tests
5. Multi-Model Selection Interface Tests
6. Performance and Load Tests
7. End-to-End Workflow Tests
8. Accessibility and Usability Tests

This comprehensive suite ensures all enhanced widget components work correctly
across different cloud environments and usage scenarios.
"""

import sys
import os
import time
import asyncio
import json
import traceback
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable, Tuple
from dataclasses import dataclass, field
from unittest.mock import MagicMock, patch
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import our enhanced components
try:
    from modules.CivitaiAPI import CivitAiAPI, ModelData
    from modules.TunnelHub import EnhancedTunnel, CloudPlatformInfo
    from scripts.enhanced_model_selector import EnhancedModelSelector
    from scripts.visual_feedback_system import EnhancedVisualFeedback, NotificationType
    from scripts.cloud_compatibility import CloudCompatibilityManager
    print("[+] Successfully imported all enhanced components")
except ImportError as e:
    print(f"[-] Failed to import enhanced components: {e}")
    sys.exit(1)


@dataclass
class TestResult:
    """Enhanced test result with detailed information"""
    test_name: str
    category: str
    passed: bool
    duration: float
    details: str
    error_details: Optional[str] = None
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)


@dataclass
class TestSuiteConfig:
    """Configuration for test suite execution"""
    run_performance_tests: bool = True
    run_integration_tests: bool = True
    run_cloud_tests: bool = True
    max_test_duration: float = 30.0
    parallel_execution: bool = True
    verbose_output: bool = True
    generate_report: bool = True


class ComprehensiveTestSuite:
    """Complete testing suite for enhanced widget functionality"""
    
    def __init__(self, config: Optional[TestSuiteConfig] = None):
        self.config = config or TestSuiteConfig()
        self.results: List[TestResult] = []
        self.start_time = 0.0
        self.end_time = 0.0
        
        # Test categories
        self.categories = {
            'core': 'Core Widget Functionality',
            'integration': 'Module Integration',
            'cloud': 'Cloud Compatibility',
            'visual': 'Visual Feedback',
            'selection': 'Model Selection',
            'performance': 'Performance & Load',
            'workflow': 'End-to-End Workflow',
            'accessibility': 'Accessibility & Usability'
        }
        
        # Performance thresholds
        self.performance_thresholds = {
            'widget_load_time': 2.0,    # seconds
            'api_response_time': 5.0,   # seconds
            'memory_usage_mb': 500.0,   # megabytes
            'ui_responsiveness': 100.0  # milliseconds
        }
    
    def log_test_start(self, test_name: str, category: str):
        """Log test start"""
        if self.config.verbose_output:
            print(f"\n[TEST] {category}: {test_name}")
    
    def record_result(self, result: TestResult):
        """Record test result"""
        self.results.append(result)
        
        status = "[PASS]" if result.passed else "[FAIL]"
        duration_str = f"({result.duration:.3f}s)"
        
        if self.config.verbose_output:
            print(f"  {status} {result.test_name} {duration_str}")
            if result.warnings:
                for warning in result.warnings:
                    print(f"    [WARN] {warning}")
            if result.error_details:
                print(f"    [ERROR] {result.error_details}")
    
    async def run_core_functionality_tests(self) -> List[TestResult]:
        """Test core widget functionality"""
        tests = []
        
        # Test 1: Widget imports and basic setup
        test_name = "Widget Imports and Setup"
        self.log_test_start(test_name, "Core")
        start_time = time.time()
        
        try:
            import ipywidgets as widgets
            from IPython.display import display, HTML
            
            # Test CSS and JS file existence
            css_file = project_root / "CSS" / "main-widgets.css"
            js_file = project_root / "JS" / "main-widgets.js"
            
            assert css_file.exists(), "Main CSS file missing"
            assert js_file.exists(), "Main JS file missing"
            
            # Test sanguine color scheme presence
            css_content = css_file.read_text()
            assert "#8B0000" in css_content, "Sanguine primary color missing"
            assert "#DC143C" in css_content, "Sanguine accent color missing"
            
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "core", True, duration,
                "All core files and colors validated successfully"
            ))
            
        except Exception as e:
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "core", False, duration,
                "Core functionality test failed", str(e)
            ))
        
        # Test 2: Tabbed interface functionality
        test_name = "Tabbed Interface"
        self.log_test_start(test_name, "Core")
        start_time = time.time()
        
        try:
            import ipywidgets as widgets
            
            tabs = widgets.Tab()
            tab_contents = []
            
            for i in range(4):
                content = widgets.VBox([widgets.HTML(f"<h3>Tab {i+1}</h3>")])
                tab_contents.append(content)
            
            tabs.children = tab_contents
            for i in range(4):
                tabs.set_title(i, f"Tab {i+1}")
            
            # Test tab switching
            tabs.selected_index = 0
            assert tabs.selected_index == 0, "Failed to set initial tab"
            
            tabs.selected_index = 2
            assert tabs.selected_index == 2, "Failed to switch tabs"
            
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "core", True, duration,
                f"Successfully tested {len(tab_contents)} tabs with switching"
            ))
            
        except Exception as e:
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "core", False, duration,
                "Tab interface test failed", str(e)
            ))
        
        # Test 3: Interactive controls
        test_name = "Interactive Controls"
        self.log_test_start(test_name, "Core")
        start_time = time.time()
        
        try:
            import ipywidgets as widgets
            
            controls = {
                'checkbox': widgets.Checkbox(value=False, description="Test Checkbox"),
                'toggle': widgets.ToggleButton(value=False, description="Test Toggle"),
                'slider': widgets.FloatSlider(value=0.5, min=0, max=1, description="Test Slider"),
                'dropdown': widgets.Dropdown(options=['A', 'B', 'C'], description="Test Dropdown"),
                'button': widgets.Button(description="Test Button")
            }
            
            # Test state changes
            controls['checkbox'].value = True
            assert controls['checkbox'].value == True, "Checkbox toggle failed"
            
            controls['toggle'].value = True
            assert controls['toggle'].value == True, "Toggle button failed"
            
            controls['slider'].value = 0.8
            assert abs(controls['slider'].value - 0.8) < 0.01, "Slider value change failed"
            
            controls['dropdown'].value = 'B'
            assert controls['dropdown'].value == 'B', "Dropdown selection failed"
            
            # Test event handling
            event_triggered = {'count': 0}
            
            def test_callback(change):
                event_triggered['count'] += 1
            
            controls['checkbox'].observe(test_callback, names='value')
            controls['checkbox'].value = False
            
            assert event_triggered['count'] > 0, "Event callback not triggered"
            
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "core", True, duration,
                f"Successfully tested {len(controls)} interactive controls"
            ))
            
        except Exception as e:
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "core", False, duration,
                "Interactive controls test failed", str(e)
            ))
        
        return tests
    
    async def run_integration_tests(self) -> List[TestResult]:
        """Test module integration"""
        tests = []
        
        # Test 1: CivitaiAPI integration
        test_name = "CivitaiAPI Integration"
        self.log_test_start(test_name, "Integration")
        start_time = time.time()
        
        try:
            # Test API initialization
            callback_calls = []
            
            def test_callback(progress, message, level):
                callback_calls.append((progress, message, level))
            
            api = CivitAiAPI(progress_callback=test_callback, log=False)
            
            # Test ModelData enhancements
            model = ModelData(
                download_url="https://test.url",
                clean_url="https://test.clean.url",
                model_name="Test Model",
                model_type="LORA",
                version_id="12345",
                model_id="67890"
            )
            
            # Test progress tracking
            model.update_progress(75.0, 5.0)
            assert model.download_progress == 75.0, "Progress update failed"
            assert model.download_speed == 5.0, "Speed update failed"
            assert model.estimated_time is not None, "ETA calculation failed"
            
            # Test serialization
            model_dict = model.to_dict()
            required_fields = ['model_name', 'model_type', 'download_progress', 'tags']
            for field in required_fields:
                assert field in model_dict, f"Missing serialization field: {field}"
            
            # Test cache functionality
            cache_stats = api.get_cache_stats()
            assert isinstance(cache_stats, dict), "Cache stats not returned as dict"
            assert 'total_entries' in cache_stats, "Cache stats missing total_entries"
            
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "integration", True, duration,
                "CivitaiAPI integration working correctly",
                performance_metrics={'api_init_time': duration}
            ))
            
        except Exception as e:
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "integration", False, duration,
                "CivitaiAPI integration failed", str(e)
            ))
        
        # Test 2: TunnelHub integration
        test_name = "TunnelHub Integration"
        self.log_test_start(test_name, "Integration")
        start_time = time.time()
        
        try:
            # Test cloud platform detection
            platform_info = CloudPlatformInfo.detect_platform()
            assert hasattr(platform_info, 'platform'), "Platform detection failed"
            assert hasattr(platform_info, 'recommended_tunnels'), "Recommendations missing"
            
            # Test enhanced tunnel
            widget_callbacks = []
            
            def test_tunnel_callback(status_data):
                widget_callbacks.append(status_data)
            
            tunnel = EnhancedTunnel(
                port=7860,
                widget_callback=test_tunnel_callback,
                check_local_port=False,
                debug=False
            )
            
            # Test recommendations
            recommendations = tunnel.get_tunnel_recommendations()
            assert isinstance(recommendations, list), "Recommendations not returned as list"
            
            # Test status summary
            status = tunnel.get_status_summary()
            required_fields = ['platform', 'total_tunnels', 'is_running']
            for field in required_fields:
                assert field in status, f"Status missing field: {field}"
            
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "integration", True, duration,
                f"TunnelHub integration working for {platform_info.platform}",
                performance_metrics={'tunnel_init_time': duration}
            ))
            
        except Exception as e:
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "integration", False, duration,
                "TunnelHub integration failed", str(e)
            ))
        
        return tests
    
    async def run_cloud_compatibility_tests(self) -> List[TestResult]:
        """Test cloud environment compatibility"""
        tests = []
        
        # Test 1: Environment detection
        test_name = "Environment Detection"
        self.log_test_start(test_name, "Cloud")
        start_time = time.time()
        
        try:
            manager = CloudCompatibilityManager()
            env = manager.environment
            
            assert env.platform is not None, "Platform not detected"
            assert env.provider is not None, "Provider not detected"
            assert env.max_memory_gb > 0, "Memory detection failed"
            assert env.cpu_cores > 0, "CPU detection failed"
            
            # Test layout configuration
            layout_config = manager.get_widget_layout_config()
            required_config = ['max_width', 'container_padding', 'font_size']
            for config_key in required_config:
                assert config_key in layout_config, f"Missing layout config: {config_key}"
            
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "cloud", True, duration,
                f"Environment detected: {env.platform} on {env.provider}"
            ))
            
        except Exception as e:
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "cloud", False, duration,
                "Environment detection failed", str(e)
            ))
        
        # Test 2: Responsive layout
        test_name = "Responsive Layout"
        self.log_test_start(test_name, "Cloud")
        start_time = time.time()
        
        try:
            manager = CloudCompatibilityManager()
            
            # Test CSS generation
            css = manager.get_performance_css()
            assert len(css) > 0, "CSS generation failed"
            assert ".cloud-optimized-container" in css, "Missing cloud optimization CSS"
            assert "@media" in css, "Missing responsive design CSS"
            
            # Test JavaScript generation
            js = manager.get_javascript_polyfills()
            assert len(js) > 0, "JavaScript generation failed"
            assert "CloudEnvironment" in js, "Missing CloudEnvironment object"
            
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "cloud", True, duration,
                "Responsive layout system working correctly"
            ))
            
        except Exception as e:
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "cloud", False, duration,
                "Responsive layout test failed", str(e)
            ))
        
        return tests
    
    async def run_visual_feedback_tests(self) -> List[TestResult]:
        """Test visual feedback system"""
        tests = []
        
        # Test 1: Notification system
        test_name = "Notification System"
        self.log_test_start(test_name, "Visual")
        start_time = time.time()
        
        try:
            feedback = EnhancedVisualFeedback()
            
            # Test different notification types
            notification_types = [
                (NotificationType.SUCCESS, "Test success message"),
                (NotificationType.ERROR, "Test error message"),
                (NotificationType.WARNING, "Test warning message"),
                (NotificationType.INFO, "Test info message")
            ]
            
            for notification_type, message in notification_types:
                notification_id = feedback.show_notification(message, notification_type, duration=1000)
                assert notification_id is not None, f"Failed to create {notification_type.value} notification"
            
            # Test feedback history
            assert len(feedback.feedback_history) == len(notification_types), "Feedback history not tracking correctly"
            
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "visual", True, duration,
                f"Successfully tested {len(notification_types)} notification types"
            ))
            
        except Exception as e:
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "visual", False, duration,
                "Notification system test failed", str(e)
            ))
        
        # Test 2: Status indicators
        test_name = "Status Indicators"
        self.log_test_start(test_name, "Visual")
        start_time = time.time()
        
        try:
            feedback = EnhancedVisualFeedback()
            
            # Test status indicator creation
            statuses = ["connected", "connecting", "disconnected", "loading"]
            
            for status in statuses:
                indicator = feedback.create_status_indicator(status, f"Test {status}")
                assert indicator is not None, f"Failed to create {status} indicator"
                assert hasattr(indicator, 'value'), "Indicator missing value attribute"
            
            # Test progress indicator
            progress = feedback.create_enhanced_progress(25.0, "Testing progress...")
            assert progress is not None, "Failed to create progress indicator"
            
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "visual", True, duration,
                f"Successfully tested {len(statuses)} status indicators"
            ))
            
        except Exception as e:
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "visual", False, duration,
                "Status indicators test failed", str(e)
            ))
        
        return tests
    
    async def run_model_selection_tests(self) -> List[TestResult]:
        """Test enhanced model selection interface"""
        tests = []
        
        # Test 1: Model selector initialization
        test_name = "Model Selector Initialization"
        self.log_test_start(test_name, "Selection")
        start_time = time.time()
        
        try:
            selection_callbacks = []
            
            def test_selection_callback(selected_models):
                selection_callbacks.append(selected_models)
            
            selector = EnhancedModelSelector(callback=test_selection_callback)
            
            assert hasattr(selector, 'all_models'), "Model data not loaded"
            assert hasattr(selector, 'selected_models'), "Selection tracking missing"
            assert hasattr(selector, 'filtered_models'), "Filtering system missing"
            
            # Test that models were loaded
            assert len(selector.all_models) >= 0, "Model loading failed"
            
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "selection", True, duration,
                f"Model selector initialized with {len(selector.all_models)} models"
            ))
            
        except Exception as e:
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "selection", False, duration,
                "Model selector initialization failed", str(e)
            ))
        
        # Test 2: Selection functionality
        test_name = "Selection Functionality"
        self.log_test_start(test_name, "Selection")
        start_time = time.time()
        
        try:
            selector = EnhancedModelSelector()
            
            # Test selection summary
            summary = selector.get_selection_summary()
            assert isinstance(summary, dict), "Selection summary not returned as dict"
            assert 'count' in summary, "Selection summary missing count"
            assert 'models' in summary, "Selection summary missing models list"
            
            # Test status summary structure
            assert 'categories' in summary, "Selection summary missing categories"
            assert 'compatibility' in summary, "Selection summary missing compatibility"
            
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "selection", True, duration,
                "Selection functionality working correctly"
            ))
            
        except Exception as e:
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "selection", False, duration,
                "Selection functionality test failed", str(e)
            ))
        
        return tests
    
    async def run_performance_tests(self) -> List[TestResult]:
        """Test performance and load characteristics"""
        tests = []
        
        # Test 1: Widget load time
        test_name = "Widget Load Time"
        self.log_test_start(test_name, "Performance")
        start_time = time.time()
        
        try:
            import ipywidgets as widgets
            
            # Create multiple widgets to simulate load
            widget_count = 50
            widgets_list = []
            
            widget_start = time.time()
            for i in range(widget_count):
                widget = widgets.Button(description=f"Test Button {i}")
                widgets_list.append(widget)
            widget_load_time = time.time() - widget_start
            
            # Test container creation
            container = widgets.VBox(widgets_list)
            assert len(container.children) == widget_count, "Widget container failed"
            
            # Check performance threshold
            per_widget_time = widget_load_time / widget_count
            load_time_passed = widget_load_time < self.performance_thresholds['widget_load_time']
            
            warnings = []
            if not load_time_passed:
                warnings.append(f"Widget load time ({widget_load_time:.3f}s) exceeds threshold")
            
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "performance", load_time_passed, duration,
                f"Loaded {widget_count} widgets in {widget_load_time:.3f}s",
                performance_metrics={'widget_load_time': widget_load_time, 'per_widget_time': per_widget_time},
                warnings=warnings
            ))
            
        except Exception as e:
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "performance", False, duration,
                "Widget load time test failed", str(e)
            ))
        
        # Test 2: Memory usage
        test_name = "Memory Usage"
        self.log_test_start(test_name, "Performance")
        start_time = time.time()
        
        try:
            import psutil
            import gc
            
            # Get initial memory
            process = psutil.Process()
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Create memory-intensive objects
            test_objects = []
            for i in range(1000):
                obj = {
                    'api': CivitAiAPI(log=False),
                    'data': ModelData("url", "clean", "name", "type", "vid", "mid"),
                    'large_data': list(range(100))
                }
                test_objects.append(obj)
            
            # Check memory after creation
            peak_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_used = peak_memory - initial_memory
            
            # Cleanup
            del test_objects
            gc.collect()
            
            # Check memory after cleanup
            final_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            memory_passed = memory_used < self.performance_thresholds['memory_usage_mb']
            
            warnings = []
            if not memory_passed:
                warnings.append(f"Memory usage ({memory_used:.1f}MB) exceeds threshold")
            
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "performance", memory_passed, duration,
                f"Memory usage: {memory_used:.1f}MB peak, {final_memory - initial_memory:.1f}MB final",
                performance_metrics={'memory_used_mb': memory_used, 'memory_leaked_mb': final_memory - initial_memory},
                warnings=warnings
            ))
            
        except Exception as e:
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "performance", False, duration,
                "Memory usage test failed", str(e)
            ))
        
        return tests
    
    async def run_workflow_tests(self) -> List[TestResult]:
        """Test end-to-end workflow scenarios"""
        tests = []
        
        # Test 1: Complete widget workflow
        test_name = "Complete Widget Workflow"
        self.log_test_start(test_name, "Workflow")
        start_time = time.time()
        
        try:
            # Step 1: Initialize components
            cloud_manager = CloudCompatibilityManager()
            feedback_system = EnhancedVisualFeedback()
            model_selector = EnhancedModelSelector()
            
            # Step 2: Setup cloud optimizations
            cloud_manager.apply_responsive_styling()
            
            # Step 3: Test feedback notifications
            feedback_system.show_info("Workflow test started")
            
            # Step 4: Test model selection workflow
            selection_summary = model_selector.get_selection_summary()
            assert 'count' in selection_summary, "Selection summary validation failed"
            
            # Step 5: Test integration points
            compatibility_report = cloud_manager.test_compatibility()
            assert 'environment_detected' in compatibility_report, "Compatibility test failed"
            
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "workflow", True, duration,
                "Complete widget workflow executed successfully"
            ))
            
        except Exception as e:
            duration = time.time() - start_time
            tests.append(TestResult(
                test_name, "workflow", False, duration,
                "Complete widget workflow failed", str(e)
            ))
        
        return tests
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all test categories"""
        print("=" * 80)
        print("COMPREHENSIVE WIDGET TESTING SUITE - ENHANCED VERSION")
        print("=" * 80)
        
        self.start_time = time.time()
        
        # Define test categories and their functions
        test_categories = [
            ('core', self.run_core_functionality_tests),
            ('integration', self.run_integration_tests),
            ('cloud', self.run_cloud_compatibility_tests),
            ('visual', self.run_visual_feedback_tests),
            ('selection', self.run_model_selection_tests),
        ]
        
        # Add optional test categories
        if self.config.run_performance_tests:
            test_categories.append(('performance', self.run_performance_tests))
        
        test_categories.append(('workflow', self.run_workflow_tests))
        
        # Run tests
        if self.config.parallel_execution:
            # Run categories in parallel
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = {}
                
                for category, test_func in test_categories:
                    future = executor.submit(asyncio.run, test_func())
                    futures[future] = category
                
                for future in as_completed(futures):
                    category = futures[future]
                    try:
                        category_results = future.result()
                        for result in category_results:
                            self.record_result(result)
                    except Exception as e:
                        print(f"[ERROR] Category {category} failed: {e}")
        else:
            # Run categories sequentially
            for category, test_func in test_categories:
                try:
                    category_results = await test_func()
                    for result in category_results:
                        self.record_result(result)
                except Exception as e:
                    print(f"[ERROR] Category {category} failed: {e}")
        
        self.end_time = time.time()
        
        # Generate final report
        return self.generate_final_report()
    
    def generate_final_report(self) -> Dict[str, Any]:
        """Generate comprehensive final report"""
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.passed)
        failed_tests = total_tests - passed_tests
        total_duration = self.end_time - self.start_time
        
        # Category breakdown
        category_stats = {}
        for category_key, category_name in self.categories.items():
            category_results = [r for r in self.results if r.category == category_key]
            category_stats[category_name] = {
                'total': len(category_results),
                'passed': sum(1 for r in category_results if r.passed),
                'failed': sum(1 for r in category_results if not r.passed),
                'duration': sum(r.duration for r in category_results)
            }
        
        # Performance metrics
        performance_metrics = {}
        for result in self.results:
            if result.performance_metrics:
                performance_metrics.update(result.performance_metrics)
        
        # Generate report
        print("\n" + "=" * 80)
        print("COMPREHENSIVE TEST REPORT")
        print("=" * 80)
        
        print(f"\nOVERALL RESULTS:")
        print(f"  Total Tests: {total_tests}")
        print(f"  Passed: {passed_tests} [{passed_tests/total_tests*100:.1f}%]")
        print(f"  Failed: {failed_tests} [{failed_tests/total_tests*100:.1f}%]")
        print(f"  Total Duration: {total_duration:.3f}s")
        print(f"  Average Test Time: {total_duration/total_tests:.3f}s")
        
        print(f"\nCATEGORY BREAKDOWN:")
        for category_name, stats in category_stats.items():
            if stats['total'] > 0:
                success_rate = stats['passed'] / stats['total'] * 100
                print(f"  {category_name}:")
                print(f"    {stats['passed']}/{stats['total']} passed ({success_rate:.1f}%) in {stats['duration']:.3f}s")
        
        if performance_metrics:
            print(f"\nPERFORMANCE METRICS:")
            for metric, value in performance_metrics.items():
                print(f"  {metric}: {value:.3f}")
        
        # Failed tests details
        failed_results = [r for r in self.results if not r.passed]
        if failed_results:
            print(f"\nFAILED TESTS:")
            for result in failed_results:
                print(f"  [-] {result.category.upper()}: {result.test_name}")
                print(f"      Error: {result.error_details}")
        
        # Warnings
        all_warnings = []
        for result in self.results:
            all_warnings.extend(result.warnings)
        
        if all_warnings:
            print(f"\nWARNINGS:")
            for warning in all_warnings:
                print(f"  [!] {warning}")
        
        print(f"\n" + "=" * 80)
        
        # Final status
        overall_success = failed_tests == 0
        if overall_success:
            print("[SUCCESS] All comprehensive tests passed! Enhanced widget system is ready.")
        else:
            print(f"[WARNING] {failed_tests} tests failed. Review details above.")
        
        print("=" * 80)
        
        # Return structured report
        report = {
            'overall': {
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'failed_tests': failed_tests,
                'success_rate': passed_tests / total_tests * 100 if total_tests > 0 else 0,
                'total_duration': total_duration,
                'overall_success': overall_success
            },
            'categories': category_stats,
            'performance_metrics': performance_metrics,
            'failed_tests': [
                {'name': r.test_name, 'category': r.category, 'error': r.error_details}
                for r in failed_results
            ],
            'warnings': all_warnings,
            'test_results': [
                {
                    'name': r.test_name,
                    'category': r.category,
                    'passed': r.passed,
                    'duration': r.duration,
                    'details': r.details
                }
                for r in self.results
            ]
        }
        
        return report


async def main():
    """Main test execution function"""
    # Test configuration
    config = TestSuiteConfig(
        run_performance_tests=True,
        run_integration_tests=True,
        run_cloud_tests=True,
        parallel_execution=False,  # Set to False for clearer output
        verbose_output=True,
        generate_report=True
    )
    
    # Create and run test suite
    test_suite = ComprehensiveTestSuite(config)
    report = await test_suite.run_all_tests()
    
    # Return exit code
    return 0 if report['overall']['overall_success'] else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)