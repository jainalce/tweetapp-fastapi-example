import pytest
from app.calculations import add,subtract,multiply,divide,BankAccount

@pytest.fixture
def zero_bank_account():
   return BankAccount()

@pytest.fixture
def bank_account():
   return BankAccount(50)


@pytest.mark.parametrize("num1,num2,expected",[(3,2,5),(10,20,30),(100,200,300)])
def test_add(num1,num2,expected):
  assert add(num1,num2) == expected
  
def test_subtract():
   assert subtract(9,5) == 4

def test_multipy():
   assert multiply(5,6) == 30

def test_divide():
   assert divide(10,2) == 5


def test_bank_set_initial_amount(bank_account):
   assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
   assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
   bank_account.withdraw(20)
   assert bank_account.balance == 30

def test_bank_deposit(bank_account):
   bank_account.deposit(30)
   assert bank_account.balance == 80

def test_bank_collect_interest(bank_account):
   bank_account.collect_interest()
   assert round(bank_account.balance,6) == 55

@pytest.mark.parametrize("deposited,withdraw,expected",[(50,20,30),(500,400,100),(500,475,25)])
def test_bank_transaction(zero_bank_account,deposited,withdraw,expected):
   zero_bank_account.deposit(deposited)
   zero_bank_account.withdraw(withdraw)
   assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
   with pytest.raises(Exception):
      bank_account.withdraw(200)