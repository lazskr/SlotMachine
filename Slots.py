import os 
import random #generate slot machine values randomly via RNG
import Constants

#function which calculates how much the user won, lost or are leaving with the same balance 
#that they originally entered
def gain_or_loss(orig_bal, final_bal):
    if final_bal < orig_bal:
        print(f"You have lost: ${orig_bal-final_bal}.\n")
    elif final_bal > orig_bal:
        print(f"You have won: ${final_bal-orig_bal}.\n")
    else: #original balance = final balance 
        print("You did not lose or win any money.\n")

#function which returns the dictionary contianing the symbols for the slot machine and their count
def return_symbol_count():
    #Symbols for the slot machine are @, #, + and ! and the # of times they appear per reel
    symbol_count = {"@": 3, "#" : 5, "+" : 7, "!" : 9} #dictionary (24 total)
    return symbol_count

#function which returns the dictionary containing the symbols for the slot machine and their multiplier (if 3 of the same symbol appear)
def return_symbol_value():
    symbol_values = {"@": 5, "#" : 4, "+" : 3, "!" : 2} #multiplier of bet for winnings
    return symbol_values 


#instructions function which explains the slot game
def instructions():
    print("Welcome to Python slots! As the user you will be required to enter your\n"
          "your balance which will increase in value if you win, but decrease in value\n"
          "if you lose. The slot machine is 3 by 3 and to win the same symbol must appear\n"
          "in the whole line. However, you have the choice for how many lines that you want\n"
          "on. Your bet for each spin will be multiplied by the lines that you have bet on.\n"
          "This value will either be subtracted or added to your balance for each spin depending\n"
          "on the outcome of the spin. The symbols which may appear in order of lowest to highest\n"
          "rarity are: @, #, + and !.\n")

#determines if the selected rows result in winnings for the user 
def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line] #assume we have 1 reel -- -> |
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break; 
        else:
            winnings += values[symbol]*bet #accessing the dictionary 
            winning_lines.append(lines + 1) #giving the user information regarding the line they won on 
        
    return winnings, winning_lines


#function which generates the outcome of the slot machine 
def slot_machine_spin(rows, cols, symbols):
    
    all_symbols = []

    #symbols.items() gives key and value in a dictionary (key is symbol and num_symbols is # of times it appears)
    #adds all symbols in all_symbols list
    for key, value in symbols.items(): 
        for _ in range(value): #_ represents a variable where we don't care for the iteration value | we can use i to represent it 
            all_symbols.append(key) #appending to array 

    columns = [] #we need to append the columns for it to go from [] -> [[], [], []]
    for _ in range(cols): #for each column in slot machine
        cur_row = []
        current_symbols = all_symbols[:] #copies the list (using slice operator) via the ":" as we need all 24 symbols for each solumn in the slot machine
        for _ in range(rows): #for each value in the current column
            value = random.choice(current_symbols) #from import random 
            current_symbols.remove(value) 
            cur_row.append(value)
        columns.append(cur_row) #appends row (1*3 matrix) into columns. This row will be transposed and act as a 1 reel 

    return columns


#function which prints out the slot machine after slot_machine_spin() has been called
def print_slot_col(columns): #need to flip rows into columns (transposing the matrix)
    for row in range(len(columns[0])): #length of first array in the 2D array (for each value in the row (or our column))
        for i, col in enumerate(columns): #i is the count, col is the value of the variable columns 
            if i != len(columns)-1:
                print(col[row], end = " | ")
            else:
                print(col[row], end = "")
        print() #empty print statement (prints new line (\n) by default)
            
    


#This function sets the user's balance (amount they have to spend)
def set_deposit(): 
    while True:
        amount = input("How much would you like to deposit $? (no cents)\n")
        if amount.isdigit():
            amount = float(amount) #converting string to int as input of user is always a string 
            if amount > 0: #checking if value is positive 
                break 
            else:
                os.system('cls')
                print("Amount must be a a positive value > 0.\n")
        else:
            os.system('cls')
            print("Please enter a number. \n")

    os.system('cls')
    return amount 

#The user enters the number of lines which they would like to bet on (1-3)
def set_num_lines():
    while True:
        lines = input("Please enter the number of lines to bet on (1-" + str(Constants.MAX_LINES) + ").\n")
        if lines.isdigit():
            lines = int(lines) #converting string to int as input of user is always a string 
            if 1 <= lines <= Constants.MAX_LINES: #checking if value is positive 
                break 
            else:
                os.system('cls')
                print("Please enter a valid number of lines.\n")
        else:
            os.system('cls')
            print("Please enter a number.\n")

    os.system('cls')
    return lines 

#amount that the user bets on each line
def set_bet():
    while True:
        bet = input("What would you like to bet on each line $? (between $1 and $1000 inclusive - no cents) \n")
        if bet.isdigit():
            bet = float(bet) #converting string to int as input of user is always a string 
            if Constants.MIN_BET <= bet <= Constants.MAX_BET: #checking if value is positive 
                break 
            else:
                os.system('cls')
                print(f"Amount must be between {Constants.MIN_BET}-{Constants.MAX_BET}.\n") #f-string which allows for direct variable use in string (converts value to string)
        else:
            os.system('cls')
            print("Please enter a number.\n")

    os.system('cls')
    return bet 


#determines whether the user's total bet exceeds their inputted balance 
def check_bet_against_balance(input_balance, input_lines):
    while True:
        cur_bet = set_bet()
        cur_total_bet = cur_bet * input_lines

        if cur_total_bet > input_balance:
            os.system('cls')
            print(f"You do not have sufficient funds to bet that amount. Your current balance is: ${input_balance: .2f}.\n")
        else:
            return cur_bet


def per_spin(user_balance):
    lines = set_num_lines()
    bet = check_bet_against_balance(user_balance, lines)
    
    total_bet = bet*lines
    os.system('cls')
    print(f"You are betting ${bet:.2f} on {lines} lines. The total bet is: ${total_bet:.2f}.\n")

    slots = slot_machine_spin(Constants.ROW, Constants.COL, return_symbol_count())
    print_slot_col(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, return_symbol_value())
    print(f"You won ${winnings:.2f}.\n")
    print(f"You won on lines:", *winning_lines, "\n") #splat/unpack operator which passes each line from winning_lines list to print() function
    return winnings - total_bet 

def main():
    instructions()
    streak = 0
    balance = set_deposit() #initial balance entered by the user 
    original_balance = balance 
    while True:
        print(f"Your current balance is: ${balance:.2f}.\n")
        spin = input("Enter p/P to play! | Enter q/Q to quit.\n")
        if spin == "Q" or spin == "q":
            os.system('cls')
            break
        elif spin == "P" or spin == "p": 
             os.system('cls')
             prev_balance = balance
             balance += per_spin(balance) 
             if balance < prev_balance:
                streak = 0
             else:
                streak += 1 #if you maintain your balance or increase in it, you streak will increase
             print(f"Your current streak is: {streak}.\n")
        else: 
            os.system('cls')

    print(f"You entered with ${original_balance:.2f} and you are leaving with ${balance:.2f}")
    gain_or_loss(original_balance, balance)


os.system('cls')
main() #calls main function for execution of program 

        

