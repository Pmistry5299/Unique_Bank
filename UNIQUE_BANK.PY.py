import sqlite3
account = {}
user = {}
import sqlite3

def create_acc():
    cursor = connection.cursor()
    cursor.execute(f"SELECT account_no from account")
    lastkey, = cursor.fetchall()[-1]
    print()

    new_acc = lastkey+1
    account[new_acc] = 0
    print("Account No: ", new_acc)
    password_condition = "True"
    while password_condition:
        try:
            pin = int(input("Enter pin:"))
            if len(str(pin)) == 4:
                user[new_acc] = pin
                break
            else:
                print("opps! password is not in 4 digit")
                continue
        except ValueError:
            print("please try correct number")
        else:
            password_condition = "False"

    cursor = connection.cursor()
    cursor.execute("INSERT INTO account (account_no,pin,balance) values ({},{}, 0);".format(new_acc, pin))
    cursor.execute("COMMIT;")
    cursor.close()

    print("***  Hurrey, Your Account has been created successfully  ***\n")
    print("Welcome to Unique Bank. \nYour account number is ", new_acc)
    print()

def type_amount():
    correct_amount = "True"
    while correct_amount:
        try:
            amount = int(input("Enter Amount:"))
        except ValueError:
            print("!!!  Opps, Invalid inpute amount  !!!\n")
            print("Please try again")
            continue
        if amount > 0:
            correct_amount = "False"
            break
        print("!!!  Opps, Account is not found  !!!\n")
        print("Please try again")
    return amount

def type_account():
    correct_account = "True"
    while correct_account:
        try:
            acc_no = int(input("Enter Account No:"))

            cursor = connection.cursor()
            cursor.execute(f"SELECT LOGIN FROM account WHERE account_no='{acc_no}' ;")
            if not cursor.fetchone():
                correct_account = "False"
                continue

        except ValueError:
            print("!!!  Sorry, positive numbers are only allowed  !!!\n")
            print("Please, Try again\n")
            continue
        print("!!!  Opps, You selected invalid account  !!!\n")
        # use when account not find
        print("Please, choose correct Account \n")
    return acc_no

def display_balance(acc):
    print("*** Your current balance is ", account.get(acc), " dollars   ***")

def AddMoney(acc_no, amount=0):
    message_print = 0
    if amount == 0:
        amount = type_amount()
        message_print = 1  # account balance Message only print when it deposite
    # temp = account.index(acc_no)
    account[acc_no] = amount + account[acc_no]
    return message_print

def DeductMoney(acc_no, amount=0):
    if amount == 0:
        amount = type_amount()
    if account.get(acc_no) >= amount:
        account[acc_no] = account.get(acc_no) - amount
        display_balance(acc_no)
        return 1
    else:
        print("!!!  Opps, You have insufficient money  !!!\n Please, Deposite first")
        return 0

def login_options():
    login_con = "True"
    while login_con:
        try:
            user_acc = int(input("Enter account number:"))
            pin = int(input("enter Pin no:"))

            cursor = connection.cursor()
            cursor.execute(f"SELECT account_no FROM account WHERE account_no='{user_acc}' AND pin = '{pin}';")
            if not cursor.fetchone():
                print("Opps! LOGIN ID AND PASSWORD IS INCORRECT IF YOU HAVE NOT CREATED ACCOUNT, PLEASE CREATE FIRST TO ACCESS\n ")
                continue

            if len(str(pin)) != 4:
                print("pin must be 4 digit")
                continue

        except ValueError:
            print("plese type account number carefully")
        else:
            login_con = "False"
        login(user_acc)

def login(acc_no):
    wrong_ans = "True"
    while wrong_ans:
        options = [1, 2, 3, 4, 5, 0]
        print("|---  Unique Bank ---|")
        print("1) Acoount Information \n2) Deposit \n3) Withdraw \n4) Transfer Money \n5) create another account \n0) Exit")
        try:
            choise = int(input("PLEASE CHOOSE SERVIECE:"))
            print()
            if choise not in options:
                print("!!! Opps, you select wrong option  !!! ")
                print("Please try again \n")
                continue
            elif choise == 0:
                print()  # in order to exit if loop
            elif choise != 1 and len(account) == 0:
                print("!!!  Opps, You have not open account Yet   !!!")
                print("please, open account first to use our services \n")
                continue

            elif choise == 4 and len(account) < 2:
                print("@@@ Sorry, Transaction is not posible  @@@")
                print("you have to create another account First\n")
                continue

        except ValueError:
            print("!!!  Opps, You are not selected Correct number  !!!")
            print("Please, try again @\n")
            continue

        else:
            wrong_ans = "False"

        if choise == 1:
            print("your account number is: ", acc_no)
            display_balance(acc_no)
            print()

        if choise == 2:
            deposit_acc = acc_no
            if account.get(deposit_acc) is not None:
                message_print = AddMoney(deposit_acc)
            if message_print == 1:
                display_balance(deposit_acc)
                print()

        if choise == 3:
            withdraw_acc = acc_no
            if account.get(withdraw_acc) is not None:
                DeductMoney(withdraw_acc)
            print()

        if choise == 4:
            print("Transfer From")
            transfer_from = acc_no
            transfer_to = type_account()
            if account.get(transfer_to) is not None and transfer_from != transfer_to:
                damount = type_amount()
                successful_tran = DeductMoney(transfer_from, damount)
                if successful_tran == 1:
                    AddMoney(transfer_to, damount)
                    print()
            else:
                print("Self Transfer is not possible ")

        if choise == 0:
            print("//*****  Thank you to visit Unique Bank  *****\\")
            print("//*****         Have a nice day!         *****")
            break

if __name__ == "__main__":

    connection = sqlite3.connect("USER.DB")
    print("|---  Unique Bank ---|")
    print("1) Create Account \n2) Log In \n0) Exit")
    options1 = [0, 1, 2]
    co_op_1 = "True"

    while co_op_1:
        try:
            choise1 = int(input("PLEASE CHOOSE SERVIECE:"))

            if choise1 not in options1:
                print("!!! Opps, you select wrong option  !!! ")
                print("Please try again \n")
                continue
            elif choise1 == 0:
                co_op_1 = "False"
                print("*****  Thank you to visit Unique Bank  *****")
                print("*****         Have a nice day!         *****")
                print()  # in order to exit if loop

            if choise1 == 1:
                create_acc()
                con = int(input("would you like to login. \n1)Yes \n2)No\nselect option:"))
                if con == 1:
                    login_options()
                else:
                    print("*****  Thank you to visit Unique Bank  *****")
                    print("*****         Have a nice day!         *****")
                    break

            if choise1 == 2:
                print("----------Login---------")
                login_options()

        except ValueError:
            print("!!!  Opps, You are not selected Correct number  !!!")
            print("Please, try again @\n")
            continue
        else:
            wrong_ans = "False"