'''
This script is used to search the Neo4j database for financial rules that match the inputted keyword.
'''

import os
from db.connection import driver

def get_rules_by_keyword(keyword):
    """
    Retrieves all rules containing a specific keyword in FullRule, Condition, or Action.

    Args:
    - keyword (str): The word to search for in the rules.

    Returns:
    - list of dict: A list of rule details.
    """
    if not driver:
        print("No active Neo4j connection.")
        return []

    with driver.session() as session:
        result = session.run(
            """
            MATCH (r:Rule)-[:HAS_CONDITION]->(c:Condition),
                  (r)-[:HAS_ACTION]->(a),
                  (r)-[:BASED_ON]->(reg:Regulation)
            WHERE toLower(r.full_text) CONTAINS toLower($Keyword)
               OR toLower(c.text) CONTAINS toLower($Keyword)
               OR toLower(a.text) CONTAINS toLower($Keyword)
            RETURN r.id AS RuleID, r.full_text AS FullRule,
                   c.text AS Condition, a.text AS Action, reg.name AS Regulation;
            """,
            Keyword=keyword
        )

        rules = []
        for record in result:
            rules.append({
                "RuleID": record["RuleID"],
                "FullRule": record["FullRule"],
                "Condition": record["Condition"],
                "Action": record["Action"],
                "Regulation": record["Regulation"],
            })

        if not rules:
            print(f"No rules found containing '{keyword}'.")

        return rules

def main():
    keyword = "transaction"
    rules = get_rules_by_keyword(keyword)
    
    if rules:
        print(f"Found {len(rules)} rules containing '{keyword}':")
        for rule in rules:
            print(f"\nRule ID: {rule['RuleID']}")
            print(f"Full Rule: {rule['FullRule']}")
            print(f"Condition: {rule['Condition']}")
            print(f"Action: {rule['Action']}")
            print(f"Regulation: {rule['Regulation']}")

if __name__ == "__main__":
    main()
