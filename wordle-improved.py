import random

def load_words(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

input_words = load_words('valid-words14855.txt')
answer_words = load_words('answer_words.txt')

target_word = 'abide'  # For testing purposes, you can randomize this

def display_guess_result(guess, target):
    feedback = ["⬜"] * 5
    target_letter_count = {}

    # First pass: check for correct positions
    for i in range(5):
        if guess[i] == target[i]:
            feedback[i] = "🟩"
        else:
            if target[i] in target_letter_count:
                target_letter_count[target[i]] += 1
            else:
                target_letter_count[target[i]] = 1

    # Second pass: check for correct letters in the wrong positions
    for i in range(5):
        if feedback[i] == "⬜" and guess[i] in target_letter_count and target_letter_count[guess[i]] > 0:
            feedback[i] = "🟨"
            target_letter_count[guess[i]] -= 1

    return ''.join(feedback)

def filter_words(words, guess, feedback):
    possible_words = []
    for word in words:
        match = True
        word_letter_count = {}

        # Count occurrences of each letter in the word
        for letter in word:
            if letter in word_letter_count:
                word_letter_count[letter] += 1
            else:
                word_letter_count[letter] = 1

        for i in range(5):
            if feedback[i] == "🟩":
                if word[i] != guess[i]:
                    match = False
                    break
            elif feedback[i] == "🟨":
                if word[i] == guess[i] or guess[i] not in word_letter_count or word_letter_count[guess[i]] <= 0:
                    match = False
                    break
                word_letter_count[guess[i]] -= 1
            elif feedback[i] == "⬜":
                if guess[i] in word_letter_count and word_letter_count[guess[i]] > 0:
                    match = False
                    break

        if match:
            possible_words.append(word)

    return possible_words

def wordle_game():
    max_guesses = 6
    guess_count = 0
    possible_words = answer_words

    print(f"Valid input num: {len(input_words)}")
    print(f"Answer num: {len(answer_words)}")
    print(f"Answer: {target_word}")

    while guess_count < max_guesses:
        guess = input(f"Guess {guess_count + 1}: ").lower()

        if len(guess) != 5:
            print("Please enter a 5-letter word.")
            continue

        if guess not in input_words:
            print("Word not in list.")
            continue

        feedback = display_guess_result(guess, target_word)
        print(feedback)

        guess_count += 1

        if guess == target_word:
            print("Congratulations! You've guessed the word!")
            break

        possible_words = filter_words(possible_words, guess, feedback)
        print(f"Possible words remaining: {len(possible_words)}")
    else:
        print(f"Game Over. The word was: {target_word}")

if __name__ == "__main__":
    wordle_game()
