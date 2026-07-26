from tries import *

#Variables
Data =[]
Max_Error = 2
trie = Trie()

#File Handling
try:
    with(open("Dictionary.txt", "r")) as f:
        Data = f.readlines()
except FileNotFoundError:
    print("The file does not exist!")
except Exception as e:
    print("An unexceptional error occurred")

#Handling the Data Lines
for lines in Data:
    clean_line = lines.replace(",", "").strip().split()
    if len(clean_line) < 2:
        print("The line is too short (< 2)! ")
        continue
    try:
        Current_Weight = int(clean_line[-1])
    except ValueError:   
        print("The weight must be a positive integer!")
        continue
    if Current_Weight <= 0:
        print("The weight must be a positive integer!")
        continue
    else:
        Completed_Word = " ".join(clean_line[:-1]).lower()
        trie.insert(Completed_Word, Current_Weight)


#User Inputting validation
while True:
    User_Input = input("Enter a word: ").lower()
    if User_Input == "" or " " in User_Input or User_Input.isalpha() == False:
        print("Invalid word! Please try again!")
    else:
        res = trie.autocomplete(User_Input)
        if res:
            print("Do you mean: ", end="")
            print(res[0][0])
            break
        else:
            res = trie.fuzzy_search(User_Input)
            if res:
                print("Do you mean: ", end="")
                print("{}".format(res[0]))
                break
            else:
                print("Invalid Word! PLease try again!")
        
