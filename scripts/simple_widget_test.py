#!/usr/bin/env python3
"""
Simple Widget Functionality Test - ASCII Only Version
Quick validation of enhanced widget components
"""

import sys
import os
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_basic_imports():
    """Test basic module imports"""
    print("[TEST] Testing module imports...")
    
    try:
        from modules.CivitaiAPI import CivitAiAPI, ModelData
        print("  [+] CivitaiAPI imported successfully")
        
        from modules.TunnelHub import EnhancedTunnel, CloudPlatformInfo
        print("  [+] TunnelHub imported successfully")
        
        # Test basic functionality
        api = CivitAiAPI(log=False)
        print("  [+] CivitaiAPI instance created")
        
        platform = CloudPlatformInfo.detect_platform()
        print(f"  [+] Cloud platform detected: {platform.platform}")
        
        tunnel = EnhancedTunnel(port=7860, check_local_port=False, debug=False)
        print("  [+] Enhanced tunnel instance created")
        
        return True
        
    except Exception as e:
        print(f"  [-] Import test failed: {e}")
        return False

def test_model_data_enhancements():
    """Test enhanced ModelData functionality"""
    print("[TEST] Testing ModelData enhancements...")
    
    try:
        from modules.CivitaiAPI import ModelData
        
        # Create test model
        model = ModelData(
            download_url="https://test.url",
            clean_url="https://test.clean.url", 
            model_name="Test Model",
            model_type="LORA",
            version_id="12345",
            model_id="67890"
        )
        
        # Test progress tracking
        model.update_progress(50.0, 2.5)
        assert model.download_progress == 50.0, "Progress update failed"
        assert model.download_speed == 2.5, "Speed update failed"
        print("  [+] Progress tracking works")
        
        # Test serialization
        data_dict = model.to_dict()
        assert "model_name" in data_dict, "Serialization missing model_name"
        assert "download_progress" in data_dict, "Serialization missing progress"
        print("  [+] Model serialization works")
        
        return True
        
    except Exception as e:
        print(f"  [-] ModelData test failed: {e}")
        return False

def test_api_enhancements():
    """Test CivitaiAPI enhancements"""
    print("[TEST] Testing CivitaiAPI enhancements...")
    
    try:
        from modules.CivitaiAPI import CivitAiAPI
        
        # Test with widget callback
        callback_calls = []
        
        def test_callback(progress, message, level):
            callback_calls.append((progress, message, level))
        
        api = CivitAiAPI(progress_callback=test_callback, log=False)
        print("  [+] API with callback created")
        
        # Test cache functionality
        cache_stats = api.get_cache_stats()
        assert isinstance(cache_stats, dict), "Cache stats should be dict"
        assert "total_entries" in cache_stats, "Cache stats missing total_entries"
        print("  [+] Cache system works")
        
        return True
        
    except Exception as e:
        print(f"  [-] API enhancement test failed: {e}")
        return False

def test_tunnel_enhancements():
    """Test TunnelHub enhancements"""
    print("[TEST] Testing TunnelHub enhancements...")
    
    try:
        from modules.TunnelHub import EnhancedTunnel, CloudPlatformInfo
        
        # Test platform detection
        platform = CloudPlatformInfo.detect_platform()
        assert hasattr(platform, 'platform'), "Platform missing platform attribute"
        assert hasattr(platform, 'recommended_tunnels'), "Platform missing recommendations"
        print(f"  [+] Platform detection works: {platform.platform}")
        
        # Test enhanced tunnel
        widget_calls = []
        
        def test_widget_callback(status_data):
            widget_calls.append(status_data)
        
        tunnel = EnhancedTunnel(
            port=7860,
            widget_callback=test_widget_callback,
            check_local_port=False,
            debug=False
        )
        
        # Test recommendations
        recommendations = tunnel.get_tunnel_recommendations()
        assert isinstance(recommendations, list), "Recommendations should be list"
        print(f"  [+] Tunnel recommendations: {len(recommendations)} options")
        
        # Test status summary
        status = tunnel.get_status_summary()
        assert "platform" in status, "Status missing platform"
        assert "total_tunnels" in status, "Status missing total_tunnels"
        print("  [+] Status summary works")
        
        return True
        
    except Exception as e:
        print(f"  [-] Tunnel enhancement test failed: {e}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("[TEST] Testing file structure...")
    
    required_files = [
        "CSS/main-widgets.css",
        "JS/main-widgets.js",
        "scripts/_models-data.py",
        "scripts/_xl-models-data.py",
        "modules/CivitaiAPI.py",
        "modules/TunnelHub.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = project_root / file_path
        if not full_path.exists():
            missing_files.append(file_path)
        else:
            print(f"  [+] Found: {file_path}")
    
    if missing_files:
        print(f"  [-] Missing files: {missing_files}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("ENHANCED WIDGET FUNCTIONALITY - QUICK TEST")
    print("=" * 60)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Basic Imports", test_basic_imports),
        ("ModelData Enhancements", test_model_data_enhancements),
        ("API Enhancements", test_api_enhancements),
        ("Tunnel Enhancements", test_tunnel_enhancements),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print()
        start_time = time.time()
        
        try:
            success = test_func()
            duration = time.time() - start_time
            results.append((test_name, success, duration))
            
            status = "[PASS]" if success else "[FAIL]"
            print(f"  {status} {test_name} ({duration:.3f}s)")
            
        except Exception as e:
            duration = time.time() - start_time
            results.append((test_name, False, duration))
            print(f"  [FAIL] {test_name} ({duration:.3f}s) - {e}")
    
    # Summary
    print()
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success, _ in results if success)
    total_duration = sum(duration for _, _, duration in results)
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
    print(f"Total Duration: {total_duration:.3f}s")
    
    if passed_tests == total_tests:
        print("\n[SUCCESS] All tests passed! Widget enhancements are working correctly.")
        return 0
    else:
        print(f"\n[WARNING] {total_tests - passed_tests} tests failed. Review output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())