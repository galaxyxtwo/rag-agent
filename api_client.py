import os
import requests
import json
from config import API_URL, DEFAULT_MODEL, DEFAULT_MAX_TOKENS, DEFAULT_TEMPERATURE
from logger import logger
from ui import ThinkingAnimation

class APIClient:
    """Handles interaction with API"""

    def __init__(self, api_token=None):
        self.api_url = API_URL
        self.api_token = api_token or os.getenv("API_TOKEN")
        logger.info(f"🔗 API Client initialized with URL: {self.api_url}")

    def query(self, query: str, context: str) -> str:
        """Query API with the given query and context"""

        system_prompt = """You are an AI assistant that answers questions using only the provided context.

1. Read ALL provided context carefully before answering.
2. ONLY use information present in the context.
3. Provide a clear and direct answer using the most relevant details.
4. If the answer is NOT in the context, say 'NO MATCH FOUND'.
5. DO NOT mention 'chunks', 'CHUNK X', 'Issue X', 'Issue', or any metadata related to document retrieval.
6. If the context includes issue numbers, REWRITE the response to exclude them.
7. Instead of referencing "Issue X," rephrase the information naturally. 
   - Example: Instead of saying "Using multiple GPUs (Issue 2)," say "A common issue is configuring multiple GPUs correctly."
8. Summarize issues in a way that is natural and avoids referencing the original structure of the document."""

        # **Remove chunk identifiers from context**
        cleaned_context = self._clean_context(context)

        user_prompt = f"""Context:
    {cleaned_context}

    Question: {query}

    Answer strictly based on the context above:
    """

        payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": DEFAULT_MAX_TOKENS,
            "temperature": DEFAULT_TEMPERATURE,
            "stream": True
        }
        
        # Add model only if it's specified in config
        if DEFAULT_MODEL:
            payload["model"] = DEFAULT_MODEL

        headers = {
            "Content-Type": "application/json"
        }
        
        # Only add authorization if token exists (for remote APIs)
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"

        thinking = ThinkingAnimation()
        thinking.start()

        try:
            logger.info(f"🚀 Making POST request to: {self.api_url}")
            logger.info(f"📤 Payload: {payload}")
            response = requests.post(self.api_url, headers=headers, json=payload, stream=True)

            if response.status_code == 401:
                logger.error("❌ Unauthorized (401) - Check API Token and Headers.")
                return "❌ Unauthorized. Please check your API token."

            return self._process_streaming_response(response)
        finally:
            thinking.stop()

    def _clean_context(self, context: str) -> str:
        """Remove chunk references from the retrieved context"""
        import re
        # Remove any references like [CHUNK X - TYPE: XYZ]
        return re.sub(r"\[CHUNK \d+.*?\]", "", context).strip()


    def _process_streaming_response(self, response: requests.Response) -> str:
        """Process streaming or full JSON response from API."""
        full_response = []
        
        logger.info(f"📥 Response status: {response.status_code}")
        logger.info(f"📥 Response headers: {dict(response.headers)}")

        try:
            # Check if streaming based on response (your API returns streaming data)
            if response.status_code == 200 and (response.headers.get("content-type", "").startswith("text/plain") or "stream" in str(response.headers) or response.text.startswith("data:")):
                # Handle streaming response
                for line in response.iter_lines():
                    if not line:
                        continue

                    line_str = line.decode("utf-8").strip()
                    logger.debug(f"Stream line: {line_str[:200]}...")
                    
                    # Handle both SSE format and plain streaming
                    if line_str.startswith("data:"):
                        data_str = line_str[len("data:"):].strip()
                        
                        if data_str == "[DONE]":
                            break
                            
                        try:
                            data = json.loads(data_str)
                            content = ""
                            
                            # Handle streaming format from your API
                            if "choices" in data and len(data["choices"]) > 0:
                                choice = data["choices"][0]
                                # Try delta format first
                                if "delta" in choice and "content" in choice["delta"]:
                                    content = choice["delta"]["content"]
                                # Try direct message content
                                elif "message" in choice and "content" in choice["message"]:
                                    content = choice["message"]["content"]
                                # Try text field (some APIs use this)
                                elif "text" in choice:
                                    content = choice["text"]
                            
                            if content:
                                full_response.append(content)
                                
                        except json.JSONDecodeError as e:
                            logger.debug(f"Failed to parse JSON: {data_str[:100]}... Error: {e}")
                            # If it's not JSON, maybe it's raw text
                            if data_str and not data_str.startswith("{"):
                                full_response.append(data_str)

            else:
                # Handle non-streaming response
                try:
                    data = response.json()
                    logger.debug(f"Full response: {data}")
                    
                    if "choices" in data and len(data["choices"]) > 0:
                        message = data["choices"][0].get("message", {})
                        content = message.get("content", "")
                        if content:
                            full_response.append(content)
                    else:
                        # Fallback: try to get any text content
                        content = str(data)
                        full_response.append(content)
                        
                except Exception as e:
                    logger.error(f"Failed to parse JSON response: {e}")
                    # Try to get raw text
                    full_response.append(response.text)

        except Exception as e:
            logger.error(f"Error processing response: {e}")
            full_response.append(f"Error: {str(e)}")

        result = "".join(full_response).strip()
        logger.info(f"📤 Final response length: {len(result)}")
        return result
