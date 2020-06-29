# Write your code here
import random
import sqlite3

count = 0


def check_luh(number):
    last_digit = number[-1]
    number = number[0:15]
    numbers = [int(x) for x in number]
    numbers = [x * 2 if (i + 1) % 2 != 0 else x for i, x in enumerate(numbers)]
    numbers = [x - 9 if x > 9 else x for x in numbers]
    total = sum(numbers)
    if (total + int(last_digit)) % 10 == 0:
        return True
    else:
        return False


def create_account():
    global count
    count += 1
    pin = ""
    for i in range(4):
        pin += str(random.randint(0, 9))
    card_number = "400000"
    total = 0
    checksum = 0
    for i in range(9):
        card_number += str(random.randint(0, 9))
    numbers = [int(x) for x in card_number]
    numbers = [x * 2 if (i + 1) % 2 != 0 else x for i, x in enumerate(numbers)]
    numbers = [x - 9 if x > 9 else x for x in numbers]
    total = sum(numbers)
    for i in range(0, 10):
        if (total + i) % 10 == 0:
            checksum = i
            break
    card_number += str(checksum)
    conn.execute("INSERT INTO card (id,number,pin,balance) \
          VALUES ({}, {}, {}, 0)".format(count, card_number, pin, ));
    conn.commit()
    print("\nYour card has been created")
    print("Your card number:")
    print(card_number)
    print("Your card PIN:")
    print(pin + "\n")


def update(card1):
    print("\nEnter income:")
    amount = int(input())
    conn.execute("UPDATE card SET balance = balance + {} WHERE number = {}".format(amount, card1))
    conn.commit()
    print("Income was added!")


def transfer(card_number, balance):
    print("Transfer")
    print("Enter card number:")
    new_card = input()
    try:
        new_status = conn.execute("SELECT * FROM card WHERE number = {}".format(new_card))
        new_status = new_status.fetchall()
    except:
        new_status == []
    if new_card == card_number:
        print("You can't transfer money to the same account!")
    elif check_luh(new_card) == False:
        print("Probably you made mistake in the card number. Please try again!")
    elif new_status == []:
        print("Such a card does not exist.")
    elif new_status[0][1] == new_card:
        print("Enter how much money you want to transfer:")
        amount = int(input())
        if amount > balance:
            print("Not enough money!")
        else:
            conn.execute("UPDATE card SET balance = balance - {} WHERE number = {}".format(amount, card_number))
            conn.commit()
            conn.execute("UPDATE card SET balance = balance + {} WHERE number = {}".format(amount, new_card))
            conn.commit()
            print("Success!")


def delete_card(card_number):
    conn.execute("DELETE FROM card WHERE number = {}".format(card_number))
    conn.commit()
    print("\nThe account has been closed!\n")


def log_in():
    print('\nEnter your card number:')
    card_number = input()
    print('Enter your PIN:')
    pin = input()
    try:
        status = conn.execute("SELECT * FROM card WHERE number = {} AND pin = {};".format(card_number, pin))
        status = status.fetchall()
        if status[0][1] == card_number and status[0][2] == pin:
            print("\nYou have successfully logged in!")
            while True:
                status = conn.execute("SELECT * FROM card WHERE number = {} AND pin = {};".format(card_number, pin))
                status = status.fetchall()
                balance = status[0][3]
                print('\n1. Balance\n2. Add Income\n3. Do Transfer\n4. Close Account\n5. Logout\n0. Exit')
                option = input("Enter process: ")
                if option == "1":
                    print("\nBalance: {}".format(balance))
                elif option == "2":
                    update(card_number)
                elif option == "3":
                    transfer(card_number, balance)
                elif option == '4':
                    delete_card(card_number)
                    return None
                elif option == "5":
                    print("\nYou have successfully logged out!\n")
                    return None
                elif option == "0":
                    return option
        else:
            return False
    except Exception as e:
        print(e)
        return False



conn = sqlite3.connect('card.s3db ')
conn.execute('''CREATE TABLE  IF NOT EXISTS card
         (id INTEGER,
         number TEXT,
         pin TEXT,
         balance INTEGER DEFAULT 0);''')

while True:
    print('1. Create an account\n2. Log into account\n0. Exit')
    choice = input("Enter your choice: ")
    if choice == '0':
        print('\nBye!')
        break
    elif choice == '1':
        create_account()
    elif choice == '2':
        option = log_in()
        if option == False:
            print("\nWrong card number or PIN!\n")
        elif option == '0':
            print('\nBye!')
            break
