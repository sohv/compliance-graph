'''
Main script for checking transaction compliance.
'''

from rule_retrieve import RuleRetriever
from rule_check import RuleChecker

def print_results(results):
    """
    Prints the compliance check results in a formatted way.
    
    Args:
        results (dict): Dictionary containing compliance check results
    """
    print("\nTransaction Details:")
    print(f"Type: {results['transaction']['type']}")
    print(f"Amount: {results['transaction']['amount']}")
    print(f"Parties: {results['transaction']['parties']}")
    print(f"Description: {results['transaction']['description']}")
    
    print("\nCompliance Status:", results['compliance_status'])
    
    if results['violations']:
        print("\nViolations:")
        for violation in results['violations']:
            print(f"- Rule {violation['rule_id']}: {violation['details']}")
    
    if results['warnings']:
        print("\nWarnings:")
        for warning in results['warnings']:
            print(f"- Rule {warning['rule_id']}: {warning['details']}")
    
    if results['applied_rules']:
        print("\nApplied Rules:")
        for rule in results['applied_rules']:
            print(f"- Rule {rule['rule_id']}: {rule['details']}")

def main():
    """
    Main function to demonstrate the compliance checking process.
    """
    # Example transaction
    transaction = {
        "type": "payment",
        "amount": 15000,
        "parties": ["Company A", "Company B"],
        "description": "Monthly service fee",
        "date": "2024-03-15"
    }
    
    # Initialize retriever and checker
    retriever = RuleRetriever()
    checker = RuleChecker()
    
    # Get relevant rules
    rules = retriever.get_relevant_rules(transaction)
    
    # Check compliance
    results = checker.check_compliance(transaction, rules)
    
    # Print results
    print_results(results)

if __name__ == "__main__":
    main() 