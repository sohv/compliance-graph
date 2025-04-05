import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
import time

load_dotenv()

# Gemini API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=GOOGLE_API_KEY)

# initialize Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# JSON extraction prompt
json_extraction_prompt = PromptTemplate(
    input_variables=["document_text"],
    template="""
    Extract all financial rules from the given text and return them as structured JSON.

    Text:
    "{document_text}"

    Ensure the output follows this JSON format strictly:

    [
        {{
            "RuleID": "R001",
            "FullRule": "All transactions above $10,000 must be reported to FinCEN under the Bank Secrecy Act.",
            "Condition": "Transaction > $10,000",
            "Action": "Report to FinCEN",
            "Regulation": "Bank Secrecy Act (BSA)"
        }},
        {{
            "RuleID": "R002",
            "FullRule": "Customers attempting multiple failed logins within 5 minutes must trigger a fraud alert.",
            "Condition": "Multiple failed login attempts in 5 minutes",
            "Action": "Trigger fraud alert",
            "Regulation": "Cybersecurity Best Practices"
        }},
        {{
            "RuleID": "R003",
            "FullRule": "For loans, a minimum credit score of 650 is required.",
            "Condition": "Credit score < 650",
            "Action": "Reject loan application",
            "Regulation": "Lending Policy"
        }}
    ]

    - Extract **FullRule** from the text verbatim.
    - Identify the **Condition** (the situation where the rule applies).
    - Identify the **Action** (what needs to happen when the condition is met).
    - Identify the **Regulation** (if mentioned, otherwise return 'Company Policy').

    Do not include explanations or formatting outside this JSON format.
    """
)

def extract_financial_rules(text_document: str) -> list:
    """
    Extracts financial rules from a document using Gemini and outputs structured JSON.

    Args:
    - text_document (str): Input financial text containing rules.

    Returns:
    - list: Extracted rules in structured format.
    """

    # generate prompt text
    prompt_text = json_extraction_prompt.format(document_text=text_document)

    # run Gemini API
    response = model.generate_content(prompt_text)

    # parse response JSON safely
    try:
        json_start = response.text.find("[")
        json_end = response.text.rfind("]") + 1
        json_text = response.text[json_start:json_end]
        return json.loads(json_text)  # convert string to JSON
    except (json.JSONDecodeError, ValueError) as e:
        print(f"❌ JSON Parsing Error: {e}")
        print(f"🔍 Raw Output: {response.text}")
        return [] 

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    input_txt = os.path.join(script_dir, "..", "data", "output.txt")
    output_json = os.path.join(script_dir, "..", "data", "extracted_rules.json")
    
    if not os.path.exists(input_txt):
        print(f"Input file not found at: {input_txt}")
        print("Please run pdf_reader.py first to generate the output.txt file.")
        return
    
    with open(input_txt, 'r', encoding='utf-8') as f:
        financial_text = f.read()

    # text splitter
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    # split text into chunks
    text_chunks = text_splitter.split_text(financial_text)

    # process each chunk with delay
    all_extracted_rules = []
    for chunk in text_chunks:
        try:
            extracted_rules = extract_financial_rules(chunk)
            if extracted_rules:
                all_extracted_rules.extend(extracted_rules)  # append structured JSON output
            time.sleep(2)  # add delay
        except Exception as e:
            print(f"❌ Error processing chunk: {e}")

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(all_extracted_rules, f, indent=4)
    
    print(f"✅ Extracted rules have been saved to: {output_json}")

    full_rules = [rule["FullRule"] for rule in all_extracted_rules if "FullRule" in rule]

    # print the extracted full rules
    print("\nExtracted Full Rules:")
    for i, rule in enumerate(full_rules, 1):
        print(f"{i}. {rule}")

if __name__ == "__main__":
    main()
