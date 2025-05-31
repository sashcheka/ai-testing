import pytest
import json
from unittest.mock import patch, MagicMock
from .api_validator import ProductDataValidator, ValidationResult

@pytest.fixture
def mock_products():
    """Fixture providing sample product data for testing."""
    return [
        {
            "id": 1,
            "title": "Valid Product",
            "price": 19.99,
            "rating": {"rate": 4.5, "count": 120}
        },
        {
            "id": 2,
            "title": "",  # Empty title defect
            "price": 29.99,
            "rating": {"rate": 3.8, "count": 90}
        },
        {
            "id": 3,
            "title": "Invalid Price Product",
            "price": -10.00,  # Negative price defect
            "rating": {"rate": 4.2, "count": 150}
        },
        {
            "id": 4,
            "title": "Invalid Rating Product",
            "price": 39.99,
            "rating": {"rate": 5.5, "count": 200}  # Invalid rating defect
        }
    ]

@pytest.fixture
def validator():
    """Fixture providing a ProductDataValidator instance."""
    return ProductDataValidator()

def test_fetch_products_success(validator):
    """Test successful product fetching."""
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1, "title": "Test Product"}]
        mock_get.return_value = mock_response

        status_code, products = validator.fetch_products()
        assert status_code == 200
        assert len(products) == 1
        assert products[0]["title"] == "Test Product"

def test_fetch_products_failure(validator):
    """Test product fetching failure."""
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("API Error")
        
        with pytest.raises(Exception) as exc_info:
            validator.fetch_products()
        assert "Failed to fetch products" in str(exc_info.value)

def test_validate_product_valid(validator, mock_products):
    """Test validation of a valid product."""
    result = validator.validate_product(mock_products[0])
    assert isinstance(result, ValidationResult)
    assert result.product_id == 1
    assert len(result.defects) == 0

def test_validate_product_empty_title(validator, mock_products):
    """Test validation of a product with empty title."""
    result = validator.validate_product(mock_products[1])
    assert "empty_title" in result.defects
    assert validator.defects_report["defects_by_type"]["empty_title"] == 1

def test_validate_product_negative_price(validator, mock_products):
    """Test validation of a product with negative price."""
    result = validator.validate_product(mock_products[2])
    assert "negative_price" in result.defects
    assert validator.defects_report["defects_by_type"]["negative_price"] == 1

def test_validate_product_invalid_rating(validator, mock_products):
    """Test validation of a product with invalid rating."""
    result = validator.validate_product(mock_products[3])
    assert "invalid_rating" in result.defects
    assert validator.defects_report["defects_by_type"]["invalid_rating"] == 1

def test_validate_all_products(validator, mock_products):
    """Test validation of all products."""
    with patch.object(validator, 'fetch_products') as mock_fetch:
        mock_fetch.return_value = (200, mock_products)
        
        report = validator.validate_all_products()
        
        assert report["total_products"] == 4
        assert report["products_with_defects"] == 3
        assert len(report["defective_products"]) == 3
        assert report["defects_by_type"]["empty_title"] == 1
        assert report["defects_by_type"]["negative_price"] == 1
        assert report["defects_by_type"]["invalid_rating"] == 1

def test_save_report(validator, tmp_path):
    """Test saving the defects report."""
    # Create a temporary file path
    report_file = tmp_path / "test_report.json"
    
    # Add some test data to the report
    validator.defects_report["total_products"] = 10
    validator.defects_report["products_with_defects"] = 2
    
    # Save the report
    validator.save_report(str(report_file))
    
    # Verify the file was created and contains the correct data
    assert report_file.exists()
    with open(report_file) as f:
        saved_report = json.load(f)
        assert saved_report["total_products"] == 10
        assert saved_report["products_with_defects"] == 2

if __name__ == "__main__":
    pytest.main(["-v"]) 