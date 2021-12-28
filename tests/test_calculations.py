from app.calculations import BankAccount, InsufficientFunds
import pytest


@pytest.fixture
def bank_account_50():
    return BankAccount(50)


def test_insufficient_funds(bank_account_50):
    with pytest.raises(InsufficientFunds):
        bank_account_50.withdraw(100)
