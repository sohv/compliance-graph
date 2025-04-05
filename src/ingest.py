'''
This script is used to ingest the extracted rules into the Neo4j database.
'''

import os
import json
from db.connection import driver

def create_knowledge_graph(rules):
    """
    Inserts financial rules into Neo4j as a knowledge graph.

    Args:
    - rules (list): Extracted financial rules in JSON format.
    """
    if not driver:
        print("No active Neo4j connection.")
        return

    with driver.session() as session:
        for rule in rules:
            session.run(
                """
                MERGE (r:Rule {id: $RuleID, full_text: $FullRule})
                MERGE (c:Condition {text: $Condition})
                MERGE (a:Action {text: $Action})
                MERGE (reg:Regulation {name: $Regulation})

                MERGE (r)-[:HAS_CONDITION]->(c)
                MERGE (r)-[:HAS_ACTION]->(a)
                MERGE (r)-[:BASED_ON]->(reg)
                """,
                RuleID=rule["RuleID"],
                FullRule=rule["FullRule"],
                Condition=rule["Condition"],
                Action=rule["Action"],
                Regulation=rule["Regulation"]
            )
    print("Financial Rules inserted into Neo4j Knowledge Graph!")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rules_json = os.path.join(script_dir, "..", "data", "extracted_rules.json")
    
    if not os.path.exists(rules_json):
        print(f"Extracted rules file not found at: {rules_json}")
        print("Please run extract_rules.py first to generate the extracted_rules.json file.")
        return
    
    with open(rules_json, 'r', encoding='utf-8') as f:
        all_extracted_rules = json.load(f)
    
    if not all_extracted_rules:
        print("No rules found in the extracted_rules.json file.")
        return

    # convert extracted rules into a knowledge graph
    create_knowledge_graph(all_extracted_rules)

if __name__ == "__main__":
    main()
