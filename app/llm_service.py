import openai
import os
from typing import Dict, List
from dotenv import load_dotenv
import json
import re

load_dotenv()

class LLMCodeReviewer:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def analyze_code(self, filename: str, content: str) -> Dict:
        """
        Analyze code using OpenAI GPT-4 for code review
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
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer with extensive experience in software development best practices."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
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
