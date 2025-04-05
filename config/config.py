import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# file path
PDF_FILE_PATH = os.getenv('PDF_FILE_PATH', 'data/input.pdf')
OUTPUT_FILE_PATH = os.getenv('OUTPUT_FILE_PATH', 'data/output.txt')
RULES_OUTPUT_PATH = os.getenv('RULES_OUTPUT_PATH', 'data/rules.json')

# model settings
MODEL_NAME = 'gemini-1.5-pro'

# processing settings
MAX_TOKENS = 2048
TEMPERATURE = 0.7

# neo4j configuration
NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password') 