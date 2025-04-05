import os
from neo4j import GraphDatabase
import sqlite3
from dotenv import load_dotenv
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = Path(script_dir).parent

load_dotenv(os.path.join(project_root, '.env'))

uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

if not all([uri, username, password]):
    print("Error: Neo4j connection details not found in .env file")
    print(f"Checking for .env file at: {os.path.join(project_root, '.env')}")
    print("Please make sure the .env file exists and contains NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD")
    exit(1)

try:
    driver = GraphDatabase.driver(uri, auth=(username, password))
    
    # test connection
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN count(n) as count")
        count = result.single()["count"]
        print(f"Number of nodes in DB: {count}")
    print("Successfully connected to Neo4j database!")
    
except Exception as e:
    print(f"Error connecting to Neo4j database: {e}")
    exit(1)