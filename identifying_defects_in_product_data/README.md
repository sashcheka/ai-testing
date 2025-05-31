# API Product Data Validation

This project implements automated tests to validate product data from the Fake Store API (https://fakestoreapi.com/products) and identify potential defects in the data.

## Project Overview

The application performs automated validation of product data by checking:
- Server response status (expected 200)
- Product data integrity:
  - Product title (must not be empty)
  - Product price (must not be negative)
  - Product rating (must not exceed 5)

## Project Structure

```
identifying defects in product data/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── api_validator.py
│   └── test_validator.py
└── results/
    └── defects_report.json
```

## Setup and Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
.\venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the tests using:
```bash
python -m pytest src/test_validator.py -v
```

**To validate real API data and generate a defects report:**
```bash
python src/api_validator.py
```

The validation results and identified defects will be saved in `results/defects_report.json`.

## Test Cases

1. Server Response Validation
   - Verify HTTP status code is 200
   - Confirm response is valid JSON

2. Product Data Validation
   - Title validation (non-empty)
   - Price validation (non-negative)
   - Rating validation (≤ 5)

## Output

The application generates a JSON report containing:
- List of products with defects
- Type of defect for each product
- Summary statistics of defects found

## Dependencies

- Python 3.8+
- requests
- pytest
- pytest-html (for HTML reports) 