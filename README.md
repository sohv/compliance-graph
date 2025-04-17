# Financial Compliance Using Knowledge Graphs

This **project prototype** checks for financial compliance of transactions by storing compliance rules in knowledge graphs and using 
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

## Evaluation

The system's performance in extracting and matching rules was evaluated with the following metrics:

| Metric | Value |
|--------|-------|
| Number of extracted rules | 25 |
| Number of rules in output.txt | 33 |
| Fully Recovered Rules | 21 (63.64%) |
| Partially Recovered Rules | 4 (12.12%) |
| Similar Rules | 5 (15.15%) |
| Missed Rules | 3 (9.09%) |
| Average Similarity | 0.8074 |
| Average Corrected Similarity | 0.7873 |
| Relative Excess Extracted Rules | 0.2000 |

These metrics indicate:
- Strong rule recovery rate with 63.64% fully recovered rules
- High average similarity (0.8074) suggesting good matching quality
- Low miss rate (9.09%) indicating effective rule extraction


## Why not RAG ?

I have implemented a semantic search-based rule system for financial rule retrieval in this project. This is how it works :
- Uses **SentenceTransformer** to convert word text into embeddings
- Compares the transaction with rules stored in knowledge graph using **cosine similarity**.
- Finds the semantically most similar rules to the transaction and returns the top k relevant rules.

By employing this method, we can find relevant rules even if wording is different and also handle variations in rule descriptions.

Why I chose semantic search over RAG is because :
- Compliance needs deterministic results - RAG used LLMs that are unpredictable and we can't risk hallucinations in financial decisions.
- Transparency - The compliance decisions must be 100% consistent, so we must show exactly what rules were applied.
- Cost and Performance - RAG requires LLM API call for every transaction, which results in higher latency and more costs in RAG systems.

## Limitations
- **Real-time Updates** - Financial Compliance rules evolve rapidly and are highly subject to change. This project focuses on static rules being fed into the model as real-time integration of rules would incur extra costs in addition to LLM API expenses.
- **Neo4j Scaling** -  The code written for Neo4j is not scalable for handling a large number of rules. My estimate is that the code can likely manage ~2000 financial rules in format **Rule-Action-Condition** stored in Neo4j database. More scalability means additional costs and further tuning of written code.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Note
If anyone is up for funding this project, please feel free to contact me through LinkedIn or through email. I plan to incorporate three following features to build an industry-ready prototype: 
1. An AI agent for real-time transaction compliance monitoring 
2. A real-time rule update agent that updates knowledge graphs dynamically with new rules and updates
3. Try out microservices cloud architecture for scalability.



