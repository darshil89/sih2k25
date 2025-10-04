# ChromaDB Vector Database Client Configuration
import chromadb
from chromadb.config import Settings
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class ChromaDBClient:
    """ChromaDB Vector Database Client"""
    
    def __init__(self, host: str = None, port: int = None, collection_name: str = None):
        """Initialize ChromaDB client"""
        self.host = host or os.getenv("CHROMA_HOST")
        self.port = port or int(os.getenv("CHROMA_PORT"))
        self.collection_name = collection_name or os.getenv("CHROMA_COLLECTION")
        
        self.client = None
        self.collection = None
        self._connect()
    
    def _connect(self):
        """Establish connection to ChromaDB"""
        try:
            # Initialize ChromaDB client
            self.client = chromadb.HttpClient(
                host=self.host,
                port=self.port,
                settings=Settings(
                    allow_reset=True,
                    anonymized_telemetry=False
                )
            )
            
            # Get or create collection
            self._get_or_create_collection()
            logger.info(f"Connected to ChromaDB at {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to connect to ChromaDB: {e}")
            raise
    
    def _get_or_create_collection(self):
        """Get existing collection or create new one"""
        try:
            # Try to get existing collection
            self.collection = self.client.get_collection(name=self.collection_name)
            logger.info(f"Using existing collection: {self.collection_name}")
        except Exception:
            # Create new collection if it doesn't exist
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "UFDR documents and reports"}
            )
            logger.info(f"Created new collection: {self.collection_name}")

# Global ChromaDB client instance
chroma_client = None

def get_chroma_client() -> ChromaDBClient:
    """Get or create global ChromaDB client instance"""
    global chroma_client
    if chroma_client is None:
        chroma_client = ChromaDBClient()
    return chroma_client

def close_chroma_client():
    """Close the global ChromaDB client"""
    global chroma_client
    if chroma_client:
        chroma_client = None
