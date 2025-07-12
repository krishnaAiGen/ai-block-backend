#!/usr/bin/env python3
"""
Test script for AI Block Backend API
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    print("-" * 50)

def test_stats():
    """Test stats endpoint"""
    print("📊 Testing stats endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/stats")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    print("-" * 50)

def test_search_chunks():
    """Test search chunks endpoint"""
    print("🔍 Testing search chunks endpoint...")
    try:
        payload = {
            "query": "How do I find recent transfers?",
            "max_chunks": 3
        }
        response = requests.post(f"{BASE_URL}/search-chunks", json=payload)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Found {len(data.get('chunks', []))} chunks")
        for chunk in data.get('chunks', [])[:2]:  # Show first 2
            print(f"  - {chunk['id']}: {chunk['content'][:100]}...")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    print("-" * 50)

def test_generate_query():
    """Test GraphQL query generation"""
    print("🔧 Testing GraphQL query generation...")
    try:
        payload = {
            "query": "Show me the last 5 transfers on Kusama",
            "max_chunks": 3
        }
        response = requests.post(f"{BASE_URL}/generate-query", json=payload)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Generated Query:\n{data.get('graphql_query', 'No query generated')}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    print("-" * 50)

def test_answer():
    """Test main answer endpoint"""
    print("🤖 Testing main answer endpoint...")
    try:
        payload = {
            "query": "What are the recent transfers on Kusama?",
            "max_chunks": 5
        }
        response = requests.post(f"{BASE_URL}/answer", json=payload)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Answer: {data.get('answer', 'No answer provided')[:200]}...")
            print(f"GraphQL Query: {data.get('graphql_query', 'No query')[:100]}...")
            print(f"Raw Data Keys: {list(data.get('raw_data', {}).keys())}")
            print(f"Relevant Chunks: {len(data.get('relevant_chunks', []))}")
        else:
            print(f"Error response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    print("-" * 50)

def main():
    """Run all tests"""
    print("🚀 AI Block Backend API Test Suite")
    print("=" * 50)
    
    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    test_health()
    test_stats()
    test_search_chunks()
    test_generate_query()
    test_answer()
    
    print("✅ Test suite completed!")

if __name__ == "__main__":
    main() 