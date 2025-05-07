import random

# 词汇表
# words = ["apple", "grape", "peach", "berry", "lemon"]

# 从文件中读取单词列表
def load_words(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

# 加载输入单词和答案单词
input_words = load_words('valid-words14855.txt')
answer_words = load_words('answer_words.txt')

# 随机选择一个单词
# target_word = random.choice(answer_words)
target_word='abide'

def display_guess_result(guess, target):
    feedback = ""
    for i in range(5):
        if guess[i] == target[i]:
            feedback += "🟩"  # 正确位置
        elif guess[i] in target:
            feedback += "🟨"  # 错误位置但存在该字母
        else:
            feedback += "⬜"  # 不存在该字母
    return feedback

def filter_words(words, guess, feedback):
    possible_words = []
    for word in words:
        match = True
        for i in range(5):
            if feedback[i] == "🟩" and word[i] != guess[i]:
                match = False
                break
            elif feedback[i] == "🟨" and (word[i] == guess[i] or guess[i] not in word):
                match = False
                break
            elif feedback[i] == "⬜" and guess[i] in word:
                match = False
                break
        if match:
            possible_words.append(word)
    return possible_words

def wordle_game():
    max_guesses = 6
    guess_count = 0
    possible_words = answer_words

    # print("Welcome to Wordle!")
    # print("Try to guess the 5-letter word.")
    print(f"valid input num:{len(input_words)}")
    print(f"answer num:{len(answer_words)}")
    print(f"Answer: {target_word}")

    while guess_count < max_guesses:
        guess = input(f"Guess {guess_count + 1}: ").lower()

        if len(guess) != 5:
            print("Please enter a 5-letter word.")
            continue

        if guess not in input_words:    #input must be in the valid list
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
