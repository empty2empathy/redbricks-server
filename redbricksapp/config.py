import os
import boto3


ENV = os.environ.get("ENV", "local")


def get_connection_string():
    if ENV in ("production"):
        ssm = boto3.client("ssm")
        response = ssm.get_parameters(Names=["RedbricksDB"], WithDecryption=True)

        return response["Parameters"][0]["Value"]
    else:
        return os.environ["DB_CONNECTION_STRING"]  # rfc1738


connection_string = get_connection_string()
