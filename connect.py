import pymysql
from sshtunnel import SSHTunnelForwarder
import configparser
import sys

# Load configuration
config = configparser.ConfigParser()
config_path = 'config.ini'
config.read(config_path)

def connect():
    try:
        ssh_host = config['ssh_tunnel']['ssh_host']
        ssh_port = int(config['ssh_tunnel']['ssh_port'])
        ssh_username = config['ssh_tunnel']['ssh_username']
        ssh_pem_key = config['ssh_tunnel']['ssh_pem_key']

        db_host = config['database']['db_host']
        db_port = int(config['database']['db_port'])
        db_user = config['database']['db_user']
        db_password = config['database']['db_password']

    except KeyError as e:
        print(f"Error: Missing key {e} in {config_path}")
        sys.exit(1)

    # Establishing SSH tunnel
    try:
        tunnel = SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_username,
            ssh_private_key=ssh_pem_key,
            remote_bind_address=(db_host, db_port),
        )
        tunnel.start()
        print("tunnel started")

    except Exception as e:
        print(f"Error establishing SSH tunnel: {e}")
        sys.exit(1)

    # Connecting to the database through the SSH tunnel
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            port=tunnel.local_bind_port,
            user=db_user,
            passwd=db_password,
        )
        print("Successfully connected to the database.")
        
        # Test the connection
        return conn

    except pymysql.Error as err:
        print(f"Database connection failed: {err}")
        tunnel.stop()
        sys.exit(1)
