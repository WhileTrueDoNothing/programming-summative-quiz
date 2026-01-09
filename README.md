# Postcode Area Quiz
A quiz built in Python for testing postcode area knowledge. Currently only runs in the command line.

# Requirements
To run this program, you will need a Python environment set up with the following packages (also detailed in requirements.txt):
- numpy ver. 2.4.0
- pandas ver. 2.3.3

# How to play
#### Open the game's folder in the command prompt or terminal
After downloading the folder, open your computer's command prompt or terminal. Use the cd command to navigate to the folder containing main.py.
#### Run `main.py`
Use `python main.py` in the command line to run the game.
<img width="997" height="90" alt="image" src="https://github.com/user-attachments/assets/aaa7683a-c593-478d-9bca-ac62c7f8fb28" />
#### Select a difficulty
The quiz currently has 2 difficulties: Normal and Hard. Normal difficulty will give you multiple-choice questions, giving you a hint as to the answer. Hard difficulty instead uses a free text input, with no extra help. Type either the difficulty you want, or the letter associated with it on the menu. Either way will work.
<img width="798" height="179" alt="image" src="https://github.com/user-attachments/assets/96e6a266-dfb5-4a15-9172-a151f38319a9" /> 
<img width="804" height="177" alt="image" src="https://github.com/user-attachments/assets/c9b4be11-72be-4a58-a342-4f93b33524a2" />
#### Answer questions
For multiple choice questions, you can answer either by typing the answer itself or the letter associated with it. The program won't accept an answer until you choose one of the available options. The free text input of hard mode will accept the first input you make, no matter what it is. This lets you skip a question you're stuck on by pressing enter, but make sure to spell your guesses correctly!
<img width="663" height="210" alt="image" src="https://github.com/user-attachments/assets/ada1376f-c4a1-4f17-a746-a5eb4337b0bf" />
<img width="688" height="100" alt="image" src="https://github.com/user-attachments/assets/5dd9531a-f586-492e-8959-6ac9893ea3b8" />

Each quiz has 10 questions in total. Good luck!
# Technical Notes
Here I'll detail how each part of the program works, including classes, functions, attributes and variables.

## main
You need to run main.py to play the game. Its overall structure is a simple sequence contained within a while loop. Until the user inputs that they don't want to play again, it will repeat the following steps:
1. Have the user select a difficulty. This will repeat until the user inputs a valid difficulty option.
2. When the user inputs a valid difficulty option, it will generate questions according to the selected difficulty using `gen_questions_csv()`. If hard difficulty is selected, the function is called with the `multi_choice` parameter set to False. As the default value for `multi_choice` is True, this does not need to be specified while generating normal difficulty questions.
3. Once a question list has been generated, call the `run_quiz()` function with the newly-created question list. This will run the quiz, and print the user's score at the end.
4. Ask the user if they want to play again. If they select anything other than "y", the loop will end and the game will shut down.

#### Variables within `main`
|Name|Type|Description|
|----------|-------|--------|
|`play_again`|bool|Initialized as True, can be set to False if the user doesn't want to play again at the end of a quiz. This will end the while loop.|
|`SEPARATOR_STRING`|str|A constant string used for separating different sections of quiz in the command line, to make the program look neater and easier to follow.|
|`question_file`|str|Stores the name of the file to retrieve question data from.|
|`question_texts`|list[tuple[str,str]|A list of tuples with question details to be used for `gen_questions_csv`. The first value in each tuple is the text for the question, with the column to get values from in curly brackets. The second value is the name of the column the answer will be in.|
|`selected_difficulty`|str|Initialized as an empty string, but will be changed to the user's difficulty selection when they input one. It's reset to an empty string if the user doesn't input a valid option.|
|`question_list`|list[Question]|Initialized as an empty list, then populated with Question objects after the user selects a difficulty. It's then used for `run_quiz`.|
|`replay_input`|str|Stores the user's input for whether they want to play again or not.|

## quiz_utils
This is where the bulk of the program takes place. I decided to store question details in classes so multiple of them could easily be put in a list and run in turn.

### `Question` class
This is the base class for question details, as well as the one used directly for free text input questions.

#### Attributes
|Name|Type|Description|
|----------|-------|--------|
|`question`|str|The text for the question to be asked.|
|`answers`|list[str]|The correct answer(s) for the question. It's a list in case there are multiple correct ones.|

#### `Question.ask()`
This function asks the user the question and checks the given answer by performing the following steps:
1. Display the question text.
2. Prompt the user to input an answer.
3. If the user's answer is in the correct answer list (both having been converted to lowercase with `.lower()`, notify them that they were correct and return 1.
4. Otherwise, inform the user what the correct answer was and return 0.

##### Variables within `Question.ask()`
|Name|Type|Description|
|----------|-------|--------|
|`user_answer`|str|The answer input by the user, which is then validated to determine if it's correct or not.|

### `MultiChoiceQuestion` class
This class is a child of Question tailored for multiple choice questions.

#### Attributes
|Name|Type|Description|
|----------|-------|--------|
|`question`|str|The text for the question to be asked.|
|`answers`|list[str]|The correct answer(s) for the question. It's a list in case there are multiple correct ones.|
|`wrong_answers`|list[str]|Other (incorrect) options for the question.|

#### Raises
|Error|Condition|
|--------|--------|
|`ValueError`|Raised when initiating a MultiChoiceQuestion object if the combined length of correct and incorrect answer lists is higher than 26. If it were higher, there would not be enough letters to label them all.|

#### `MultiChoiceQuestion.ask()`
The multiple choice version of `.ask()` that displays the available options and loops until the user selects one of them. It performs the following steps:
1. Create a combined list of correct and incorrect answers and shuffle the list.
2. Save the shuffled list as values in a dictionary, with alphabetical keys generated from the `ascii_lowercase` alphabet string.
3. Place the dictionary keys and values into format strings, then combine them together with the question text to get the full text to display.
4. Display the question text.
5. Have the user input an option. This will repeat until the key or value for one of the options is input.
6. If the input is the key/value for a correct answer, notify the user they are correct and return 1. If it's for a valid option but an incorrect answer, inform the user of the correct answer and return 0.

If the user somehow ends the while loop without the function returning a value yet, it will return 0. This shouldn't happen, though.

##### Variables within `MultiChoiceQuestion.ask()`
|Name|Type|Description|
|----------|-------|--------|
|`all_options`|list[str]|A combined list of the question's correct and incorrect answers.|
|`option_list`|dict{str:str}|Initializes as an empty dictionary, before being populated with keys from `ascii_lowercase` and values from `all_options`.|
|`full_question_text`|str|The full text for the question, constructed from the object's `question` attribute and `option_list`.|
|`valid_input`|bool|Initializes as False, and is set to True when the user inputs a valid option. This will end the while loop.|

### `run_quiz()` function

#### Arguments

#### Raises

#### Variables within `run_quiz()`

### `extract_placeholders()` function

#### Arguments

### `gen_questions_csv()` function

#### Arguments

#### Raises

#### Variables within `gen_questions_csv()`
