import json
import requests
import os
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ValidationResult:
    """Class to store validation results for a product."""
    product_id: int
    defects: List[str]
    product_data: Dict[str, Any]

class ProductDataValidator:
    """Class to validate product data from the Fake Store API."""
    
    def __init__(self, api_url: str = "https://fakestoreapi.com/products"):
        self.api_url = api_url
        self.defects_report = {
            "timestamp": "",
            "total_products": 0,
            "products_with_defects": 0,
            "defects_by_type": {
                "empty_title": 0,
                "negative_price": 0,
                "invalid_rating": 0
            },
            "defective_products": []
        }

    def fetch_products(self) -> Tuple[int, List[Dict[str, Any]]]:
        """
        Fetch products from the API.
        Returns tuple of (status_code, products_list)
        """
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            return response.status_code, response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch products: {str(e)}") from e
        except Exception as e:
            raise Exception(f"Failed to fetch products: {str(e)}") from e

    def validate_product(self, product: Dict[str, Any]) -> ValidationResult:
        """
        Validate a single product for defects.
        Returns ValidationResult object containing any found defects.
        """
        defects = []
        product_id = product.get('id', 0)

        # Validate title
        if not product.get('title', '').strip():
            defects.append("empty_title")
            self.defects_report["defects_by_type"]["empty_title"] += 1

        # Validate price
        if product.get('price', 0) < 0:
            defects.append("negative_price")
            self.defects_report["defects_by_type"]["negative_price"] += 1

        # Validate rating
        rating = product.get('rating', {})
        if rating.get('rate', 0) > 5:
            defects.append("invalid_rating")
            self.defects_report["defects_by_type"]["invalid_rating"] += 1

        return ValidationResult(
            product_id=product_id,
            defects=defects,
            product_data=product
        )

    def validate_all_products(self) -> Dict[str, Any]:
        """
        Validate all products and generate a defects report.
        Returns the complete defects report.
        """
        status_code, products = self.fetch_products()
        
        if status_code != 200:
            raise Exception(f"API returned unexpected status code: {status_code}")

        self.defects_report["timestamp"] = datetime.now().isoformat()
        self.defects_report["total_products"] = len(products)

        for product in products:
            validation_result = self.validate_product(product)
            if validation_result.defects:
                self.defects_report["products_with_defects"] += 1
                self.defects_report["defective_products"].append({
                    "id": validation_result.product_id,
                    "defects": validation_result.defects,
                    "data": validation_result.product_data
                })

        return self.defects_report

    def save_report(self, filename: str = "defects_report.json") -> None:
        """
        Save the defects report to a JSON file.
        """
        try:
            # Get the absolute path to the results directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            results_dir = os.path.join(os.path.dirname(current_dir), "results")
            os.makedirs(results_dir, exist_ok=True)
            
            filepath = os.path.join(results_dir, filename)
            with open(filepath, 'w') as f:
                json.dump(self.defects_report, f, indent=2)
        except IOError as e:
            raise Exception(f"Failed to save report: {str(e)}")

def main():
    """Main function to run the validation process."""
    validator = ProductDataValidator()
    try:
        report = validator.validate_all_products()
        validator.save_report()
        print(f"Validation complete. Found {report['products_with_defects']} products with defects.")
        print(f"Report saved to results/defects_report.json")
    except Exception as e:
        print(f"Error during validation: {str(e)}")

if __name__ == "__main__":
    main()