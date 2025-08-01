#!/usr/bin/env python3
"""
Health check script for the mock server.
Can be used for monitoring and deployment health checks.
"""

import requests
import sys
import json
from typing import Dict, Any

def check_health(base_url: str = "http://localhost:3001") -> Dict[str, Any]:
    """
    Perform health check on the mock server.
    
    Args:
        base_url: Base URL of the server
        
    Returns:
        Dictionary with health check results
    """
    results = {
        "status": "healthy",
        "checks": {},
        "errors": []
    }
    
    try:
        # Test 1: Check if server is responding
        response = requests.get(f"{base_url}/users", timeout=5)
        if response.status_code == 200:
            results["checks"]["server_responding"] = True
        else:
            results["checks"]["server_responding"] = False
            results["errors"].append(f"Server returned status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        results["checks"]["server_responding"] = False
        results["errors"].append(f"Connection error: {str(e)}")
    
    try:
        # Test 2: Check API functionality
        response = requests.get(f"{base_url}/user/data?username=alice", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("username") == "alice" and data.get("plan") == "normal":
                results["checks"]["api_functional"] = True
            else:
                results["checks"]["api_functional"] = False
                results["errors"].append("API returned unexpected data")
        else:
            results["checks"]["api_functional"] = False
            results["errors"].append(f"API test failed with status {response.status_code}")
            
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        results["checks"]["api_functional"] = False
        results["errors"].append(f"API test error: {str(e)}")
    
    # Set overall status
    if not all(results["checks"].values()):
        results["status"] = "unhealthy"
    
    return results

def main():
    """Main function for command line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Health check for mock server")
    parser.add_argument("--url", default="http://localhost:3001", 
                       help="Base URL of the server (default: http://localhost:3001)")
    parser.add_argument("--json", action="store_true", 
                       help="Output results as JSON")
    
    args = parser.parse_args()
    
    results = check_health(args.url)
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"Health Status: {results['status'].upper()}")
        print("\nChecks:")
        for check, status in results["checks"].items():
            status_symbol = "✓" if status else "✗"
            print(f"  {status_symbol} {check}")
        
        if results["errors"]:
            print("\nErrors:")
            for error in results["errors"]:
                print(f"  - {error}")
    
    # Exit with appropriate code
    sys.exit(0 if results["status"] == "healthy" else 1)

if __name__ == "__main__":
    main()
