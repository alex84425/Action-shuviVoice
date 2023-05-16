import os
import sys


def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    # print(f"HP_IDP_SERVICE_ID: {os.environ.get('HP_IDP_SERVICE_ID')}")
    # print(f"HP_IDP_SERVICE_SECRET: {os.environ.get('HP_IDP_SERVICE_SECRET')}")
    # print(f"GITHUB_STATUS: {os.environ.get('GITHUB_STATUS')}")
    # print(f"AZ_PAT_TEST_PLANS: {os.environ.get('AZ_PAT_TEST_PLANS')}")

    print("################################################")
    for i in sys.argv:
        print(i)
    print("################################################")

    filename = sys.argv[1]
    print(filename)

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    print("content")
    valid_json_data = content.replace("'", '"')
    print(f"{valid_json_data}:")
