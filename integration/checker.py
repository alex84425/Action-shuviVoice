# this is a cli tool, which can be used to check the correctness of the feature test
import argparse
import json
import os


def main():
    # print env variables
    print("ENV variables :")
    # print("RepositoryName: " + os.environ["RepositoryName"])
    # print("SourceVersion: " + os.environ["SourceVersion"])
    print(f"HP_IDP_SERVICE_ID: {os.environ.get('HP_IDP_SERVICE_ID')}")
    print(f"HP_IDP_SERVICE_SECRET: {os.environ.get('HP_IDP_SERVICE_SECRET')}")
    print(f"GITHUB_STATUS: {os.environ.get('GITHUB_STATUS')}")
    print(f"AZ_PAT_TEST_PLANS: {os.environ.get('AZ_PAT_TEST_PLANS')}")

    parser = argparse.ArgumentParser(description="Feature Test Checker")
    parser.add_argument("payload", type=str, help="ATC task done subscription callback payload")
    print("payload variables:")
    args = parser.parse_args()
    print(args.payload)
    # valid_json_data = args.payload.replace("'", '"')
    # print("payload as dict variables:")
    # my_dict = json.loads(valid_json_data)
    # print(my_dict)


if __name__ == "__main__":
    main()
