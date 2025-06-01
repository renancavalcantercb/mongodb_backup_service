#!/usr/bin/env python3

import requests
import json
import time
from typing import bool


def test_health_check() -> bool:
    print("Testing health check endpoint...")
    try:
        response = requests.get("http://localhost:5000/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"ERROR: Health check failed: {e}")
        return False


def test_backup() -> bool:
    print("\nTesting backup endpoint...")
    try:
        response = requests.post("http://localhost:5000/trigger_backup")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"ERROR: Backup test failed: {e}")
        return False


def main() -> None:
    print("MongoDB Backup Service - Test Suite")
    print("=" * 50)

    health_ok = test_health_check()

    if not health_ok:
        print("ERROR: Health check failed. Verify if the service is running.")
        return

    print("SUCCESS: Health check passed")

    time.sleep(1)

    backup_ok = test_backup()

    if backup_ok:
        print("SUCCESS: Backup test completed successfully")
    else:
        print("ERROR: Backup test failed. Check MongoDB configuration.")

    print("\n" + "=" * 50)
    print("Test suite completed")


if __name__ == "__main__":
    main()
