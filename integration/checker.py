import json
import os
import sys


def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    print(f"HP_IDP_SERVICE_ID: {os.environ.get('HP_IDP_SERVICE_ID')}")
    print(f"HP_IDP_SERVICE_SECRET: {os.environ.get('HP_IDP_SERVICE_SECRET')}")
    print(f"GITHUB_STATUS: {os.environ.get('GITHUB_STATUS')}")
    print(f"AZ_PAT_TEST_PLANS: {os.environ.get('AZ_PAT_TEST_PLANS')}")

    filename = sys.argv[1]
    with open(filename, "r") as f:
        content = f.read()
    print(content)
    valid_json_data = content.replace("'", '"')
    print(valid_json_data)
    
