'''
script to retrieve  relevant rules from the Knowledge Graph using semantic similarity.
'''
import os
import sys
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.connection import driver

class RuleRetriever:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def _get_all_rules(self):
        """Retrieves all rules from the Knowledge Graph."""
        with driver.session() as session:
            result = session.run("""
                MATCH (r:Rule)-[:HAS_CONDITION]->(c:Condition),
                      (r)-[:HAS_ACTION]->(a:Action),
                      (r)-[:BASED_ON]->(reg:Regulation)
                RETURN r.id as RuleID, r.full_text as FullRule,
                       c.text as Condition, a.text as Action,
                       reg.name as Regulation
            """)
            
            rules = []
            for record in result:
                rules.append({
                    "RuleID": record["RuleID"],
                    "FullRule": record["FullRule"],
                    "Condition": record["Condition"],
                    "Action": record["Action"],
                    "Regulation": record["Regulation"]
                })
            return rules
    
    def get_relevant_rules(self, transaction_details, top_k=5):
        """
        Retrieves relevant rules based on transaction details.
        
        Args:
            transaction_details (dict): Dictionary containing transaction information
            top_k (int): Number of most relevant rules to return
            
        Returns:
            list: List of relevant rules
        """
        # Convert transaction details to searchable text
        search_text = f"Transaction type: {transaction_details.get('type', '')} "
        search_text += f"Amount: {transaction_details.get('amount', '')} "
        search_text += f"Parties: {transaction_details.get('parties', '')} "
        search_text += f"Description: {transaction_details.get('description', '')}"
        
        # Get embedding for search text
        search_embedding = self.model.encode([search_text])[0]
        
        # Get all rules and their embeddings
        rules = self._get_all_rules()
        rule_texts = [rule["FullRule"] for rule in rules]
        rule_embeddings = self.model.encode(rule_texts)
        
        # Calculate similarities
        similarities = cosine_similarity([search_embedding], rule_embeddings)[0]
        
        # Get top k most relevant rules
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        relevant_rules = [rules[i] for i in top_indices]
        
        return relevant_rules 