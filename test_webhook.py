#!/usr/bin/env python3
"""
Test script for GitHub Webhook functionality
This script simulates GitHub webhook events for local testing
"""

import requests
import json
import hashlib
import hmac
from datetime import datetime

# Configuration
WEBHOOK_URL = "http://localhost:5000/webhook"
WEBHOOK_SECRET = "test-secret"  # Change this to match your .env file

def create_signature(payload, secret):
    """Create HMAC signature for GitHub webhook"""
    if secret:
        signature = "sha256=" + hmac.new(
            secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    return None

def test_push_event():
    """Test push event"""
    payload = {
        "ref": "refs/heads/main",
        "pusher": {
            "name": "TestUser"
        },
        "repository": {
            "name": "test-repo"
        },
        "commits": [
            {
                "id": "abc123",
                "message": "Test commit"
            }
        ]
    }
    
    payload_json = json.dumps(payload)
    signature = create_signature(payload_json, WEBHOOK_SECRET)
    
    headers = {
        "X-GitHub-Event": "push",
        "Content-Type": "application/json"
    }
    
    if signature:
        headers["X-Hub-Signature-256"] = signature
    
    print("Testing PUSH event...")
    response = requests.post(WEBHOOK_URL, data=payload_json, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    print("-" * 50)

def test_pull_request_event():
    """Test pull request event"""
    payload = {
        "action": "opened",
        "pull_request": {
            "number": 1,
            "user": {
                "login": "TestUser"
            },
            "head": {
                "ref": "feature-branch"
            },
            "base": {
                "ref": "main"
            }
        },
        "repository": {
            "name": "test-repo"
        }
    }
    
    payload_json = json.dumps(payload)
    signature = create_signature(payload_json, WEBHOOK_SECRET)
    
    headers = {
        "X-GitHub-Event": "pull_request",
        "Content-Type": "application/json"
    }
    
    if signature:
        headers["X-Hub-Signature-256"] = signature
    
    print("Testing PULL REQUEST event...")
    response = requests.post(WEBHOOK_URL, data=payload_json, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    print("-" * 50)

def test_merge_event():
    """Test merge event"""
    payload = {
        "action": "closed",
        "pull_request": {
            "number": 1,
            "merged": True,
            "merged_by": {
                "login": "TestUser"
            },
            "head": {
                "ref": "feature-branch"
            },
            "base": {
                "ref": "main"
            }
        },
        "repository": {
            "name": "test-repo"
        }
    }
    
    payload_json = json.dumps(payload)
    signature = create_signature(payload_json, WEBHOOK_SECRET)
    
    headers = {
        "X-GitHub-Event": "pull_request",
        "Content-Type": "application/json"
    }
    
    if signature:
        headers["X-Hub-Signature-256"] = signature
    
    print("Testing MERGE event...")
    response = requests.post(WEBHOOK_URL, data=payload_json, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    print("-" * 50)

def test_api_events():
    """Test the events API endpoint"""
    print("Testing API events endpoint...")
    try:
        response = requests.get("http://localhost:5000/api/events")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            events = response.json()
            print(f"Found {len(events)} events:")
            for event in events[:3]:  # Show first 3 events
                print(f"  - {event.get('type', 'unknown')}: {event.get('message', 'no message')}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 50)

def test_health_check():
    """Test health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get("http://localhost:5000/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 50)

if __name__ == "__main__":
    print("GitHub Webhook Test Suite")
    print("=" * 50)
    print(f"Target URL: {WEBHOOK_URL}")
    print(f"Using secret: {'Yes' if WEBHOOK_SECRET else 'No'}")
    print("=" * 50)
    
    # Test health check first
    test_health_check()
    
    # Test webhook events
    test_push_event()
    test_pull_request_event()
    test_merge_event()
    
    # Test API endpoint
    test_api_events()
    
    print("Test suite completed!")
    print("\nNext steps:")
    print("1. Check the web UI at http://localhost:5000")
    print("2. Verify events are stored in MongoDB")
    print("3. Test with real GitHub webhooks") 