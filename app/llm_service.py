import openai
import os
from typing import Dict, List
from dotenv import load_dotenv
import json
import re

load_dotenv()

class LLMCodeReviewer:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "your_openai_api_key_here":
            self.client = openai.OpenAI(api_key=api_key)
            self.api_available = True
        else:
            self.client = None
            self.api_available = False
    
    def analyze_code(self, filename: str, content: str) -> Dict:
        """
        Analyze code using OpenAI GPT for code review
        """
        prompt = f"""
        Please review the following code file "{filename}" for readability, modularity, and potential bugs. 
        Provide a comprehensive analysis with specific improvement suggestions.

        Code to review:
        ```{self._get_file_extension(filename)}
        {content}
        ```

        Please provide your analysis in the following JSON format:
        {{
            "report": "Detailed analysis of the code...",
            "scores": {{
                "readability_score": 0.0-10.0,
                "modularity_score": 0.0-10.0,
                "bug_risk_score": 0.0-10.0,
                "overall_score": 0.0-10.0
            }},
            "suggestions": [
                "Specific improvement suggestion 1",
                "Specific improvement suggestion 2",
                "..."
            ]
        }}

        Focus on:
        1. Code readability and clarity
        2. Modularity and separation of concerns
        3. Potential bugs and edge cases
        4. Best practices and conventions
        5. Performance considerations
        6. Security implications

        Provide actionable, specific suggestions for improvement.
        """
        
        try:
            # Check if OpenAI API key is available
            if not self.api_available:
                return self._create_demo_response(filename, content)
            
            # Try different models in order of preference
            models_to_try = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]
            response = None
            
            for model in models_to_try:
                try:
                    response = self.client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": "You are an expert code reviewer with extensive experience in software development best practices."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.3,
                        max_tokens=2000
                    )
                    break  # If successful, break out of the loop
                except Exception as model_error:
                    if "insufficient_quota" in str(model_error) or "quota" in str(model_error):
                        return self._create_demo_response(filename, content)
                    elif "model_not_found" in str(model_error) or "does not exist" in str(model_error):
                        continue  # Try next model
                    else:
                        raise model_error  # Re-raise if it's a different error
            
            if response is None:
                return self._create_demo_response(filename, content)
            
            content = response.choices[0].message.content
            
            # Try to extract JSON from the response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                # Fallback if JSON parsing fails
                return self._create_fallback_response(content)
                
        except Exception as e:
            # If OpenAI fails, fall back to demo mode
            if "quota" in str(e).lower() or "limit" in str(e).lower():
                return self._create_demo_response(filename, content)
            return self._create_error_response(str(e))
    
    def _get_file_extension(self, filename: str) -> str:
        """Extract file extension for syntax highlighting"""
        return filename.split('.')[-1] if '.' in filename else 'text'
    
    def _create_fallback_response(self, content: str) -> Dict:
        """Create a fallback response when JSON parsing fails"""
        return {
            "report": content,
            "scores": {
                "readability_score": 7.0,
                "modularity_score": 7.0,
                "bug_risk_score": 5.0,
                "overall_score": 6.5
            },
            "suggestions": [
                "Review the detailed analysis above for specific improvement suggestions"
            ]
        }
    
    def _create_demo_response(self, filename: str, content: str) -> Dict:
        """Create a demo response when API is not available"""
        lines = content.split('\n')
        line_count = len(lines)
        
        # Simple analysis based on code characteristics
        readability_score = min(8.0, max(3.0, 10.0 - (line_count / 20)))
        modularity_score = min(8.0, max(3.0, 10.0 - (line_count / 15)))
        bug_risk_score = min(7.0, max(2.0, 10.0 - (line_count / 25)))
        overall_score = (readability_score + modularity_score + bug_risk_score) / 3
        
        return {
            "report": f"Demo Analysis for {filename}:\n\nThis is a demo analysis since your OpenAI API key is not configured or quota has been exceeded. The code appears to be {line_count} lines long. For a real AI-powered analysis, please add your OpenAI API key to the .env file.\n\nKey observations:\n- Code length: {line_count} lines\n- File type: {filename.split('.')[-1] if '.' in filename else 'unknown'}\n- This is a placeholder analysis",
            "scores": {
                "readability_score": round(readability_score, 1),
                "modularity_score": round(modularity_score, 1),
                "bug_risk_score": round(bug_risk_score, 1),
                "overall_score": round(overall_score, 1)
            },
            "suggestions": [
                "Add your OpenAI API key to .env file for real AI analysis",
                "Consider breaking down large functions into smaller ones",
                "Add comments and documentation for better readability",
                "Review error handling and edge cases",
                "This is a demo - get real analysis with OpenAI API key"
            ]
        }
    
    def _create_error_response(self, error: str) -> Dict:
        """Create an error response when LLM call fails"""
        return {
            "report": f"Error analyzing code: {error}",
            "scores": {
                "readability_score": 0.0,
                "modularity_score": 0.0,
                "bug_risk_score": 0.0,
                "overall_score": 0.0
            },
            "suggestions": [
                "Please check your OpenAI API key and try again"
            ]
        }