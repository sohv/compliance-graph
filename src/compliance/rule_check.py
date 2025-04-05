'''
script to check transaction compliance against rules.
'''

import re

class RuleChecker:
    def __init__(self):
        pass
    
    def parse_amount(self, amount_str):
        """
        parse a string containing a currency amount into a float.
        """
        # Remove currency symbols and commas
        cleaned = re.sub(r'[^\d.]', '', amount_str)
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
    
    def check_amount_rule(self, amount, condition):
        """
        check if an amount complies with a condition.
        """
        threshold_match = re.search(r'[<>]\s*[\$]?\s*[\d,]+', condition)
        if not threshold_match:
            return "WARNING", "Could not parse amount threshold"
            
        threshold_str = threshold_match.group()
        threshold = self.parse_amount(threshold_str)
        
        if ">" in threshold_str and amount > threshold:
            return "FAIL", f"Amount {amount} exceeds threshold {threshold}"
        elif "<" in threshold_str and amount < threshold:
            return "FAIL", f"Amount {amount} is below threshold {threshold}"
        else:
            return "PASS", "Rule check passed"
    
    def check_rule(self, transaction_details, rule):
        """
        check if a transaction complies with a specific rule.
        """
        rule_result = {
            "rule_id": rule["RuleID"],
            "condition": rule["Condition"],
            "action": rule["Action"],
            "regulation": rule["Regulation"],
            "status": "PASS",
            "details": "Rule check passed"
        }
        
        # Check amount-based rules
        amount = transaction_details.get("amount", 0)
        condition = rule["Condition"].lower()
        
        if "amount" in condition:
            status, details = self.check_amount_rule(amount, condition)
            rule_result["status"] = status
            rule_result["details"] = details
        
        # note: add more checks here
        
        return rule_result
    
    def check_compliance(self, transaction_details, rules):
        """
        Checks if a transaction complies with a set of rules.
        
        Args:
            transaction_details (dict): Transaction information
            rules (list): List of rules to check against
            
        Returns:
            dict: Compliance check results
        """
        compliance_results = {
            "transaction": transaction_details,
            "compliance_status": "COMPLIANT",
            "violations": [],
            "warnings": [],
            "applied_rules": []
        }
        
        for rule in rules:
            rule_result = self.check_rule(transaction_details, rule)
            
            if rule_result["status"] == "FAIL":
                compliance_results["compliance_status"] = "NON-COMPLIANT"
                compliance_results["violations"].append(rule_result)
            elif rule_result["status"] == "WARNING":
                compliance_results["warnings"].append(rule_result)
            else:
                compliance_results["applied_rules"].append(rule_result)
        
        return compliance_results 