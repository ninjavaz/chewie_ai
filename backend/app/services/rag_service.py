"""
RAG (Retrieval-Augmented Generation) service using pgvector.
Handles document retrieval and semantic search.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy import select, func, cast, type_coerce, text
from sqlalchemy.ext.asyncio import AsyncSession
from pgvector.sqlalchemy import Vector
from app.models.database import Document
from app.utils.embeddings import get_embedding_service


class RAGService:
    """Service for RAG operations with pgvector."""
    
    def __init__(self):
        self.embedding_service = get_embedding_service()
    
    async def retrieve_relevant_documents(
        self,
        query: str,
        db: AsyncSession,
        top_k: int = 3,
        similarity_threshold: float = 0.7,
        dapp: str = "kamino",
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query using semantic search.
        
        Args:
            query: User's query
            db: Database session
            top_k: Number of documents to retrieve
            similarity_threshold: Minimum similarity score
            dapp: Filter by dapp name
            
        Returns:
            List of relevant documents with metadata
        """
        # Generate query embedding
        query_embedding = self.embedding_service.encode(query)
        
        # Convert to pgvector format: "[1,2,3]"
        embedding_str = '[' + ','.join(map(str, query_embedding)) + ']'
        
        # Use text() to create a raw SQL expression that bypasses pgvector validation
        embedding_literal = text(f"'{embedding_str}'::vector")
        
        # Perform vector similarity search
        # Using pgvector's <-> operator for L2 distance
        stmt = (
            select(
                Document.id,
                Document.title,
                Document.content,
                Document.url,
                Document.doc_type,
                Document.meta_data,
                # Calculate cosine similarity (1 - cosine_distance)
                (1 - func.cosine_distance(Document.embedding, embedding_literal)).label("similarity")
            )
            .where(Document.dapp == dapp)
            .where(Document.embedding.isnot(None))
            .order_by(func.cosine_distance(Document.embedding, embedding_literal))
            .limit(top_k * 2)  # Get more, then filter by threshold
        )
        
        result = await db.execute(stmt)
        rows = result.all()
        
        # Filter by similarity threshold and format results
        documents = []
        for row in rows:
            if row.similarity >= similarity_threshold:
                documents.append({
                    "id": str(row.id),
                    "title": row.title,
                    "content": row.content,
                    "url": row.url,
                    "doc_type": row.doc_type,
                    "metadata": row.meta_data,
                    "similarity": float(row.similarity),
                })
                
                if len(documents) >= top_k:
                    break
        
        return documents
    
    async def build_context(
        self,
        documents: List[Dict[str, Any]],
        max_length: int = 2000,
    ) -> str:
        """
        Build context string from retrieved documents.
        
        Args:
            documents: List of retrieved documents
            max_length: Maximum context length in characters
            
        Returns:
            Formatted context string
        """
        if not documents:
            return ""
        
        context_parts = []
        current_length = 0
        
        for doc in documents:
            # Format document
            doc_text = f"[{doc['title']}]\n{doc['content']}\nSource: {doc['url']}\n"
            doc_length = len(doc_text)
            
            # Check if adding this document would exceed max length
            if current_length + doc_length > max_length:
                # Truncate the document to fit
                remaining = max_length - current_length
                if remaining > 100:  # Only add if we have reasonable space
                    doc_text = doc_text[:remaining] + "..."
                    context_parts.append(doc_text)
                break
            
            context_parts.append(doc_text)
            current_length += doc_length
        
        return "\n\n".join(context_parts)
    
    async def add_document(
        self,
        title: str,
        content: str,
        url: str,
        db: AsyncSession,
        dapp: str = "kamino",
        doc_type: str = "documentation",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Document:
        """
        Add a new document to the database with embedding.
        
        Args:
            title: Document title
            content: Document content
            url: Source URL
            db: Database session
            dapp: DApp name
            doc_type: Type of document
            metadata: Additional metadata
            
        Returns:
            Created Document instance
        """
        # Generate embedding
        embedding = self.embedding_service.encode(content)
        
        # Create document
        document = Document(
            title=title,
            content=content,
            url=url,
            dapp=dapp,
            doc_type=doc_type,
            embedding=embedding,
            meta_data=metadata,
        )
        
        db.add(document)
        await db.flush()
        
        return document
    
    async def update_document_embedding(
        self,
        document_id: str,
        db: AsyncSession,
    ) -> bool:
        """
        Regenerate embedding for a document.
        
        Args:
            document_id: Document UUID
            db: Database session
            
        Returns:
            True if successful
        """
        stmt = select(Document).where(Document.id == document_id)
        result = await db.execute(stmt)
        document = result.scalar_one_or_none()
        
        if not document:
            return False
        
        # Regenerate embedding
        embedding = self.embedding_service.encode(document.content)
        document.embedding = embedding
        
        await db.flush()
        return True
    
    async def search_documents(
        self,
        query: str,
        db: AsyncSession,
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 10,
    ) -> List[Document]:
        """
        Search documents with optional filters.
        
        Args:
            query: Search query
            db: Database session
            filters: Optional filters (dapp, doc_type, etc.)
            top_k: Number of results
            
        Returns:
            List of matching documents
        """
        query_embedding = self.embedding_service.encode(query)
        
        # Convert to pgvector format: "[1,2,3]"
        embedding_str = '[' + ','.join(map(str, query_embedding)) + ']'
        
        # Use text() to create a raw SQL expression that bypasses pgvector validation
        embedding_literal = text(f"'{embedding_str}'::vector")
        
        stmt = (
            select(Document)
            .order_by(func.cosine_distance(Document.embedding, embedding_literal))
            .limit(top_k)
        )
        
        # Apply filters
        if filters:
            if "dapp" in filters:
                stmt = stmt.where(Document.dapp == filters["dapp"])
            if "doc_type" in filters:
                stmt = stmt.where(Document.doc_type == filters["doc_type"])
        
        result = await db.execute(stmt)
        return list(result.scalars().all())


# Global instance
_rag_service: Optional[RAGService] = None


def get_rag_service() -> RAGService:
    """Get or create RAGService instance."""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service
