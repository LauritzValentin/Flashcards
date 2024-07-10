import json  # Import the JSON module for handling JSON data

# Define the Deck class to manage the flashcard deck
class Deck:
    def __init__(self, path):
        """
        Initialize the Deck with the given JSON file path.
        Args:
            path (str): The file path to the JSON deck file.
        """
        self._path = path  # Store the file path
        self._deck_dictionary = self._json_to_dict()  # Load the JSON data into a dictionary

    # Private method to load JSON data from the file into a dictionary
    def _json_to_dict(self):
        """
        Load JSON data from the file into a dictionary.
        Returns:
            dict: The deck data loaded from the JSON file.
        """
        try:
            # Open the JSON file for reading with UTF-8 encoding
            with open(self._path, 'r', encoding="utf-8") as fp:
                deck_dict = json.load(fp)  # Load JSON data from the file into a dictionary
            cleaned_deck_dict = self._validate_and_clean_data(deck_dict)  # Validate and clean the loaded data
            return cleaned_deck_dict  # Return the cleaned data
        except (IOError, OSError, FileNotFoundError, PermissionError):
            return {}  # Return an empty dictionary on error
        except json.JSONDecodeError:
            return {}  # Return an empty dictionary on error

    # Private method to validate and clean the JSON data
    def _validate_and_clean_data(self, deck_dict):
        """
        Validate and clean the JSON data to ensure it matches the expected format.
        Args:
            deck_dict (dict): The raw deck data loaded from the JSON file.
        Returns:
            dict: The cleaned deck data.
        """
        for topic, cards in deck_dict.items():  # Iterate through each topic and its cards in the dictionary
            for question, answer in cards.items():  # Iterate through each question and its answer in the topic
                if not isinstance(answer[1], int):  # Check if the progress value is not an integer
                    answer[1] = 0  # Reset the progress value to 0 if it's invalid
        return deck_dict  # Return the cleaned dictionary

    # Private method to check if a topic exists in the dictionary (case-insensitive)
    def _topic_exists(self, topic):
        """
        Check if a topic exists in the dictionary (case-insensitive).
        Args:
            topic (str): The name of the topic to check.
        Returns:
            bool: True if the topic exists, False otherwise.
        """
        return topic.lower() in (t.lower() for t in self._deck_dictionary)  # Return True if the topic exists

    # Private method to get the actual topic name matching the case-insensitive input
    def _get_actual_topic_name(self, topic):
        """
        Get the actual topic name matching the case-insensitive input.
        Args:
            topic (str): The name of the topic to match.
        Returns:
            str or None: The actual topic name if found, otherwise None.
        """
        for t in self._deck_dictionary:  # Iterate through the topics in the dictionary
            if t.lower() == topic.lower():  # Check if the topic matches the input (case-insensitive)
                return t  # Return the actual topic name
        return None  # Return None if the topic is not found

    # Public method to save the current state of the dictionary back to the JSON file
    def save_deck_json(self):
        """
        Save the current state of the dictionary back to the JSON file.
        Returns:
            bool: True if the save was successful, False otherwise.
        """
        try:
            # Open the JSON file for writing with UTF-8 encoding
            with open(self._path, 'w', encoding="utf-8") as fp:
                json.dump(self._deck_dictionary, fp, indent=4)  # Save the dictionary to the JSON file with indentation
            return True  # Return True if the save was successful
        except (IOError, OSError, FileNotFoundError, PermissionError):
            return False  # Return False on error

    @property  # Define a property method to get the list of available topics
    def get_topic_list(self):
        """
        Get the list of available topics.
        Returns:
            list: A list of topic names.
        """
        return list(self._deck_dictionary.keys())  # Return the list of topic names

    # Public method to get the flashcards and progress for a specific topic
    def get_topic_dictionary(self, topic):
        """
        Get the flashcards and progress for a specific topic.
        Args:
            topic (str): The name of the topic to retrieve.
        Returns:
            dict: The flashcards and progress for the specified topic.
        """
        actual_topic = self._get_actual_topic_name(topic)  # Get the actual topic name
        if actual_topic:  # Check if the topic exists
            return self._deck_dictionary[actual_topic]  # Return the flashcards and progress for the topic
        return {}  # Return an empty dictionary if the topic does not exist

    # Public method to check if a topic exists
    def topic_exists(self, topic):
        """
        Check if a topic exists.
        Args:
            topic (str): The name of the topic to check.
        Returns:
            bool: True if the topic exists, False otherwise.
        """
        return self._topic_exists(topic)  # Return True if the topic exists

    # Public method to create a new topic in the dictionary
    def new_topic_dictionary(self, topic):
        """
        Create a new topic in the dictionary.
        Args:
            topic (str): The name of the new topic.
        Returns:
            bool: True if the topic was created, False if it already exists.
        """
        if self._topic_exists(topic):  # Check if the topic already exists
            return False  # Return False if the topic exists
        else:
            self._deck_dictionary[topic] = {}  # Create a new empty topic
            return True  # Return True if the topic was created

    # Public method to update the flashcards and progress for an existing topic
    def update_topic_dictionary(self, topic, card_front, card_back):
        """
        Update the flashcards and progress for an existing topic.
        Args:
            topic (str): The name of the topic.
            card_front (str): The front text of the flashcard.
            card_back (str): The back text of the flashcard.
        Returns:
            bool: True if the topic was updated, False if the topic does not exist.
        """
        actual_topic = self._get_actual_topic_name(topic)  # Get the actual topic name
        if actual_topic:  # Check if the topic exists
            if actual_topic not in self._deck_dictionary:  # Check if the topic is not in the dictionary
                self._deck_dictionary[actual_topic] = {}  # Initialize an empty dictionary for the topic
            # Add or update the flashcard with progress 0
            self._deck_dictionary[actual_topic][card_front] = [card_back, 0]
            return True  # Return True if the topic was updated
        return False  # Return False if the topic does not exist

    # Public method to add a new flashcard to a topic
    def add_new_flashcard(self, topic, card_front, card_back):
        """
        Add a new flashcard to a topic.
        Args:
            topic (str): The name of the topic.
            card_front (str): The front text of the flashcard.
            card_back (str): The back text of the flashcard.
        """
        self.update_topic_dictionary(topic, card_front, card_back)  # Update the topic with the new flashcard

    # Public method to reset the progress of all flashcards in a topic
    def reset_progress(self, topic):
        """
        Reset the progress of all flashcards in a topic.
        Args:
            topic (str): The name of the topic to reset.
        Returns:
            bool: True if the progress was reset, False if the topic does not exist.
        """
        actual_topic = self._get_actual_topic_name(topic)  # Get the actual topic name
        if actual_topic:  # Check if the topic exists
            for key in self._deck_dictionary[actual_topic]:  # Iterate through each flashcard in the topic
                self._deck_dictionary[actual_topic][key][1] = 0  # Reset progress to 0 for all flashcards
            return True  # Return True if the progress was reset
        return False  # Return False if the topic does not exist
