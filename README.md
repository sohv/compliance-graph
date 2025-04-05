# Financial Compliance Using AI

This project checks for financial compliance of transactions by storing compliance rules in knowledge graphs and using them to assess transaction adherence.


## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following variables:
```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

Run the main script:
```bash
python src/main.py
```

