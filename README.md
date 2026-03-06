# Postcode Area Quiz
# Introduction
This app is a quiz for improving knowledge on UK postcode areas by asking randomly generated questions until you run out of lives. The first questions ask you to pick from only 4 random options, but as you score more points you'll be asked to pick from a complete list of options and eventually type answers yourself with no hints provided!

## Setup instructions
The app currently can only run locally, so you'll have to install and run it yourself.
### 1. Clone the repository
Using your terminal/command line, navigate to the folder you want to save the repository to and use:
```
git clone https://github.com/WhileTrueDoNothing/programming-summative-quiz
```
### 2. Install dependencies
```
pip install -r requirements.txt
```
### 3. Run the project
Navigate to the app's folder and run it with:
```
streamlit run main.py
```
It takes a few seconds to start, but it'll then open in a tab in your browser.
# Design
## Requirements
### Must
The application must:
- Generate questions randomly from the postcode data.
- Save and store user scores so they can be accessed later.
- Validate user name inputs to ensure they don't contain numbers or symbols.
- Either end the quiz or reset the data if all question data has been used.
### Should
The application should:
- Display the leaderboard as a graph.
- Contain a widget explaining how to play the game.
- Use a contrasting colour palette tested with a colour blindness simulator.
- Ensure that questions don't accidentally provide a correct answer as an incorrect option. (for example, if both SW and EC were labelled London, if SW was the intended answer then EC should either not be a selectable option or accepted as correct.)
### Could
The application could:
- Become more difficult once the user scores enough points by offering a selection menu of all options instead of just 4.
- Become even more difficult for high scoring users by switching to just a free text input.
### Won't
(This version of the application) Won't:
- Utilize postcode district data for questions. That dataset is too large and complex to be worth implementing at this stage.
- Differentiate between users with the same score by other metrics. Choosing and implementing an alternative metric takes time, and I have higher priority tasks.
- Score users based on the time they take to answer (to deter them from googling it). The time it could take to implement the system and find ideal time limits outweighs the value it could bring.

## Initial plans
Here are the initial plans for the quiz's interface that I drew in my notebook.
[INSERT PHOTOS OF THAT HERE]

## Prototype
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
# Development
## quiz_utils module
I began development with the quiz_utils module, as a lot of the code could be reconstructed from the quiz's command line version. I first constructed a basic class diagram to plan my classes and their functions, with plans to amend it during development, should I need to.

<img width="796" height="518" alt="A draw.io diagram with details on the User, LeaderboardManager, Question and QuestionGenerator classes." src="https://github.com/user-attachments/assets/910f75be-7cdb-4e17-8a35-fda432d2c097" />

### Question
I developed Question first. Classes like QuestionGenerator relied on it's existence, and the specifics of many other app elements depended on the way I decided to implement it.

<img width="1294" height="653" alt="image" src="https://github.com/user-attachments/assets/8f45cb1f-6018-4869-838e-45c3a08ab90c" /><img width="1306" height="545" alt="image" src="https://github.com/user-attachments/assets/415ca9e6-da9a-4c2f-b597-cf7eb7aee785" /><img width="1481" height="254" alt="image" src="https://github.com/user-attachments/assets/d644ea67-a82a-4ebd-a01f-09b6e0d09621" />

Alongside the question's text and correct answers, I decided to store the name of the column used for the answer. This allows the QuestionGenerator to generate incorrect multiple choice answers without needing to store them in the class itself. If I later utilize a selectbox widget with all potential answer options, it'll allow for easy retrieval of the correct column from the QuestionGenerator's DataFrame.

I added allow_multiple_correct slightly later, upon realising the QuestionGenerator needed to know all potential answers to the given question, even if only one were to be displayed. If a single value was stored, other correct values could be selected as "incorrect" options. With allow_multiple_correct set to False, the Question will store all potential answers to avoid this, while only outputting the first answer if a single one is needed.

### QuestionGenerator
This is the most complicated class in the backend, requiring many methods to manage its DataFrame and generate Questions.

<img width="1385" height="1079" alt="image" src="https://github.com/user-attachments/assets/78bf4de5-1cd5-4dae-8cab-a31512261a92" /><img width="765" height="224" alt="image" src="https://github.com/user-attachments/assets/747007cb-8717-45b1-b022-09afe5d94019" />

The get_colnames_from_text method extracts the column(s) to use for a question based on the placeholders in its format string. Without it, I'd have to store those values in another variable.

<img width="1120" height="252" alt="image" src="https://github.com/user-attachments/assets/fdad91cd-6e6d-4315-a0f0-52673628b60c" />

While I had planned to only initialize DataFrames from CSV files, I realised that allowing a DataFrame to be input directly would make testing easier. Breaking down the question generation functions into smaller, more specific methods also helped with this. The command line quiz generated all its questions in a single, overly-complicated function. QuestionGenerator instead contains a method to generate a Question from a specific row and a method to mark a specific row as used, which can both be easily tested. They can then both be called by another method that selects the random row and details they are to use.

<img width="1110" height="358" alt="image" src="https://github.com/user-attachments/assets/a9065693-b528-4ecb-a48f-6d8655efee6b" /><img width="1588" height="823" alt="image" src="https://github.com/user-attachments/assets/c446765c-5828-4d5a-b131-79ee9151700a" /><img width="1591" height="814" alt="image" src="https://github.com/user-attachments/assets/fac88795-c7dc-4d33-a1cd-79514129bded" />

The gen_alt_options method relies on the Question's allow_multiple_correct attribute to handle duplicates in the question or answer columns. When calculating the number of options it needs to generate, it'll only count the Question's "valid" answer(s). However, when selecting potential alternative options, it ignores *all* potential correct answers, regardless of allow_multiple_correct's value. This prevents it from selecting an "incorrect" option that's actually correct.

<img width="1492" height="796" alt="image" src="https://github.com/user-attachments/assets/22367d89-5dbc-408f-93d0-91204924fcd7" />

The reset_used_rows method resets the "row_used" value to False for all rows of the question data. This could potentially be called to continue the quiz if a user answers a question for every item in the dataset.

<img width="930" height="120" alt="image" src="https://github.com/user-attachments/assets/410d6d8e-0042-4092-9038-bbf1d22dd141" />
### User
This class stores and manages details on the current user playing the quiz. My main concern when creating this class was preventing the user's lives from being set to less than zero, to avoid issues displaying lives in the interface. The constructor method throws a ValueError if the initial lives value is 0 or less, to avoid ending the quiz immediately. The User's lives can be set to 0 by the lose_lives method, and will be set to 0 if the subtracted value would be less than that.

<img width="1147" height="626" alt="image" src="https://github.com/user-attachments/assets/4537e3b9-cacf-49d7-aff9-cab63e302774" /><img width="698" height="229" alt="image" src="https://github.com/user-attachments/assets/29dbc0ae-4b39-4329-ae13-36511f6342ad" /><img width="1070" height="411" alt="image" src="https://github.com/user-attachments/assets/ec0d7fc1-bcef-4e0c-8b2a-824f77048a78" />

### LeaderboardManager
This class loads and manages the leaderboard data, currently stored locally in a CSV file. I decided to limit the number of rows in the DataFrame to keep it to a reasonable size. I chose to make the leaderboard chart a Plotly figure for its interactivity and customizeability. I added an option for direct DataFrame input to the class alongside the CSV file, to make it easier to input data from external sources in the future.

<img width="1054" height="612" alt="image" src="https://github.com/user-attachments/assets/5149a4fe-7175-44f1-a893-6ad3a2840870" /><img width="877" height="628" alt="image" src="https://github.com/user-attachments/assets/168ec499-99c4-405b-8bb1-5fbcbd0c33dd" /><img width="707" height="109" alt="image" src="https://github.com/user-attachments/assets/ac33eff5-4433-4ea6-8e01-a780985e096e" />

When saving a new user's results, I've decided to always include them in the DataFrame so they can see themselves on the leaderboard at the end. I achieve this by removing the bottom row from the score data before adding the new row and sorting the DataFrame.

<img width="872" height="264" alt="image" src="https://github.com/user-attachments/assets/244b5787-22cb-4678-afb2-56c6bf69c897" />

### StringInputChecker
This class validates text inputs with its methods. It'll allow me to keep input requirements consistent by only needing to declare them once per object. My only planned use for it is to validate the user's name input.

<img width="1220" height="794" alt="image" src="https://github.com/user-attachments/assets/11708d8f-cb4a-4c47-9080-69f2386c98e3" />

## streamlit frontend
I opted to use Streamlit for the frontend as I'm familiar with the library, and could eventually deploy this project on the community cloud.

# Testing
## Unit Tests
I used pytest to ensure my classes and functions worked as expected. I chose pytest over unittest due to it's easy Github integration and the lack of boilerplate code required when creating tests. I used a separate file for each class to keep my tests organized.

### Question
Question was a fairly simple class to test. I started with a smoke test to ensure things were working properly, then used two almost-identical fixtures to ensure the allow_multiple_correct attribute properly affected the answer checking.

<img width="727" height="1021" alt="image" src="https://github.com/user-attachments/assets/1ab75f21-9203-420e-9a60-15ebe5265179" />

### QuestionGenerator
Adding a direct DataFrame parameter for initializing QuestionGenerators let me run tests with a specially designed DataFrame fixture. By having duplicate values in both columns of ez_maths_df, I could ensure the QuestionGenerator could properly handle questions with multiple correct answers and vice versa.

<img width="1399" height="916" alt="image" src="https://github.com/user-attachments/assets/5cc5ab09-089a-4fce-82b2-8288e947058d" /><img width="1337" height="869" alt="image" src="https://github.com/user-attachments/assets/7b2f9e7c-16ba-4ace-a718-e4175e72aae6" />

It also meant that gen_alt_options would always output the same "random" sample (as only 2 options were valid to select), letting me test against that.

<img width="1174" height="453" alt="image" src="https://github.com/user-attachments/assets/d27b2692-605b-43ec-a7c1-75e3f9d6f88e" />

### User
The tests for this class ensured its attributes were properly initialized and managed by its methods, whether values were provided or defaults were used.

<img width="724" height="898" alt="image" src="https://github.com/user-attachments/assets/cf6167a9-cad9-4d45-bfc5-ee8f93c82799" />

### LeaderboardManager
For these tests, I used pytest's tmp_path functionality to create a dummy CSV file. This let me test the reading/writing functionality of the LeaderboardManager's methods without affecting the real leaderboard file.

<img width="912" height="693" alt="image" src="https://github.com/user-attachments/assets/e0bf1cea-5436-4541-a95c-dcd87fc7ae53" />

### StringInputChecker
I chose a complex regex to use for these tests. It ensures the first chracter is a capital letter, then subsequent characters aren't any of the special characters I listed. It'll still disallow names that start with an accented letter, but these are allowed for subsequent characters. I can allow a far more diverse range of inputs by specifying what to exclude instead of include.

<img width="1279" height="690" alt="image" src="https://github.com/user-attachments/assets/e27a273b-c1a3-4db1-864f-a7951c959847" />



## Evaluation
### Future plans
[insert some stuff about user testing]
[add some stuff about a difficulty increase if I didn't add that]
[improve the regex string to allow for people whose names start with accents n stuff]
