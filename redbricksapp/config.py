import os

ENV = os.environ.get('ENV', 'local')
connection_string = os.environ['DB_CONNECTION_STRING']  # rfc1738
