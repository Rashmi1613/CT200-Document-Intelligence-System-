import json

import google.generativeai as genai


class LLMService:

    def __init__(self, api_key):

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

    # -----------------------------------------
    # Prompt
    # -----------------------------------------

    def build_prompt(self, context):

        return f"""
You are an experienced QA Engineer.

Using ONLY the document below, generate exactly 3 to 5 QA test case ideas.

Return ONLY valid JSON in the following format.

{{
  "test_cases":[
    {{
      "title":"...",
      "description":"...",
      "expected_result":"..."
    }}
  ]
}}

Document:

{context}
"""

    # -----------------------------------------
    # Generate
    # -----------------------------------------

    def generate(self, context):

        prompt = self.build_prompt(context)

        try:

            response = self.model.generate_content(prompt)

            raw_response = response.text.strip()

        except Exception as e:

            return {
                "status": "FAILED",
                "prompt": prompt,
                "response": str(e),
                "parsed": None
            }

        try:

            parsed = json.loads(raw_response)

            if "test_cases" not in parsed:
                raise ValueError()

            return {

                "status": "SUCCESS",

                "prompt": prompt,

                "response": raw_response,

                "parsed": parsed

            }

        except Exception:

            return {

                "status": "INVALID_RESPONSE",

                "prompt": prompt,

                "response": raw_response,

                "parsed": None

            }