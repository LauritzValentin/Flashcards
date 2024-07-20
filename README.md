# Flash Genius

Flash Genius is a flashcard application designed to help users learn various topics through an interactive graphical interface. The application allows users to create new topics, add flashcards to existing topics, learn flashcards, and track their progress. 

## GitHub

You´ll find the project here: https://github.com/LauritzValentin/Flashcards

## Features

- **Learn Flashcards**: Select a topic and start a learning session where you can answer flashcards. Earn points for each correct answer and mark cards as complete when you've answered correctly three times.
- **Add Flashcards**: Create new topics and add flashcards to them with ease.
- **Reset Progress**: Reset your progress for any topic to start learning from scratch.

## Project Structure

- `deck.py`: Manages loading, saving, and handling the flashcard deck. (Anja)
- `learn_topic.py`: Controls the learning process, tracking progress and providing feedback. (Jana, Isabel, Lauritz)
- `flashcard_app.py`: Implements the graphical user interface and manages user interactions. (Marko, Eric, Jana, Lauritz)
- `initialize.py`: Initializes the flashcard deck by loading data from flash.json. (Anja)
- `flash.json`: JSON file storing flashcard data. (Isabel)
- `main_gui.py`: Run the programme


## Usage

 ### Install the required dependencies:
    tkinter

### Run the programm from main.py


```python
if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
```
### Main Menu

Upon launching the application, you will be presented with the main menu. From here, you can choose to learn flashcards, add new flashcards, or quit the application.

### Learning Flashcards

1. Click on the "Learn" button.
2. Select a topic from the dropdown menu and click "Proceed".
3. If the topic is completed, you will be prompted to reset progress. Otherwise, you will start the learning session.
4. During the session, you will be shown a flashcard and asked if you know the answer. Click "Show Answer" to reveal the answer and then choose whether you knew it or not.

### Adding Flashcards

1. Click on the "Add" button.
2. Select an existing topic or create a new topic.
3. Enter the front and back of the flashcard and click "Add Flashcard".

### Reset Progress

1. Select a topic and click "Reset Progress" to start the learning session from scratch.



