import os

ENV = os.environ.get('ENV', 'local')
connection_string = "sqlite:///:memory:"  # rfc1738
