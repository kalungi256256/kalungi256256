import pytest
from pytest import approx
from finance_tracker import (
    load_transactions,
    calculate_monthly_totals,
    generate_category_breakdown,
    format_currency
)


@pytest.fixture
def sample_transactions():
    return [
        {"Date": "2025-01-05", "Description": "Salary Payment", "Amount": 1500.00, "Type": "Income", "Category": "Salary"},

        {"Date": "2025-01-08", "Description": "Rent Payment", "Amount": -500.00, "Type": "Expense", "Category": "Housing"},

        {"Date": "2025-01-10", "Description": "Supermarket Purchase", "Amount": -120.50, "Type": "Expense", "Category": "Groceries"},
        
        {"Date": "2025-01-15", "Description": "Electricity Bill", "Amount": -60.00, "Type": "Expense", "Category": "Utilities"}
    ]


def test_load_transactions(tmp_path):
    file = tmp_path / "test.csv"
    file.write_text(
        "Date,Description,Amount,Type,Category\n"
        "2025-01-01,Test Income,100.0,Income,Salary\n"
        "2025-01-02,Test Expense,-50.0,Expense,Groceries\n"
    )
    data = load_transactions(file)
    assert len(data) == 2
    assert data[0]["Amount"] == approx(100.0)
    assert data[1]["Amount"] == approx(-50.0)


def test_calculate_monthly_totals(sample_transactions):

    totals = calculate_monthly_totals(sample_transactions)

    assert "2025-01" in totals

    assert totals["2025-01"]["Income"] == approx(1500.00)

    assert totals["2025-01"]["Expense"] == approx(680.50)


def test_generate_category_breakdown(sample_transactions):
    breakdown = generate_category_breakdown(sample_transactions)

    assert breakdown["Housing"] == approx(500.00)

    assert breakdown["Groceries"] == approx(120.50)

    assert breakdown["Utilities"] == approx(60.00)


def test_most_expensive_transaction(sample_transactions):

    expenses_only = [t for t in sample_transactions if t["Type"] == "Expense"]

    most_expensive = max(expenses_only, key=lambda x: abs(x["Amount"]))

    assert most_expensive["Description"] == "Rent Payment"

    assert most_expensive["Amount"] == approx(-500.00)


def test_top_spending_category(sample_transactions):

    category_totals = generate_category_breakdown(sample_transactions)

    top_category = max(category_totals.items(), key=lambda x: x[1])

    assert top_category[0] == "Housing"

    assert top_category[1] == approx(500.00)


def test_format_currency():

    assert format_currency(1500) == "$1,500.00"

    assert format_currency(0) == "$0.00"

pytest.main(["-v", "--tb=line", "-rN", __file__])

