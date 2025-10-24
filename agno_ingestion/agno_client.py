"""API client for Agno-RAG service."""

import os
import logging
import requests
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class AgnoRAGClient:
    """Client wrapper for Agno-RAG API with authentication and retry logic."""

    def __init__(
        self,
        base_url: str,
        email: Optional[str] = None,
        password: Optional[str] = None,
        max_retries: int = 3,
        timeout: int = 30
    ):
        """
        Initialize Agno-RAG client.
        
        Args:
            base_url: Base URL for Agno-RAG API (e.g., http://localhost:8000)
            email: User email for authentication
            password: User password for authentication
            max_retries: Maximum retry attempts for failed requests
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.email = email
        self.password = password
        self.max_retries = max_retries
        self.timeout = timeout
        self.token: Optional[str] = None
        self.session = requests.Session()
        
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication."""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    def _retry_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Execute request with exponential backoff retry logic.
        
        Args:
            method: HTTP method (GET, POST, DELETE, etc.)
            url: Request URL
            **kwargs: Additional arguments for requests
            
        Returns:
            Response object
            
        Raises:
            Exception: If all retries fail
        """
        for attempt in range(self.max_retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    timeout=self.timeout,
                    **kwargs
                )
                
                # If successful or client error (4xx), return immediately
                if response.status_code < 500:
                    return response
                
                # Server error - retry with exponential backoff
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(
                        f"Request failed with {response.status_code}, "
                        f"retrying in {wait_time}s (attempt {attempt + 1}/{self.max_retries})"
                    )
                    time.sleep(wait_time)
                    
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(
                        f"Request exception: {e}, "
                        f"retrying in {wait_time}s (attempt {attempt + 1}/{self.max_retries})"
                    )
                    time.sleep(wait_time)
                else:
                    raise
        
        return response
    
    def login(self) -> bool:
        """
        Authenticate and obtain JWT token.
        
        Returns:
            True if login successful, False otherwise
        """
        if not self.email or not self.password:
            logger.warning("No credentials provided, skipping authentication")
            return False
        
        try:
            response = self._retry_request(
                "POST",
                f"{self.base_url}/v1/auth/login",
                json={"email": self.email, "password": self.password},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data["access_token"]
                logger.info(f"Successfully authenticated as {self.email}")
                return True
            else:
                logger.error(f"Login failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False
    
    def health_check(self) -> Dict:
        """
        Check API health status.
        
        Returns:
            Health status dictionary
        """
        try:
            response = self._retry_request(
                "GET",
                f"{self.base_url}/health",
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            raise
    
    def create_collection(
        self,
        name: str,
        description: Optional[str] = None
    ) -> Dict:
        """
        Create a new collection.
        
        Args:
            name: Collection name
            description: Optional collection description
            
        Returns:
            Collection metadata dictionary
        """
        try:
            payload = {"name": name}
            if description:
                payload["description"] = description
            
            response = self._retry_request(
                "POST",
                f"{self.base_url}/v1/collections",
                json=payload,
                headers=self._get_headers()
            )
            response.raise_for_status()
            
            collection = response.json()
            logger.info(f"Created collection: {name} (ID: {collection['id']})")
            return collection
            
        except Exception as e:
            logger.error(f"Failed to create collection {name}: {e}")
            raise
    
    def list_collections(self, offset: int = 0, limit: int = 100) -> List[Dict]:
        """
        List all collections.
        
        Args:
            offset: Pagination offset
            limit: Maximum number of results
            
        Returns:
            List of collection dictionaries
        """
        try:
            response = self._retry_request(
                "GET",
                f"{self.base_url}/v1/collections",
                params={"offset": offset, "limit": limit},
                headers=self._get_headers()
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get("results", [])
            
        except Exception as e:
            logger.error(f"Failed to list collections: {e}")
            raise
    
    def get_collection(self, collection_id: str) -> Optional[Dict]:
        """
        Get collection by ID.
        
        Args:
            collection_id: Collection UUID
            
        Returns:
            Collection dictionary or None if not found
        """
        try:
            response = self._retry_request(
                "GET",
                f"{self.base_url}/v1/collections/{collection_id}",
                headers=self._get_headers()
            )
            
            if response.status_code == 404:
                return None
            
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Failed to get collection {collection_id}: {e}")
            raise
    
    def upload_pre_chunked_document(
        self,
        collection_id: str,
        parent_document_name: str,
        chunks: List[Dict[str, Any]],
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Upload a pre-chunked document.
        
        Args:
            collection_id: Collection UUID
            parent_document_name: Name of the parent document
            chunks: List of chunk dictionaries with 'content', 'chunk_index', 'metadata'
            metadata: Optional parent document metadata
            
        Returns:
            Upload response dictionary
        """
        try:
            payload = {
                "collection_id": collection_id,
                "parent_document_name": parent_document_name,
                "chunks": chunks
            }
            
            if metadata:
                payload["metadata"] = metadata
            
            response = self._retry_request(
                "POST",
                f"{self.base_url}/v1/documents/chunks",
                json=payload,
                headers=self._get_headers()
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(
                f"Uploaded document '{parent_document_name}' "
                f"with {len(chunks)} chunks to collection {collection_id}"
            )
            return result
            
        except Exception as e:
            logger.error(f"Failed to upload document '{parent_document_name}': {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                logger.error(f"Response: {e.response.text}")
            raise
    
    def delete_document(
        self,
        document_id: str,
        collection_id: str
    ) -> bool:
        """
        Delete a document and all its chunks.
        
        Args:
            document_id: Document UUID
            collection_id: Collection UUID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            response = self._retry_request(
                "DELETE",
                f"{self.base_url}/v1/documents/{document_id}",
                params={"collection_id": collection_id},
                headers=self._get_headers()
            )
            
            if response.status_code == 404:
                logger.warning(f"Document {document_id} not found")
                return False
            
            response.raise_for_status()
            logger.info(f"Deleted document {document_id} from collection {collection_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete document {document_id}: {e}")
            return False
    
    def list_documents(
        self,
        collection_id: str,
        offset: int = 0,
        limit: int = 50
    ) -> List[Dict]:
        """
        List documents in a collection.
        
        Args:
            collection_id: Collection UUID
            offset: Pagination offset
            limit: Maximum number of results
            
        Returns:
            List of document dictionaries
        """
        try:
            response = self._retry_request(
                "GET",
                f"{self.base_url}/v1/documents",
                params={
                    "collection_id": collection_id,
                    "offset": offset,
                    "limit": limit
                },
                headers=self._get_headers()
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get("results", [])
            
        except Exception as e:
            logger.error(f"Failed to list documents: {e}")
            raise
    
    def search(
        self,
        query: str,
        collection_id: str,
        mode: str = "traditional",
        limit: int = 5
    ) -> Dict:
        """
        Search documents in a collection.
        
        Args:
            query: Search query
            collection_id: Collection UUID
            mode: Search mode ('traditional' or 'agentic')
            limit: Maximum number of results
            
        Returns:
            Search results dictionary
        """
        try:
            payload = {
                "query": query,
                "collection_id": collection_id,
                "mode": mode,
                "limit": limit
            }
            
            response = self._retry_request(
                "POST",
                f"{self.base_url}/v1/search",
                json=payload,
                headers=self._get_headers()
            )
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise

