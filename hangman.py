#Credits for the hangman ASCII art: 
#    https://gist.github.com/chrishorton/8510732aa9a80a03c829b09f12e20d9c


import os, random


hangman = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']



def dis_msg(msg):
    """Prints the string msg inside a frame of stars *"""
    width = len(msg)+6
    print(width*"*")
    print("*"+ (width-2)*" "+ "*" )
    print("*"+ 2*" "+msg+2*" "+"*")
    print("*"+ (width-2)*" "+ "*" )
    print(width*"*")


def word_to_dic(word):
    """takes a string word and creat a dictionary where the keys are 
    the letters of word (without repetition) and the values for each key 
    is a list of the indexes of that key in word"""
    word_dic = {}
    for i in range(len(word)):
        try:
            word_dic[word[i]].append(i)
        except KeyError:
            word_dic[word[i]] = [i]
    return word_dic
            
            
def dashed_word(word):
    """Takes a string word and returnes a list that when joined over an empty 
    string, it resemples word. 
    e.g. input = 'eat', output = ['-', '-', '-']
    input = "eat apple" , 
    output = ['-', '-', '-', ' ', '-', '-', '-', '-', '-']"""
    dashed_list = []
    for ch in word:
        if ch == " ":
            dashed_list.append(" ")
        else:
            dashed_list.append("-")
    return dashed_list
            
def update_dashed(lst, letter, index):
    """ takes a list lst, a string letter, a list of integers index. 
    this funcitions puts thestring letter in list[i] for every i in index"""
    for i in index:
        lst[i] = letter

def get_words(file_name, level):
    """takes a string file_name that exists in the cwd and string level
    and returns a list whose elements are lists of two elements. the first one
    is the category of the word, and the second is the word. the level of 
    these words is level """
    words_list = []
    words_file = open(file_name)
    for line in words_file:
        if line[0] == level:
            line_list = line.split(", ")
            words_list.append(line_list[1:])
    return words_list


def choose_file():
    
    """prints the .txt files in the cwd and prompts the user to chose among 
    them"""
    dir_path = os.path.dirname(os.path.realpath(__file__)) # to get the directory where the file is located
    os.chdir(dir_path) # set current directory to the directory where the file is located
    files_list = [file for file in os.listdir(dir_path) if file.endswith(".txt")] 
    valid_input = [str(i+1) for i in range(len(files_list))]
    
    print("You can choose one of the following files:")
    for i in range(len(files_list)):
        print(str(i+1)+".", files_list[i])
    file_name_tmp = input("What file do you want to use?\n"+
                          "(Enter a number 1-"+str(len(files_list))+")\n"+
                          "qq: quit the game\n" ).strip().lower()
    while file_name_tmp not in valid_input and file_name_tmp!= "qq":
        print("Error: Wrong Input")
        file_name_tmp = input("What file do you want to use?\n"+
                          "(Enter a number 1-"+str(len(files_list))+")\n"+
                          "qq: quit the game\n").strip().lower()
    if file_name_tmp == "qq":
        file_name = "qq"
    else:
        file_index = valid_input.index(file_name_tmp)
        file_name = files_list[file_index]
    return file_name
        
def main_menu():
    """ starts the program, prints a welcoming message, 
    uses the function choose_file to choose a file, prompts the user to 
    choose the level and then uses the function get_words to get a list of 
    words as described in the function get_words """
    open_status = True
    dis_msg("__Welcome to $$NAME$$'s Hangman__")
    
    #choose a file
    file_name = choose_file()
    if file_name == "qq":
        dis_msg("Goodbye!")
        open_status = False
        return open_status, None
    
    #ask for the level
    level = input("What level do you want to play?\ne: Easy\n"+
                  "m: Medium \nh: Hard \nqq: quit the game\n").strip().lower()
    while level not in ["e", "m", "h", "qq"]:
        print("please enter e, m, or h")
        level = input("What level do you want to play?\ne: Easy\n"+
                  "m: Medium \nh: Hard \nqq: quit the game\n").strip().lower()
    if level == "qq":
        dis_msg("Goodbye!")
        open_status = False
        return open_status, None
    #get words
    words_list = get_words(file_name, level)
    return open_status, words_list

def new_game(words_list):
    """starts a game round. This includes get a random word, 
    mask it using the function dashed_word,
    store the data of the word in a dictionary as described by the function
    word_to_dic,
    reset the lives of the player,
    """
    random_index = random.randrange(len(words_list))
    category = words_list[random_index][0].strip()
    word = words_list[random_index][1].strip()
    dashed = dashed_word(word)
    word_dic = word_to_dic(word)
    lives = 7
    return category, word, dashed, word_dic, lives


##################
#    The Game    #
##################

open_status, words_list = main_menu()

while open_status:
    category, word, dashed, word_dic, lives = new_game(words_list)
    print("This one asks for a(n) "+category)
    
    while lives>0:
        print("".join(dashed))
        guess = input("What is your guess? \nqq: quit the game"
                      +" \nmm: Main Menu \n").strip().lower()
        while (len(guess)> 1 or guess == "") and guess !="qq" and guess != "mm": 
            print("Please enter one letter, qq, or mm")
            guess= input("What is your guess? \nqq: quit the game"
                         +"\nmm: Main Menu \n").strip().lower()
        if guess == "qq":
            dis_msg("Goodbye!")
            open_status = False
            break
        elif guess == "mm":
            open_status, words_file, level = main_menu()
            break
        elif guess in word_dic:
            index= word_dic[guess]
            update_dashed(dashed, guess, index)
            if len(index) == 1:
                print("There is 1", guess)
            else:
                print("There are", len(index), guess+"\'s")
            if "-" not in dashed:
                dis_msg("Awesome! You won!")
                break
        else:
            print("There are no "+guess+"\'s")
            print(hangman[len(hangman)-lives])
            lives -= 1
            if lives == 0:
                dis_msg("You killed the man!!")
                    
            
    #Another game?
    if guess!= "qq":
        another_game = input("Another word? y: yes or n: no"+
                             "\nmm: Main Menu\n").strip().lower()
        while another_game not in ["y", "n", "mm"]:
            print("Error: Wrong Input")
            another_game = input("Another word? y: yes or n: no"+
                             "\nmm: Main Menu\n").strip().lower()
        if another_game =="n":
            dis_msg("Goodbye!")
            open_status= False
        elif another_game == "mm":
            open_status, words_list = main_menu()

        






        
