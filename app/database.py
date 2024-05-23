from neo4j import GraphDatabase, basic_auth
import os
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

URI = os.getenv("NEO4J_URI", "bolt://memgraph:7687")
USER = os.getenv("NEO4J_USER", "")
PASSWORD = os.getenv("NEO4J_PASSWORD", "")
AUTH = basic_auth(USER, PASSWORD)


class Database:
    def __init__(self):
        self.driver = None
        self.connect_with_retry()

    def connect_with_retry(self):
        retry_count = 0
        while True:
            try:
                self.driver = GraphDatabase.driver(URI, auth=AUTH)
                # Try to open a session to check if the connection is successful
                with self.driver.session() as session:
                    session.run("RETURN 1")
                logger.info(f"Connected to Memgraph at {URI}")
                break
            except Exception as e:
                retry_count += 1
                logger.error(f"Failed to connect to Memgraph at {URI}: {e}")
                if retry_count >= 5:
                    raise e
                time.sleep(5)

    def close(self):
        if self.driver:
            self.driver.close()

    def get_session(self):
        return self.driver.session()


db = Database()


def get_db():
    try:
        yield db
    finally:
        db.close()
