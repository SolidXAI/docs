import os
import logging
from r2r import R2RClient
from typing import Any, Dict, Optional
import toml

logger = logging.getLogger(__name__)


class R2RHelper:
    """
    Wrapper around R2RClient that auto-initializes from environment variables.

    Expected environment variables:
      GENAI_RAG_SERVER_URL   -> e.g. "http://localhost:7272"
      GENAI_RAG_SERVER_LOGIN      -> user email for login
      GENAI_RAG_SERVER_PASSWORD   -> user password for login
    """

    def __init__(self):
        self.base_url = os.getenv("GENAI_RAG_SERVER_URL", "http://localhost:7272")
        self.email = os.getenv("GENAI_RAG_SERVER_LOGIN")
        self.password = os.getenv("GENAI_RAG_SERVER_PASSWORD")
        self.client: Optional[R2RClient] = None

    def connect(self) -> R2RClient:
        """Initialize client and login if creds available."""
        self.client = R2RClient(self.base_url)

        # Health check
        # try:
        #     health = self.client.health()
        #     if health.get("status") != "ok":
        #         logger.warning("R2R health check returned %s", health)
        #     else:
        #         logger.debug("R2R health check ok at %s", self.base_url)
        # except Exception as e:
        #     logger.error("Failed health check against %s: %s", self.base_url, e)
        #     raise

        # Login if credentials provided
        if self.email and self.password:
            try:
                self.client.users.login(self.email, self.password)
                logger.info("R2R login successful for %s", self.email)
            except Exception as e:
                logger.error("R2R login failed for %s: %s", self.email, e)
                raise

        return self.client

    # def search(
    #     self,
    #     query: str,
    #     *,
    #     filters: Optional[Dict[str, Any]] = None,
    #     top_k: int = 5,
    # ) -> Any:
    #     """
    #     Perform a semantic search via R2R retrieval.

    #     Args:
    #         query: Natural language query
    #         filters: Optional dict of filters (e.g. {"kind": "solidx-metadata"})
    #         top_k: Max number of results

    #     Returns:
    #         R2R search results (list of hits or raw response depending on SDK)
    #     """
    #     if not self.client:
    #         raise RuntimeError("R2R client not initialized. Call connect() first.")

    #     try:
    #         results = self.client.retrieval.search(
    #             query=query,
    #             # filters=filters or {},
    #             # top_k=top_k,
    #         )
    #         return results
    #     except Exception as e:
    #         logger.error("R2R search failed for query=%r: %s", query, e)
    #         raise

    # def rag_search(
    #     self,
    #     query: str,
    #     rag_generation_config,
    #     search_settings,
    #     *,
    #     filters: Optional[Dict[str, Any]] = None,
    #     top_k: int = 5,
    # ) -> Any:
    #     """
    #     Perform a semantic search via R2R retrieval.

    #     Args:
    #         query: Natural language query
    #         filters: Optional dict of filters (e.g. {"kind": "solidx-metadata"})
    #         top_k: Max number of results

    #     Returns:
    #         R2R search results (list of hits or raw response depending on SDK)
    #     """
    #     print("ANTHROPIC_API_KEY =", os.getenv("ANTHROPIC_API_KEY"))
    #     if not self.client:
    #         raise RuntimeError("R2R client not initialized. Call connect() first.")

    #     try:
    #         results = self.client.retrieval.rag(
    #             query,
    #             rag_generation_config=rag_generation_config,
    #             search_settings=search_settings,
    #         )
    #         return results
    #     except Exception as e:
    #         logger.error("R2R search failed for query=%r: %s", query, e)
    #         raise
