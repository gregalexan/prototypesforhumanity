import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ai_check_legality(user_question: str, country: str = "Greece") -> str:
    """
    Calls Azure OpenAI to determine whether an action is legal or illegal in a specific country.
    The AI should respond YES or NO, and cite the applicable law or regulation.
    """
    load_dotenv()

    endpoint = os.environ.get("ENDPOINT")
    deployment = "gpt-4.1"
    search_endpoint = os.environ.get("SEARCH_ENDPOINT")
    search_index = os.environ.get("SEARCH_INDEX_NAME")
    search_key = os.environ.get("SEARCH_KEY")
    api_key = os.environ.get("AZURE_KEY")

    client = AzureOpenAI(
        api_key=api_key,
        azure_endpoint=endpoint,
        api_version="2024-05-01-preview",
    )

    system_prompt = f"""
    You are a legal expert specialized in the laws of {country}. 
    When a user asks whether something is legal or illegal, you must:

    - Respond ONLY with "YES" or "NO".
    - Then cite the specific **law, regulation, or legal precedent** that justifies your answer.
    - If there are exceptions or conditions, mention them **after** the main YES/NO judgment.
    - Do NOT fabricate laws—only refer to actual legal data found in your knowledge or connected search index.
    - If no clear legal conclusion is possible, say "Cannot determine with available information" and explain why.

    Respond in the language you were spoken.
    """

    messages = [
        {"role": "system", "content": system_prompt.strip()},
        {"role": "user", "content": f"Ερώτηση: {user_question.strip()}"},
    ]

    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=messages,
            extra_body={
                "data_sources": [
                    {
                        "type": "azure_search",
                        "parameters": {
                            "endpoint": search_endpoint,
                            "index_name": search_index,
                            "authentication": {"type": "api_key", "key": search_key},
                        },
                    }
                ]
            },
            temperature=0,
            max_tokens=1200,
        )

        reply = response.choices[0].message.content.strip()
        logger.info(f"AI response:\n{reply}")
        return reply

    except Exception as e:
        logger.error(f"Error during Azure AI call: {e}")
        return f"Error: {e}"


if __name__ == "__main__":
    # Example usage
    question = "Can I record someone using a camera in my apartment without their consent?"
    country = "Greece"
    answer = ai_check_legality(question, country)
    print(answer)
