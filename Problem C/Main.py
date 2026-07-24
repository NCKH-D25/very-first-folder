from tries import *

#Varibles
Data =[]
Words = []
Available_Weight = []
Max_Error = 2

#File hanlding
try:
    with(open("Dictionary.txt", "r")) as f:
        Data = f.readlines()
except FileNotFoundError:
    print("The file is not existed!")
except Exception as e:
    print("An unexception error is occurred")

#Handling the Data Lines
for lines in Data:
    clean_line = lines.replace(",", "").strip().split()
    if not clean_line:
        print("This line is empty!")
        continue
    else:
        if len(clean_line) < 2:
            print("The line is too short (< 1)! ")
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
            # print(clean_line[:-1])
            Available_Weight.append(Current_Weight)
            Completed_Word = " ".join(clean_line[:-1]).lower()
            Words.append(Completed_Word)

#Print the Output    
# print(Words)
# print(Available_Weight)
        
trie = Trie()

for i in range(50000):
    trie.insert(Words[i], Available_Weight[i])
    
ip3 = "we"
print(trie.autocomplete(ip3))