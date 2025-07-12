"""
AI Agents for GraphQL query generation and response formatting
"""

from openai import OpenAI
from typing import List, Dict, Any, Optional
import json
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class GraphQLQueryAgent:
    def __init__(self, openai_api_key: Optional[str] = None):
        """Initialize the GraphQL query generation agent"""
        from source.config import settings
        self.client = OpenAI(api_key=openai_api_key or settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.temperature = settings.OPENAI_TEMPERATURE
        self.max_tokens = settings.OPENAI_MAX_TOKENS
        
    def generate_query(self, user_query: str, relevant_chunks: List[Dict[str, Any]], 
                      endpoint: str) -> str:
        """Generate a GraphQL query based on user query and relevant schema chunks"""
        
        # Prepare context from chunks
        context = self._prepare_context(relevant_chunks)
        
        system_prompt = """You are a GraphQL query expert specializing in Kusama blockchain data.
        Your task is to generate a precise GraphQL query based on the user's question and the provided schema information.
        
        IMPORTANT RULES:
        1. Always return valid GraphQL syntax
        2. Use the exact field names and types from the schema
        3. Include relevant filters, ordering, and pagination as needed
        4. For amounts, remember they are in smallest units (1 KSM = 1,000,000,000,000 units)
        5. Use proper timestamp format for date filtering (ISO 8601)
        6. Always include necessary fields in the response
        7. Return ONLY the GraphQL query without any explanation or markdown formatting
        
        Schema Context:
        {context}
        """
        
        user_prompt = f"""
        Generate a GraphQL query for this request: {user_query}
        
        The GraphQL endpoint is: {endpoint}
        
        Based on the provided schema context, create a query that:
        1. Addresses the user's specific question
        2. Uses appropriate filters and sorting
        3. Includes relevant fields in the response
        4. Handles pagination if needed
        
        Return only the GraphQL query without any additional text.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt.format(context=context)},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            query = response.choices[0].message.content.strip()
            
            # Clean up the query (remove markdown formatting if present)
            if query.startswith("```"):
                query = query.split("```")[1]
                if query.startswith("graphql"):
                    query = query[7:].strip()
            
            logger.info(f"Generated GraphQL query for: {user_query}")
            return query
            
        except Exception as e:
            logger.error(f"Error generating GraphQL query: {e}")
            raise
    
    def _prepare_context(self, chunks: List[Dict[str, Any]]) -> str:
        """Prepare context string from relevant chunks"""
        context_parts = []
        
        for chunk in chunks:
            part = f"ID: {chunk['id']}\n"
            part += f"Content: {chunk['content']}\n"
            
            if 'metadata' in chunk:
                metadata = chunk['metadata']
                if 'examples' in metadata:
                    part += f"Examples: {'; '.join(metadata['examples'])}\n"
                if 'keywords' in metadata:
                    part += f"Keywords: {', '.join(metadata['keywords'])}\n"
            
            context_parts.append(part)
        
        return "\n---\n".join(context_parts)


class ResponseAgent:
    def __init__(self, openai_api_key: Optional[str] = None):
        """Initialize the natural language response agent"""
        from source.config import settings
        self.client = OpenAI(api_key=openai_api_key or settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.temperature = settings.OPENAI_TEMPERATURE
        self.max_tokens = settings.OPENAI_MAX_TOKENS
    
    def generate_response(self, user_query: str, graphql_data: Dict[str, Any], 
                         relevant_chunks: List[Dict[str, Any]]) -> str:
        """Generate a natural language response based on GraphQL data"""
        
        # Prepare context from chunks
        context = self._prepare_context(relevant_chunks)
        
        system_prompt = """You are a helpful assistant that explains Kusama blockchain data in clear, natural language.
        Your task is to interpret GraphQL query results and provide informative answers to user questions.
        
        IMPORTANT GUIDELINES:
        1. Convert amounts from smallest units to KSM (1 KSM = 1,000,000,000,000 units)
        2. Format timestamps in a readable way
        3. Explain technical terms when necessary
        4. Provide context about what the data means
        5. Be concise but informative
        6. If there's no data, explain what that means
        7. Use proper formatting for addresses (show first and last few characters)
        8. Include relevant insights about the data
        
        Schema Context:
        {context}
        """
        
        user_prompt = f"""
        User Question: {user_query}
        
        GraphQL Response Data: {json.dumps(graphql_data, indent=2)}
        
        Please provide a clear, informative response that:
        1. Directly answers the user's question
        2. Explains what the data shows
        3. Provides relevant context and insights
        4. Formats technical data in a user-friendly way
        
        If there are errors in the data or no results, explain what that means and suggest alternatives.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt.format(context=context)},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            natural_response = response.choices[0].message.content.strip()
            
            logger.info(f"Generated natural language response for: {user_query}")
            return natural_response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    def _prepare_context(self, chunks: List[Dict[str, Any]]) -> str:
        """Prepare context string from relevant chunks"""
        context_parts = []
        
        for chunk in chunks:
            part = f"ID: {chunk['id']}\n"
            part += f"Content: {chunk['content']}\n"
            
            if 'metadata' in chunk:
                metadata = chunk['metadata']
                if 'keywords' in metadata:
                    part += f"Keywords: {', '.join(metadata['keywords'])}\n"
            
            context_parts.append(part)
        
        return "\n---\n".join(context_parts) 