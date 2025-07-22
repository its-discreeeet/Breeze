"""Gemini API proxy for calling Google's AI models."""

import os
import json
from typing import Optional, Dict, Any

try:
    import google.generativeai as genai
except ImportError:
    genai = None


class GeminiAPIProxy:
    """Proxy class for interacting with Google's Gemini API."""
    
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        """Initialize the Gemini API proxy."""
        self.model_name = model_name
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = None
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        if genai is None:
            raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")
        
        self._initialize_model()
    
    def _initialize_model(self) -> None:
        """Initialize the Gemini model."""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Gemini model: {e}")
    
    def call_gemini(
        self, 
        prompt: str, 
        verbose: bool = False,
        temperature: float = 0.3,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Call the Gemini API with the given prompt.
        
        Args:
            prompt: The input prompt for the model
            verbose: Whether to print debug information
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            The model's response as a string
        """
        if not self.model:
            raise RuntimeError("Gemini model not initialized")
        
        try:
            if verbose:
                print(f"Calling Gemini model: {self.model_name}")
                print(f"Prompt length: {len(prompt)} characters")
            
            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
            
            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            if response.candidates and response.candidates[0].content:
                result = response.candidates[0].content.parts[0].text
                
                if verbose:
                    print(f"Response length: {len(result)} characters")
                
                return result
            else:
                return "No response generated from Gemini API"
                
        except Exception as e:
            if verbose:
                print(f"Gemini API error: {e}")
            raise RuntimeError(f"Gemini API call failed: {e}")
    
    def call_gemini_with_context(
        self, 
        system_prompt: str,
        user_prompt: str,
        verbose: bool = False
    ) -> str:
        """
        Call Gemini with separate system and user prompts.
        
        Args:
            system_prompt: System/context prompt
            user_prompt: User's actual prompt
            verbose: Whether to print debug information
            
        Returns:
            The model's response as a string
        """
        combined_prompt = f"{system_prompt}\n\nUser: {user_prompt}\n\nAssistant:"
        return self.call_gemini(combined_prompt, verbose=verbose)
    
    def is_available(self) -> bool:
        """Check if the Gemini API is available and configured."""
        return self.model is not None and self.api_key is not None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        return {
            "model_name": self.model_name,
            "api_key_set": bool(self.api_key),
            "initialized": bool(self.model)
        }
