import random  # Import the random module for random selection
import os  # Import the os module for operating system dependent functionality

class LearnTopic:
    def __init__(self, flashcard_dict, deck):
        """
        Initialize the LearnTopic with the flashcard dictionary and deck instance.
        Args:
            flashcard_dict (dict): Dictionary of flashcards for the topic.
            deck (Deck): Instance of the Deck class.
        """
        self.dict = flashcard_dict  # Store the flashcard dictionary
        self.deck = deck  # Store the deck instance
        self.numberofcards = len(flashcard_dict)  # Get the number of flashcards in the topic
        self.correct_answers = 0  # Initialize correct answers counter
        self.wrong_answers = 0  # Initialize wrong answers counter
        self.finished_cards = 0  # Initialize finished cards counter
        self.previous_result = ""  # Initialize storage for previous result (currently unused)

    def still_has_flashcards(self):
        """
        Check if there are flashcards left to learn.
        Returns:
            bool: True if there are flashcards left to learn, False otherwise.
        """
        # Return True if any flashcard's progress is less than 3, meaning it still needs to be reviewed
        return any(card[1] < 3 for card in self.dict.values())

    def choose_card(self):
        """
        Select a flashcard at random for the user to learn.
        Returns:
            tuple: The key and front text of the chosen flashcard.
        """
        # Get a list of flashcards with progress less than 3
        available_flashcards = [key for key, value in self.dict.items() if value[1] < 3]
        if not available_flashcards:  # If no flashcards are available
            return None, None  # Return None, None

        # Select a random flashcard key from the available flashcards
        mykey = random.choice(available_flashcards)
        return mykey, self.dict[mykey][0]  # Return the key (question) and the answer of the chosen flashcard

    def update_card_progress(self, key, knew_answer):
        """
        Update the progress of the selected flashcard based on the user's answer.
        Args:
            key (str): The key of the flashcard.
            knew_answer (bool): Whether the user knew the answer or not.
        """
        if knew_answer:  # If the user knew the answer
            self.dict[key][1] += 1  # Increment the progress of the flashcard
            self.correct_answers += 1  # Increment the correct answers counter
            if self.dict[key][1] == 3:  # If the progress reaches 3
                self.finished_cards += 1  # Increment the finished cards counter
        else:  # If the user didn't know the answer
            if self.dict[key][1] > 0:  # If the progress is greater than 0
                self.dict[key][1] -= 1  # Decrement the progress of the flashcard
            self.wrong_answers += 1  # Increment the wrong answers counter
        self.deck.save_deck_json()  # Save the updated progress to the JSON file

