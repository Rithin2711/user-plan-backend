#!/usr/bin/env python3
"""
Simple load test script for the mock server.
Tests the performance and reliability under concurrent requests.
"""

import asyncio
import aiohttp
import time
import statistics
from typing import List, Dict, Any

async def make_request(session: aiohttp.ClientSession, url: str, username: str) -> Dict[str, Any]:
    """Make a single request and measure response time."""
    start_time = time.time()
    try:
        async with session.get(f"{url}/user/data?username={username}") as response:
            await response.json()
            end_time = time.time()
            return {
                "success": True,
                "response_time": end_time - start_time,
                "status_code": response.status
            }
    except Exception as e:
        end_time = time.time()
        return {
            "success": False,
            "response_time": end_time - start_time,
            "error": str(e)
        }

async def run_load_test(base_url: str = "http://localhost:3001", 
                       concurrent_users: int = 10, 
                       requests_per_user: int = 10) -> Dict[str, Any]:
    """
    Run a load test with concurrent users.
    
    Args:
        base_url: Base URL of the server
        concurrent_users: Number of concurrent users
        requests_per_user: Number of requests each user makes
        
    Returns:
        Dictionary with test results
    """
    usernames = ["alice", "bob", "carol"]
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        # Create tasks for concurrent users
        for user_id in range(concurrent_users):
            username = usernames[user_id % len(usernames)]
            for _ in range(requests_per_user):
                task = make_request(session, base_url, username)
                tasks.append(task)
        
        # Execute all requests concurrently
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()
    
    # Analyze results
    successful_requests = [r for r in results if r["success"]]
    failed_requests = [r for r in results if not r["success"]]
    
    response_times = [r["response_time"] for r in successful_requests]
    
    return {
        "total_requests": len(results),
        "successful_requests": len(successful_requests),
        "failed_requests": len(failed_requests),
        "success_rate": len(successful_requests) / len(results) * 100,
        "total_time": end_time - start_time,
        "requests_per_second": len(results) / (end_time - start_time),
        "response_times": {
            "min": min(response_times) if response_times else 0,
            "max": max(response_times) if response_times else 0,
            "mean": statistics.mean(response_times) if response_times else 0,
            "median": statistics.median(response_times) if response_times else 0
        },
        "errors": [r.get("error") for r in failed_requests]
    }

def main():
    """Main function for command line usage."""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Load test for mock server")
    parser.add_argument("--url", default="http://localhost:3001",
                       help="Base URL of the server")
    parser.add_argument("--users", type=int, default=10,
                       help="Number of concurrent users")
    parser.add_argument("--requests", type=int, default=10,
                       help="Number of requests per user")
    
    args = parser.parse_args()
    
    print(f"Running load test with {args.users} concurrent users, {args.requests} requests each...")
    
    results = asyncio.run(run_load_test(args.url, args.users, args.requests))
    
    print("\n" + "="*50)
    print("LOAD TEST RESULTS")
    print("="*50)
    print(f"Total Requests: {results['total_requests']}")
    print(f"Successful: {results['successful_requests']}")
    print(f"Failed: {results['failed_requests']}")
    print(f"Success Rate: {results['success_rate']:.1f}%")
    print(f"Total Time: {results['total_time']:.2f}s")
    print(f"Requests/Second: {results['requests_per_second']:.2f}")
    print("\nResponse Times:")
    print(f"  Min: {results['response_times']['min']*1000:.0f}ms")
    print(f"  Max: {results['response_times']['max']*1000:.0f}ms")
    print(f"  Mean: {results['response_times']['mean']*1000:.0f}ms")
    print(f"  Median: {results['response_times']['median']*1000:.0f}ms")
    
    if results['errors']:
        print(f"\nErrors: {len(results['errors'])}")
        for error in set(results['errors']):
            if error:
                print(f"  - {error}")

if __name__ == "__main__":
    main()
