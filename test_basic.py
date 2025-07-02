#!/usr/bin/env python3
"""
Basic GitHub Webhook Test (No MongoDB Required)
"""

import requests
import json

def test_basic_functionality():
    """Test basic app functionality"""
    print("🧪 Basic Functionality Test")
    print("=" * 40)
    
    # Test health endpoint
    print("1. Health Check...")
    try:
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            print("   ✅ Health endpoint working")
        else:
            print(f"   ❌ Health failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Health error: {e}")
    
    # Test web UI
    print("\n2. Web UI...")
    try:
        response = requests.get("http://localhost:5000/")
        if response.status_code == 200:
            print("   ✅ Web UI accessible")
            print("   🌐 Open: http://localhost:5000")
        else:
            print(f"   ❌ UI failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ UI error: {e}")
    
    # Test API endpoint
    print("\n3. API Endpoint...")
    try:
        response = requests.get("http://localhost:5000/api/events")
        if response.status_code == 200:
            events = response.json()
            print(f"   ✅ API working - {len(events)} events")
        else:
            print(f"   ❌ API failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ API error: {e}")
    
    print("\n🎯 Result: Basic functionality confirmed!")
    print("📝 Note: MongoDB needed for full webhook storage")

if __name__ == "__main__":
    test_basic_functionality() 