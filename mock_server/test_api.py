#!/usr/bin/env python3
"""
API test script for the mock server.
Tests all endpoints and validates responses.
"""

import requests
import json
import sys
from typing import Dict, Any, List

class MockServerTester:
    """Test class for mock server API endpoints."""
    
    def __init__(self, base_url: str = "http://localhost:3001"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results: List[Dict[str, Any]] = []
    
    def log_test(self, test_name: str, success: bool, message: str = ""):
        """Log test result."""
        result = {
            "test": test_name,
            "success": success,
            "message": message
        }
        self.test_results.append(result)
        status = "PASS" if success else "FAIL"
        print(f"[{status}] {test_name}: {message}")
    
    def test_users_endpoint(self) -> bool:
        """Test the /users endpoint."""
        try:
            response = self.session.get(f"{self.base_url}/users")
            if response.status_code != 200:
                self.log_test("Users Endpoint", False, f"Status code {response.status_code}")
                return False
            
            data = response.json()
            expected_users = {"alice": "normal", "bob": "premium", "carol": "ultra"}
            
            if data == expected_users:
                self.log_test("Users Endpoint", True, "Returned correct user mapping")
                return True
            else:
                self.log_test("Users Endpoint", False, f"Unexpected data: {data}")
                return False
                
        except Exception as e:
            self.log_test("Users Endpoint", False, f"Exception: {str(e)}")
            return False
    
    def test_user_data_get(self) -> bool:
        """Test GET /user/data endpoint."""
        success_count = 0
        
        test_cases = [
            ("alice", "normal", "Welcome, alice!"),
            ("bob", "premium", "Hello, bob!"),
            ("carol", "ultra", "Hi, carol!")
        ]
        
        for username, expected_plan, expected_greeting in test_cases:
            try:
                response = self.session.get(f"{self.base_url}/user/data?username={username}")
                if response.status_code != 200:
                    self.log_test(f"User Data GET ({username})", False, f"Status code {response.status_code}")
                    continue
                
                data = response.json()
                if (data.get("username") == username and 
                    data.get("plan") == expected_plan and 
                    expected_greeting in data.get("data", "")):
                    self.log_test(f"User Data GET ({username})", True, f"Correct response for {expected_plan} plan")
                    success_count += 1
                else:
                    self.log_test(f"User Data GET ({username})", False, f"Unexpected response: {data}")
                    
            except Exception as e:
                self.log_test(f"User Data GET ({username})", False, f"Exception: {str(e)}")
        
        return success_count == len(test_cases)
    
    def test_user_data_post(self) -> bool:
        """Test POST /user/data endpoint."""
        try:
            payload = {"username": "alice"}
            response = self.session.post(
                f"{self.base_url}/user/data",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                self.log_test("User Data POST", False, f"Status code {response.status_code}")
                return False
            
            data = response.json()
            if (data.get("username") == "alice" and 
                data.get("plan") == "normal"):
                self.log_test("User Data POST", True, "POST request works correctly")
                return True
            else:
                self.log_test("User Data POST", False, f"Unexpected response: {data}")
                return False
                
        except Exception as e:
            self.log_test("User Data POST", False, f"Exception: {str(e)}")
            return False
    
    def test_user_feature_get(self) -> bool:
        """Test GET /user/feature endpoint."""
        success_count = 0
        
        test_cases = [
            ("alice", "normal", "NORMAL plan:"),
            ("bob", "premium", "PREMIUM plan:"),
            ("carol", "ultra", "ULTRA plan:")
        ]
        
        for username, expected_plan, expected_feature in test_cases:
            try:
                response = self.session.get(f"{self.base_url}/user/feature?username={username}")
                if response.status_code != 200:
                    self.log_test(f"User Feature GET ({username})", False, f"Status code {response.status_code}")
                    continue
                
                data = response.json()
                if (data.get("username") == username and 
                    data.get("plan") == expected_plan and 
                    expected_feature in data.get("features", "")):
                    self.log_test(f"User Feature GET ({username})", True, f"Correct features for {expected_plan} plan")
                    success_count += 1
                else:
                    self.log_test(f"User Feature GET ({username})", False, f"Unexpected response: {data}")
                    
            except Exception as e:
                self.log_test(f"User Feature GET ({username})", False, f"Exception: {str(e)}")
        
        return success_count == len(test_cases)
    
    def test_invalid_username(self) -> bool:
        """Test with invalid username."""
        try:
            response = self.session.get(f"{self.base_url}/user/data?username=invalid")
            if response.status_code != 200:
                self.log_test("Invalid Username", False, f"Status code {response.status_code}")
                return False
            
            data = response.json()
            if "not recognized" in data.get("data", "").lower():
                self.log_test("Invalid Username", True, "Properly handles invalid username")
                return True
            else:
                self.log_test("Invalid Username", False, f"Unexpected response: {data}")
                return False
                
        except Exception as e:
            self.log_test("Invalid Username", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self) -> bool:
        """Run all tests and return overall success."""
        print(f"Testing Mock Server at {self.base_url}")
        print("="*50)
        
        tests = [
            self.test_users_endpoint,
            self.test_user_data_get,
            self.test_user_data_post,
            self.test_user_feature_get,
            self.test_invalid_username
        ]
        
        results = []
        for test in tests:
            results.append(test())
        
        print("\n" + "="*50)
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["success"])
        
        print(f"TEST SUMMARY: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("✓ All tests PASSED!")
            return True
        else:
            print("✗ Some tests FAILED!")
            return False

def main():
    """Main function for command line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="API test for mock server")
    parser.add_argument("--url", default="http://localhost:3001",
                       help="Base URL of the server")
    
    args = parser.parse_args()
    
    tester = MockServerTester(args.url)
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
