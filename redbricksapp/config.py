import os
import boto3


ENV = os.environ.get("ENV", "local")


def get_connection_string():
    if ENV in ("production"):
        ssm = boto3.client("ssm")
        response = ssm.get_parameter(
            Name="/REDBRICKS/PRODUCTION/DB", WithDecryption=True
        )

        return response["Parameter"]["Value"]
    else:
        return os.environ["DB_CONNECTION_STRING"]  # rfc1738


connection_string = get_connection_string()
