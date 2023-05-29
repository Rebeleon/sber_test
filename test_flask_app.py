import pytest
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_valid_deposit_request(client):
    # a valid deposit request
    deposit_request = {
        'date': '31.01.2021',
        'periods': 7,
        'amount': 10000,
        'rate': 6
    }

    response = client.post('/calculate_deposit', json=deposit_request)
    assert response.status_code == 200

    # check that the response is correct
    expected_response = {
        '31.01.2021': 10050.00,
        '28.02.2021': 10100.25,
        '31.03.2021': 10150.75,
        '30.04.2021': 10201.51,
        '31.05.2021': 10252.51,
        '30.06.2021': 10303.78,
        '31.07.2021': 10355.29
    }

    assert response.json == expected_response


def test_invalid_deposit_request(client):
    # an invalid deposit request
    deposit_request = {
        'date': '01/01/2022',
        'periods': 70,
        'amount': 5000,
        'rate': 10
    }

    response = client.post('/calculate_deposit', json=deposit_request)
    assert response.status_code == 400

    # check that the error message is correct
    expected_error = {'error': {
        'date': 'Date must be in DD.MM.YYYY format',
        'periods': 'Periods must be between 1 and 60',
        'amount': 'Amount must be between 10000 and 3000000',
        'rate': 'Rate must be between 1 and 8'
    }}

    assert response.json == expected_error
