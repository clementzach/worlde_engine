import sys

def compare(word_to_compare, current_guess):
	current_guess = list(current_guess)
	for i in range(len(current_guess)):
		if word_to_compare.find(current_guess[i]) == -1:
			current_guess[i] = '0'
		else:
			if current_guess[i] == word_to_compare[i]:
				current_guess[i] = '2'
			else:
				current_guess[i] = '1'
	return(''.join(current_guess))
				

def main():
	word_to_compare = input("Type the word you would like feedback on\n")
	still_playing = True
	while still_playing:
		current_guess = input("Type a guess (x to exit)\n")
		if current_guess == "x":
			sys.exit()
		print(compare(word_to_compare, current_guess)+ "\n")

	
	

if __name__ == "__main__":
	main()

