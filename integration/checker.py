import json
import os


def main():
    print(f"HP_IDP_SERVICE_ID: {os.environ.get('HP_IDP_SERVICE_ID')}")
    print(f"HP_IDP_SERVICE_SECRET: {os.environ.get('HP_IDP_SERVICE_SECRET')}")
    print(f"GITHUB_STATUS: {os.environ.get('GITHUB_STATUS')}")
    print(f"AZ_PAT_TEST_PLANS: {os.environ.get('AZ_PAT_TEST_PLANS')}")

    with open("inputs.json", "r") as f:
        data = f.read()
        valid_json_str = data.replace("'", '"')
        json_data = json.loads(valid_json_str)
        print(json_data)
