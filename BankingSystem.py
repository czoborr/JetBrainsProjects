# Write your code here
from random import randint
import sqlite3

database = 'card.s3db'
conn = sqlite3.connect(database)
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, '
            'pin TEXT, balance INTEGER DEFAULT 0);')


class Card:
    def __init__(self):
        self.number = luhn(9)
        self.PIN = str(random_generator(4))
        self.balance = 0


def random_generator(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def multi(lst):
    res = list(lst)
    for i in range(len(res)):
        if i % 2 == 0:
            res[i] = res[i] * 2
    return res


def minus(lst):
    for i in range(0, len(lst)):
        if lst[i] > 9:
            lst[i] = lst[i] - 9
        else:
            lst[i] = lst[i]
    return lst


def luhn(n):
    iin = str(400000)
    a = list(map(int, iin + str(random_generator(n))))
    b = multi(a)
    b = minus(b)
    checksum = 10 - (sum(b) % 10)
    if checksum == 10:
        checksum = 0
    a = a + [checksum]
    res = int("".join(map(str, a)))
    return str(res)


def check_luhn(n):
    a = list(map(int, n))
    to_check = a[-1]
    b = multi(a[:-1])
    b = minus(b)
    checksum = 10 - (sum(b) % 10)
    if checksum == 10:
        checksum = 0
    return checksum == to_check


def create_account():
    new_card = Card()
    cur.execute("INSERT INTO card (number, pin) VALUES (?,?)", (new_card.number, new_card.PIN))
    conn.commit()
    print("Your card has been created\nYour card number:\n{}\nYour card PIN:\n{}".format(new_card.number, new_card.PIN))


def close_account(log_account):
    cur.execute("SELECT balance FROM card WHERE number=?", (log_account,))
    cur.execute("DELETE FROM card WHERE number=?", (log_account,))
    conn.commit()
    print('The account has been closed!\n')


def print_balance(log_account):
    cur.execute("SELECT balance FROM card WHERE number=?", (log_account,))
    balance = (cur.fetchall())[0][0]
    print(f'Balance: {balance}\n')


def enter_income(log_account):
    print('Enter income:')
    inc = int(input())
    cur.execute("SELECT balance FROM card WHERE number=?", (log_account,))
    new_balance = (cur.fetchall())[0][0] + inc
    cur.execute("UPDATE card SET balance = ? WHERE number=?", (new_balance, log_account,))
    conn.commit()
    print('Income was added!')


def manage_account(number):
    while True:
        print("1. Balance\n"
              "2. Add income\n"
              "3. Transfer\n"
              "4. Close Account\n"
              "5. Log out\n"
              "0. Exit")

        choice = int(input())

        if choice == 0:
            print("Bye!")
            break

        elif choice == 1:
            print_balance(entered_number)

        elif choice == 2:
            enter_income(entered_number)
            continue

        elif choice == 4:
            close_account(entered_number)

        elif choice == 5:
            print("You have successfully logged out!")
            continue

        else:
            print("Enter card number:")
            transfer_number = input()
            cur.execute("SELECT number FROM card")
            accounts = (cur.fetchall())
            accounts = [i[0] for i in accounts]

            if transfer_number == number:
                print("You can't transfer money to the same account!")

            elif not check_luhn(transfer_number):
                print('Probably you made a mistake in the card number. Please try again!')

            elif transfer_number not in accounts:
                print("Such a card does not exist.")

            else:
                print("Enter how much money you want to transfer:")
                transfer_money = int(input())
                cur.execute("SELECT balance FROM card WHERE number = number;")
                balance = (cur.fetchall())[0][0]

                if (balance - transfer_money) <= 0:
                    print('Not enough money!')

                else:
                    new_balance = balance - transfer_money
                    new_balance2 = (cur.fetchall())[0][0] + transfer_money

                    cur.execute("UPDATE card SET balance = ? WHERE number = number;", (new_balance, ))
                    conn.commit()
                    cur.execute("SELECT balance FROM card WHERE number = number;")
                    cur.execute("UPDATE card SET balance = ? WHERE number = number", (new_balance2, ))
                    conn.commit()

                    print('Success!\n')



while True:
    print("1. Create an account\n2. Log into account\n0. Exit")
    choice = input()

    if choice == "1":
        create_account()
        continue

    elif choice == "0":
        print("Bye!")
        break

    elif choice == "2":
        print("Enter your card number:")
        entered_number = input()
        print("Enter your PIN:")
        entered_pin = input()
        cur.execute("SELECT number, pin  FROM card WHERE number=?", (entered_number,))
        records = cur.fetchall()

        if not records:
            print("Wrong card number or PIN!")

        elif entered_number == records[0][0] and entered_pin == records[0][1]:
            print("You have successfully logged in!\n")
            while True:
                manage_account(entered_number)

        else:
            print("Wrong card number or PIN!")

    else:
        continue
conn.close()