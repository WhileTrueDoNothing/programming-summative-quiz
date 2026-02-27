# Postcode Area Quiz
## Introduction
[insert description of the app here]

## Design
### Initial plans
Here are the initial plans for the quiz's interface that I drew in my notebook.
[INSERT PHOTOS OF THAT HERE]

### Requirements
## Must
The application must:
- Generate questions randomly from the postcode data.
- Save and store user scores so they can be accessed later.
- Validate user name inputs to ensure they don't contain numbers or symbols.
- Either end the quiz or reset the data if all question data has been used.
## Should
The application should:
- Display the leaderboard as a graph.
- Contain a widget explaining how to play the game.
- Use a contrasting colour palette tested with a colour blindness simulator.
- Ensure that questions don't accidentally provide a correct answer as an incorrect option. (for example, if both SW and EC were labelled London, if SW was the intended answer then EC should either not be a selectable option or accepted as correct.)
## Could
The application could:
- Become more difficult once the user scores enough points by offering a selection menu of all options instead of just 4.
- Become even more difficult for high scoring users by switching to just a free text input.
## Won't
(This version of the application) Won't:
- Utilize postcode district data for questions. That dataset is too large and complex to be worth implementing at this stage.
- Differentiate between users with the same score by other metrics. Choosing and implementing an alternative metric takes time, and I have higher priority tasks.
- Score users based on the time they take to answer (to deter them from googling it). The time it could take to implement the system and find ideal time limits outweighs the value it could bring.
### Prototype
I used figma to create a prototype of the user's journey through the quiz. It demonstrates viewing instructions on how to play, entering a user's name, answering a question and the quiz leaderboard updating with their final score. It can be accessed [here](https://www.figma.com/design/uioibs1bjv756tDAnCv9xo/postcode_quiz_ui_prototype?node-id=0-1&t=zjcT6pKWqf88Nzvt-1).
<img width="1186" height="1077" alt="The Figma UI prototype for the quiz, showing the flow between different screens." src="https://github.com/user-attachments/assets/6b433fee-1b68-4114-8511-8fa7dbb06c68" />

I chose teal, orange, black and white as the main interface colours as they're of contrasting hues and follow my company's design brand guidelines. I used [a palette checker](https://palettechecker.com/) to ensure they'd still contrast if a user was colourblind.
<img width="1504" height="768" alt="A colour blindness simulation, showing the colour contrast for 3 common types of colour blindness." src="https://github.com/user-attachments/assets/5efce0bd-65af-471f-add7-6aaa5d0cb2b1" />

### Libraries/Applications used

### Classes and functions
To start with, I had the code from [the command line version of the quiz](https://github.com/WhileTrueDoNothing/programming-formative-quiz). This contained classes for questions, along with functions for generating questions from a given CSV file and running a quiz.

[insert class diagrams for the original code here]

However, most of these were designed for the command line, and needed to be broken down into smaller functions. 

[insert some stuff here about breaking down functions and adding the user class once I do that]

[MAKE FLOWCHARTS FOR SOME KEY FUNCTIONS]
## Development
### quiz_utils module
I began development with the quiz_utils module, as a lot of the code could be reconstructed from the quiz's command line version. I first constructed a basic class diagram to plan my classes and their functions, with plans to amend it during development, should I need to.
<img width="796" height="518" alt="A draw.io diagram with details on the User, LeaderboardManager, Question and QuestionGenerator classes." src="https://github.com/user-attachments/assets/910f75be-7cdb-4e17-8a35-fda432d2c097" />
#### Question
I developed Question first. Classes like QuestionGenerator relied on it's existence, and the specifics of many other app elements depended on the way I decided to implement it.
<img width="1294" height="653" alt="image" src="https://github.com/user-attachments/assets/8f45cb1f-6018-4869-838e-45c3a08ab90c" /><img width="1306" height="545" alt="image" src="https://github.com/user-attachments/assets/415ca9e6-da9a-4c2f-b597-cf7eb7aee785" /><img width="1481" height="254" alt="image" src="https://github.com/user-attachments/assets/d644ea67-a82a-4ebd-a01f-09b6e0d09621" />
Alongside the question's text and correct answers, I decided to store the name of the column used for the answer. This allows the QuestionGenerator to generate incorrect multiple choice answers without needing to store them in the class itself. If I later utilize a selectbox widget with all potential answer options, it'll allow for easy retrieval of the correct column from the QuestionGenerator's DataFrame.

I added allow_multiple_correct slightly later, upon realising the QuestionGenerator needed to know all potential answers to the given question, even if only one were to be displayed. If a single value was stored, other correct values could be selected as "incorrect" options. With allow_multiple_correct set to False, the Question will store all potential answers to avoid this, while only outputting the first answer if a single one is needed.
### streamlit frontend

## Testing
### Unit Tests
I used pytest to ensure my classes and functions worked as expected. I chose pytest over unittest due to it's easy Github integration and the lack of boilerplate code required when creating tests. I used a separate file for each class to keep my tests organized.
####

## Evaluation
### Future plans
[insert some stuff about user testing]
[add some stuff about a difficulty increase if I didn't add that]
