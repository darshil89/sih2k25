# Neo4j Knowledge Graph Client Configuration
from neo4j import GraphDatabase
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class Neo4jClient:
    """Neo4j Knowledge Graph Client"""
    
    def __init__(self, uri: str = None, username: str = None, password: str = None):
        """Initialize Neo4j client"""
        self.uri = uri or os.getenv("NEO4J_URI")
        self.username = username or os.getenv("NEO4J_USER")
        self.password = password or os.getenv("NEO4J_PASSWORD")
        
        self.driver = None
        self._connect()
    
    def _connect(self):
        """Establish connection to Neo4j database"""
        try:
            self.driver = GraphDatabase.driver(
                self.uri, 
                auth=(self.username, self.password)
            )
            # Test connection
            with self.driver.session() as session:
                session.run("RETURN 1")
            logger.info(f"Connected to Neo4j at {self.uri}")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise
    
    def close(self):
        """Close the database connection"""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed")

# Global Neo4j client instance
neo4j_client = None

def get_neo4j_client() -> Neo4jClient:
    """Get or create global Neo4j client instance"""
    global neo4j_client
    if neo4j_client is None:
        neo4j_client = Neo4jClient()
    return neo4j_client

def close_neo4j_client():
    """Close the global Neo4j client"""
    global neo4j_client
    if neo4j_client:
        neo4j_client.close()
        neo4j_client = None
