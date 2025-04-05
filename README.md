# Financial Compliance Using Knowledge Graphs

This project checks for financial compliance of transactions by storing compliance rules in knowledge graphs and using 
them to assess transaction adherence.

## Overview

This project implements a comprehensive solution for:
- Extracting compliance rules from financial documents
- Storing rules in a Neo4j knowledge graph
- Retrieving relevant rules using semantic similarity
- Validating transactions against compliance rules
- Evaluating rule matching performance.

## Project Structure

```
src/
├── compliance/           
│   ├── rule_retrieve.py 
│   ├── rule_check.py    
│   └── check_compliance.py 
├── db/                  
│   └── connection.py    
└── evaluate_rules.py 
|__ extract_rules.py
|__ ingest.py
|__ read_pdf.py
|__ search_rules.py

config/
|-- config.py

data/
|--docs/
|--evaluation_rules.json
|--extracted_rules.json
|--output.txt
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sohv/compliance-graph.git
cd compliance-graph
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with:
```
GOOGLE_API_KEY= your_api_key
NEO4J_URI=your_neo4j_uri
NEO4J_USERNAME=your_username
NEO4J_PASSWORD=your_password
```

## Usage

1. **Extract Rules**:
```bash
python -m src.extract_rules
```

2. **Ingest Rules into Neo4j**:
```bash
python -m src.ingest
```

3. **Check Compliance**:
```bash
python -m src.compliance.check_compliance
```

4. **Evaluate Performance**:
```bash
python -m src.evaluate_rules
```

## Technical Details

- **NLP Model**: SentenceTransformer ('all-MiniLM-L6-v2')
- **Database**: Neo4j
- **Similarity Metric**: Cosine Similarity
- **Rule Preprocessing**: 
  - Stop word removal
  - Number/date standardization
  - Special character handling

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

