from app.calculations import BankAccount, InsufficientFunds, add, divide, multiply, subtract
import pytest

@pytest.fixture()
def zero_balance_bank_account():
    print("creating zero balance account")
    return BankAccount()

@pytest.fixture()
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected",[
    (2,4,6),
    (4,5,9),
    (8,2,11)
])
def test_add(num1, num2, expected):
    # sum = 
    # print("testing add function")
    assert add(5,8) == 13

def test_subtract():
    # sum = 
    # print("testing add function")
    assert subtract(3,1) == 2

def test_mul():
    # sum = 
    # print("testing add function")
    assert multiply(5,8) == 40

def test_div():
    # sum = 
    # print("testing add function")
    assert divide(8,4) == 2

def test_bank_set_initial_amount(bank_account):
    # bank_account = BankAccount(50)
    assert bank_account.balance == 50

def test_bank_default_amount(zero_balance_bank_account):
    # bank_account = BankAccount()
    print("Using zero bank balance")
    assert zero_balance_bank_account.balance == 0

def test_bank_deposit_amount(bank_account):
    # bank_account = BankAccount(10)
    bank_account.deposit(50)
    assert bank_account.balance == 100

def test_bank_withdraw_amount(bank_account):
    # bank_account = BankAccount(40)
    bank_account.withdraw(10)
    assert bank_account.balance == 40

def test_bank_collect_interest(bank_account):
    # bank_account = BankAccount(100)
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55


@pytest.mark.parametrize("deposited, withdrew, expected",[
    (400,100,340),
    (360,240,156),
    (730,40,763)
])
def test_bank_transaction(zero_balance_bank_account,deposited,withdrew,expected):
    zero_balance_bank_account.deposit(deposited)
    zero_balance_bank_account.collect_interest()
    zero_balance_bank_account.withdraw(withdrew)
    assert round(zero_balance_bank_account.balance) == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
      bank_account.withdraw(200)