import pandas as pd
import numpy as np
import string
import random

NUM_TOTAL_LETTERS = 5



LETTERS_LIST = []
for global_letter in string.ascii_lowercase:
    LETTERS_LIST.append(global_letter)

def get_best_words(current_df, right_place_dict, contains_set):
    if len(contains_set) == NUM_TOTAL_LETTERS: 
        #case: we just have to find anagrams
        #case: there's no further narrowing to do here
        possible_words = current_df['word'].tolist()
        random_word = random.choice(possible_words)
        return(random_word)
    else:
        # sum columns, then select columns with letters, then get highest NUM_MAX_LETTERS values (less than 5 in case of duplicates)
        top_letters = current_df.sum()[LETTERS_LIST].sort_values(ascending = False).index.tolist() 
        
        top_letters = [x for x in top_letters if x not in contains_set] ## We want to eliminate any already used
        
        num_max_letters = NUM_TOTAL_LETTERS - len(contains_set) - 1 ## leave 1 space for a possible duplicate
        temp_contains_set = set([])
    
        for i in range(num_max_letters):
            temp_contains_set.add(top_letters[i])
    
        possible_words = restrict_df(current_df, contains_set = temp_contains_set)['word'].tolist() #list of all possible words that have these top letters somewhere
        if len(possible_words) > 0: #there exists a best guess
            random_word = random.choice(possible_words) #select one word
            return(random_word)
        else: #give up and just select a possible word
            possible_words = current_df['word'].tolist()
            random_word = random.choice(possible_words)
            return(random_word)
            
    

    


def restrict_df(current_df, right_place_dict = {}, contains_set = set([]), wrong_position_list = [], not_contains_set = set([])):
    working_df = current_df.copy() #don't manipulate current_df in case we call this elsewhere
    for num in right_place_dict.keys():
        working_df = working_df[working_df[f"letter_{num}"] == right_place_dict[num]]
    for letter in contains_set:
        working_df = working_df[working_df[letter] > 0] #the letter occurs at least once
    for letter in not_contains_set:
        working_df = working_df[working_df[letter] == 0] #the letter happens 0 times
    for letter_pair in wrong_position_list:
        good_indices = working_df['word'].apply(lambda x: x[letter_pair[0]] != letter_pair[1])
        working_df = working_df[good_indices]
    return(working_df.copy())

def update_letter_info(right_place_dict, contains_set, wrong_position_list, not_contains_set, response_string, current_guess):
    
    for i in range(len(response_string)):
        response = response_string[i]
        if response == '0':
            not_contains_set.add(current_guess[i])
        elif response == '1':
            contains_set.add(current_guess[i])
            wrong_position_list.append([i, current_guess[i]])
        elif response == '2':
            right_place_dict[i + 1] = current_guess[i]
            contains_set.add(current_guess[i])
    return([right_place_dict, contains_set, wrong_position_list, not_contains_set])

def main():
    right_place_dict = {} #A dict, will have a key with each possible entry (1-5) and values as letters in that entry.
    contains_set = set([]) #A set of all letters that are included somewhere
    not_contains_set = set([]) #A set of all letters that are eliminated
    wrong_position_list = [] #A list of lists. For each list, the first element is the position, and the second element is the letter which does not go in that position.
    
    current_df = pd.read_csv('words_list_df.csv')
    
    still_playing = True
    while still_playing:
        current_guess = get_best_words(current_df, right_place_dict, contains_set)
        print(f"My guess is {current_guess} \n")
        
        response_string = ""
        num_responses = 0
        while len(response_string) != NUM_TOTAL_LETTERS:
            if num_responses > 0:
                print("Error: improper string length")
            
            response_string = input("0:black, 1:yellow, 2:green \n")
            num_responses = num_responses + 1
        
        right_place_dict, contains_set, wrong_position_list, not_contains_set = update_letter_info(right_place_dict, contains_set, wrong_position_list, not_contains_set, response_string, current_guess)

        current_df = restrict_df(current_df, right_place_dict, contains_set, wrong_position_list, not_contains_set)
        if current_df.shape[0] == 0:
            print("Looks like your word is not in my dictionary. Sorry...")
            still_playing = False
        if response_string == "2"*NUM_TOTAL_LETTERS:
            print("I win!")
            print("Thanks for playing")
            still_playing = False
        


if __name__ == "__main__":
    main()

