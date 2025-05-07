import random
import math
from collections import Counter

def load_words(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

# 加载输入单词和答案单词
input_words = load_words('valid-words14855.txt')
answer_words = load_words('answer_words.txt')

# target_word = random.choice(answer_words)
target_word='lower'

def display_feedback(guess, target):
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

        test_feedback = display_feedback(guess, word)
        if test_feedback != feedback:
            match = False
            continue

        if match:
            possible_words.append(word)

    return possible_words


def calculate_entropy(possible_words, guess):
    feedback_counts = Counter(display_feedback(guess, word) for word in possible_words)
    total = sum(feedback_counts.values())
    entropy = 0.0
    for count in feedback_counts.values():
        probability = count / total
        entropy -= probability * math.log2(probability)
    return entropy

def display_top_entropy_words(possible_words):
    entropies = [(word, calculate_entropy(possible_words, word)) for word in possible_words]
    entropies.sort(key=lambda x: x[1], reverse=True)

    print("Top 10 words by entropy:")
    for word, entropy in entropies[:10]:
        print(f"{word}: {entropy:.4f}")

def wordle_game():
    max_guesses = 6
    guess_count = 0
    possible_words = answer_words

    # 打印单词数和目标单词
    print(f"Total input words: {len(input_words)}")
    print(f"Total answer words: {len(answer_words)}")
    print(f"Target word: {target_word}")

    # 初次计算并显示熵分布
    # display_top_entropy_words(possible_words)

    while guess_count < max_guesses:
        guess = input("Enter your guess: ").strip().lower()

        if len(guess) != 5:
            print("Please enter a 5-letter word.")
            continue

        if guess not in input_words:
            print("Word not in list.")
            continue

        guess_count += 1
        feedback = display_feedback(guess, target_word)
        print(f"Guess {guess_count}: {guess} {feedback}")

        if guess == target_word:
            print("Congratulations! You've guessed the word!")
            return

        possible_words = filter_words(possible_words, guess, feedback)
        print(f"Possible words remaining: {len(possible_words)}")

        display_top_entropy_words(possible_words)

    print(f"Game Over. The word was: {target_word}")



def wordle_game_simulation():
    total_rounds = 0
    num_simulations = len(answer_words)

    for target_word in answer_words:
        guess_count = 0
        possible_words = input_words

        while True:
            # 计算每个可能单词的熵
            entropies = [(word, calculate_entropy(possible_words, word)) for word in possible_words]
            entropies.sort(key=lambda x: x[1], reverse=True)

            # 选择熵最大的单词作为猜测
            guess = entropies[0][0]
            guess_count += 1

            feedback = display_feedback(guess, target_word)

            if guess == target_word:
                total_rounds += guess_count
                break

            possible_words = filter_words(possible_words, guess, feedback)

    average_rounds = total_rounds / num_simulations
    print(f"Average rounds to solve: {average_rounds:.2f}")


if __name__ == "__main__":
    wordle_game()
    # wordle_game_simulation()