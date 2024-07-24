import tkinter as tk  # Import the tkinter library for GUI
from tkinter import messagebox  # Import messagebox for displaying messages
from initialize import mydeck  # Import the 'mydeck' object from initialize module
from learn_topic import LearnTopic  # Import the LearnTopic class from learn_topic module


class FlashcardApp:
    def __init__(self, root):
        self.root = root  # Initialize the root window
        self.root.title("Flash Genius")  # Set the title of the window
        self.root.configure(bg='white')  # Set the background color of the window to white

        self.deck = mydeck  # Assign the 'mydeck' object to self.deck
        self.current_topic = None  # Initialize current_topic to None
        self.learn_topic = None  # Initialize learn_topic to None
        self.current_question = None  # Initialize current_question to None
        self.current_answer = None  # Initialize current_answer to None

        self.create_main_menu()  # Call the create_main_menu method to initialize the main menu

    def clear_window(self):
        """
        Clears all widgets from the root window.
        """
        for widget in self.root.winfo_children():
            widget.destroy()  # Destroy each widget within the root window

    def create_main_menu(self):
        """
        Creates the main menu GUI with logo, options, and buttons.
        """
        self.clear_window()  # Clear the window before creating the main menu

        logo_image = tk.PhotoImage(file="image.png")  # Load logo image from file
        tk.Label(self.root, image=logo_image, bg='white').pack(pady=10)  # Display logo image on the window
        self.root.logo_image = logo_image  # Store the logo image reference in the root

        tk.Label(self.root, text="What would you like to do?", font=("Helvetica", 24, "bold"), fg='pink',
                 bg='white').pack(pady=20)  # Main menu label
        tk.Button(self.root, text="learn", command=self.start_learning, bg='#ff66b2', fg='black',
                  font=("Helvetica", 20), height=2, width=15).pack(pady=10)  # Learn button
        tk.Button(self.root, text="add", command=self.add_flashcards, bg='#ffb380', fg='black', font=("Helvetica", 20),
                  height=2, width=15).pack(pady=10)  # Add flashcards button
        tk.Button(self.root, text="quit", command=self.root.quit, bg='#666666', fg='white', font=("Helvetica", 20),
                  height=2, width=15).pack(pady=10)  # Quit button

    def start_learning(self):
        """
        Initiates the learning process by choosing a topic.
        """
        self.topics = self.deck.get_topic_list  # Get the list of topics from the deck
        if not self.topics:  # If no topics are available
            messagebox.showinfo("Info", "No topics available to learn.")  # Display info message
            return
        self.choose_topic("learn")  # Proceed to choose a topic for learning

    def add_flashcards(self):
        """
        Allows user to add flashcards to a chosen topic.
        """
        self.topics = self.deck.get_topic_list  # Get the list of topics from the deck
        self.choose_topic("add")  # Proceed to choose a topic for adding flashcards

    def choose_topic(self, action):
        """
        Allows user to choose a topic from the dropdown menu.
        Args:
            action (str): Specifies the action to be performed ('learn' or 'add').
        """
        self.clear_window()  # Clear the window before displaying topic selection

        tk.Label(self.root, text="Choose a topic", font=("Helvetica", 20), bg='white').pack(
            pady=20)  # Topic selection label
        tk.Label(self.root, text="Click on the dropdown menu to see the list of topics.", font=("Helvetica", 14),
                 bg='white').pack(pady=5)  # Instruction label

        topic_var = tk.StringVar(self.root)  # Variable to hold the selected topic
        topic_var.set("Dropdown Menu")  # Default text for the dropdown menu

        if action == "add":
            topic_options = self.topics + ["Create new topic"] if self.topics else [
                "Create new topic"]  # Add 'Create new topic' option if adding flashcards
        else:
            topic_options = self.topics  # Use existing topics for learning

        tk.OptionMenu(self.root, topic_var, *topic_options).pack(pady=10)  # Dropdown menu for selecting topics

        def proceed():
            """
            Function called when the 'Proceed' button is clicked.
            Retrieves the selected topic and takes appropriate action based on the chosen action.
            """
            chosen_topic = topic_var.get()  # Get the selected topic from the dropdown menu
            if action == "add" and chosen_topic == "Create new topic":  # If 'Create new topic' is selected when adding flashcards
                self.create_new_topic(action)  # Proceed to create a new topic
            elif chosen_topic == "Dropdown Menu":  # If no topic is selected
                if action == "learn":
                    self.choose_topic("learn")  # Stay at the choosing topic menu
                    messagebox.showinfo("Info",
                                        "You need to choose one of the topics in the Dropdown Menu!")  # Show prompt to choose valid topic
                elif action == "add":
                    self.choose_topic("add")  # Stay at the choosing topic menu
                    messagebox.showinfo("Info",
                                        "You need to choose one of the topics in the Dropdown Menu!")  # Show prompt to choose valid topic
            else:
                self.current_topic = chosen_topic  # Set the current topic to the chosen topic
                if action == "learn":
                    self.confirm_reset_or_start()  # Proceed to confirm reset or start learning
                elif action == "add":
                    self.add_flashcard_to_topic()  # Proceed to add flashcards to the chosen topic

        tk.Button(self.root, text="Proceed", command=proceed, bg='#ff66b2', fg='black', font=("Helvetica", 18)).pack(
            pady=10)  # Proceed button
        tk.Button(self.root, text="Back", command=self.create_main_menu, bg='#ff66b2', fg='black',
                  font=("Helvetica", 18)).pack(pady=5)  # Back button

    def create_new_topic(self, action):
        """
        Allows user to create a new topic.
        Args:
            action (str): Specifies the action to be performed ('learn' or 'add').
        """
        self.clear_window()  # Clear the window before displaying new topic creation

        tk.Label(self.root, text="Enter the name of the new topic", font=("Helvetica", 20), bg='white').pack(
            pady=20)  # New topic label
        new_topic_entry = tk.Entry(self.root, width=50,
                                   font=("Helvetica", 14))  # Entry widget for entering new topic name
        new_topic_entry.pack(pady=10)  # Pack the entry widget

        def save_new_topic():
            """
            Function called when 'Save Topic' button is clicked.
            Saves the newly created topic and proceeds accordingly.
            """
            new_topic = new_topic_entry.get().strip()  # Get the entered topic name
            if new_topic:
                if not self.deck.new_topic_dictionary(new_topic):  # Check if the topic already exists
                    messagebox.showinfo("Info", "Topic already exists.")  # Display info message if topic already exists
                else:
                    self.deck.save_deck_json()  # Save the updated deck to JSON file
                    messagebox.showinfo("Info",
                                        f"Topic '{new_topic}' created successfully!")  # Display info message for successful creation
                    self.current_topic = new_topic  # Set the current topic to the newly created topic
                    if action == "add":
                        self.add_flashcard_to_topic()  # Proceed to add flashcards to the new topic
                    elif action == "learn":
                        self.confirm_reset_or_start()  # Proceed to confirm reset or start learning

        tk.Button(self.root, text="Save Topic", command=save_new_topic, bg='#ff66b2', fg='black',
                  font=("Helvetica", 18)).pack(pady=10)  # Save topic button
        tk.Button(self.root, text="Back", command=lambda: self.choose_topic(action), bg='#ff66b2', fg='black',
                  font=("Helvetica", 18)).pack(pady=5)  # Back button

    def confirm_reset_or_start(self):
        """
        Allows user to confirm resetting progress or starting learning.
        """
        self.clear_window()  # Clear the window before displaying confirmation

        tk.Label(self.root, text=f"Topic: {self.current_topic}", font=("Helvetica", 20), bg='white').pack(
            pady=20)  # Display current topic
        tk.Button(self.root, text="Start Learning", command=self.check_topic_completion, bg='#ff66b2', fg='black',
                  font=("Helvetica", 18)).pack(pady=5)  # Start learning button
        tk.Button(self.root, text="Reset Progress", command=self.reset_progress, bg='#ff66b2', fg='black',
                  font=("Helvetica", 18)).pack(pady=5)  # Reset progress button
        tk.Button(self.root, text="Back", command=self.create_main_menu, bg='#ff66b2', fg='black',
                  font=("Helvetica", 18)).pack(pady=5)  # Back button

    def reset_progress(self):
        """
        Resets the progress of the current topic.
        """
        self.deck.reset_progress(self.current_topic)  # Reset progress for the current topic
        messagebox.showinfo("Info",
                            f"Progress for topic '{self.current_topic}' has been reset.")  # Display info message
        self.confirm_reset_or_start()  # Proceed to confirm reset or start learning

    def check_topic_completion(self):
        """
        Checks if the topic has any flashcards left to learn.
        """
        self.learn_topic = LearnTopic(self.deck.get_topic_dictionary(self.current_topic),
                                      self.deck)  # Create LearnTopic instance for the current topic
        if not self.learn_topic.still_has_flashcards():  # If no flashcards left to learn
            messagebox.showinfo("Info",
                                f"You have completed the topic '{self.current_topic}'. Please reset the progress to start learning again.")  # Display info message
            self.confirm_reset_or_start()  # Proceed to confirm reset or start learning
        else:
            self.show_learning_instructions()  # Proceed to show learning instructions

    def show_learning_instructions(self):
        """
        Displays learning instructions before starting learning session.
        """
        self.clear_window()  # Clear the window before displaying instructions

        instructions = (
            "Your learning session is about to begin. For each flashcard, you'll earn a point if you know the answer. "
            "If you don't, one point will be deducted. Once you've earned three points for a card, it will be marked as complete."
        )
        tk.Label(self.root, text=instructions, font=("Helvetica", 16), bg='white', wraplength=400).pack(
            pady=20)  # Display learning instructions
        tk.Button(self.root, text="Start Learning", command=self.start_learning_topic, bg='#ff66b2', fg='black',
                  font=("Helvetica", 18)).pack(pady=10)  # Start learning button
        tk.Button(self.root, text="Back", command=self.confirm_reset_or_start, bg='#ff66b2', fg='black',
                  font=("Helvetica", 18)).pack(pady=5)  # Back button

    def start_learning_topic(self):
        """
        Initiates the learning session by starting to show flashcards.
        """
        self.learn_topic = LearnTopic(self.deck.get_topic_dictionary(self.current_topic),
                                      self.deck)  # Create LearnTopic instance for the current topic
        self.show_flashcard()  # Proceed to show the first flashcard

    def show_flashcard(self):
        """
        Displays a flashcard and provides options to show answer or exit.
        """
        if not self.learn_topic.still_has_flashcards():  # If no more flashcards left to show
            self.show_progress(topic_completed=True)  # Show progress (topic completed)
            return

        self.clear_window()  # Clear the window before showing the flashcard

        self.current_question, self.current_answer = self.learn_topic.choose_card()  # Choose a flashcard from the topic
        if self.current_question is None:  # If no flashcards left to show
            self.show_progress(topic_completed=True)  # Show progress (topic completed)
            return

        tk.Label(self.root, text=f"Your flashcard is: {self.current_question}", font=("Helvetica", 20),
                 bg='white').pack(pady=20)  # Display the flashcard question

        answer_frame = tk.Frame(self.root, bg='white')  # Frame to hold answer and buttons
        answer_frame.pack(pady=10)  # Pack the answer frame

        def show_answer():
            """
            Displays the answer to the flashcard and provides options to indicate whether the user knew the answer or not.
            """
            for widget in answer_frame.winfo_children():
                widget.destroy()  # Destroy existing widgets in the answer frame

            tk.Label(self.root, text=f"The answer is: {self.current_answer}", font=("Helvetica", 20), bg='white').pack(
                pady=10)  # Display the answer
            tk.Button(answer_frame, text="I knew this", command=lambda: self.update_and_show_result(True), bg='#ff66b2',
                      fg='black', font=("Helvetica", 18)).pack(side=tk.LEFT, padx=20)  # Button for 'I knew this'
            tk.Button(answer_frame, text="I did not know this", command=lambda: self.update_and_show_result(False),
                      bg='#ff66b2', fg='black', font=("Helvetica", 18)).pack(side=tk.LEFT,
                                                                             padx=20)  # Button for 'I did not know this'
            tk.Button(answer_frame, text="Exit", command=lambda: self.show_progress(topic_completed=False),
                      bg='#ff66b2', fg='black', font=("Helvetica", 18)).pack(side=tk.LEFT, padx=20)  # Exit button

        tk.Button(answer_frame, text="Show Answer", command=show_answer, bg='#ff66b2', fg='black',
                  font=("Helvetica", 18)).pack(pady=10)  # Show answer button

    def update_and_show_result(self, knew_answer):
        """
        Updates the progress of the current flashcard based on whether the user knew the answer or not.
        Args:
            knew_answer (bool): Indicates whether the user knew the answer to the flashcard.
        """
        self.learn_topic.update_card_progress(self.current_question,
                                              knew_answer)  # Update progress based on user response
        self.show_result(knew_answer)  # Proceed to show result

    def show_result(self, knew_answer):
        """
        Displays the result of the user's response to the flashcard.
        Args:
            knew_answer (bool): Indicates whether the user knew the answer to the flashcard.
        """
        self.clear_window()  # Clear the window before displaying result

        achieved_message = ""
        if self.learn_topic.dict[self.current_question][1] == 3:
            achieved_message = "\nThis card is now achieved and will not be shown again until progress is reset."

        if knew_answer:
            if self.learn_topic.dict[self.current_question][1] == 1:
                message = f"Great! You have {self.learn_topic.dict[self.current_question][1]} point for this card.{achieved_message}"  # Positive message
            else:
                message = f"Great! You have {self.learn_topic.dict[self.current_question][1]} points for this card.{achieved_message}"  # Positive message
        else:
            if self.learn_topic.dict[self.current_question][1] == 1:
                message = f"Try to go on! You have {self.learn_topic.dict[self.current_question][1]} point for this card."  # Negative message
            else:
                message = f"Try to go on! You have {self.learn_topic.dict[self.current_question][1]} points for this card."  # Negative message

        tk.Label(self.root, text=message, font=("Helvetica", 20), bg='white').pack(pady=20)  # Display the message
        tk.Button(self.root, text="Next Flashcard", command=self.show_flashcard, bg='#ff66b2', fg='black',
                  font=("Helvetica", 18)).pack(pady=10)  # Next flashcard button
        tk.Button(self.root, text="Exit", command=lambda: self.show_progress(topic_completed=False), bg='#ff66b2',
                  fg='black', font=("Helvetica", 18)).pack(pady=5)  # Exit button

    def show_progress(self, topic_completed=False):
        """
        Displays the progress of the learning session.
        Args:
            topic_completed (bool): Indicates whether the entire topic has been completed.
        """
        self.clear_window()  # Clear the window before displaying progress

        if topic_completed:
            tk.Label(self.root, text="Congratulations! You have completed the topic.", font=("Helvetica", 20),
                     bg='white').pack(pady=20)  # Topic completed message

        tk.Label(self.root, text="Learning Session Complete", font=("Helvetica", 20), bg='white').pack(
            pady=20)  # Session complete message
        tk.Label(self.root, text=f"Correct answers: {self.learn_topic.correct_answers}", font=("Helvetica", 18),
                 bg='white').pack(pady=5)  # Display correct answers
        tk.Label(self.root, text=f"Wrong answers: {self.learn_topic.wrong_answers}", font=("Helvetica", 18),
                 bg='white').pack(pady=5)  # Display wrong answers
        tk.Label(self.root, text=f"Finished flashcards: {self.learn_topic.finished_cards}", font=("Helvetica", 18),
                 bg='white').pack(pady=5)  # Display finished flashcards

        tk.Button(self.root, text="Back to Main Menu", command=self.create_main_menu, bg='#ff66b2', fg='black',
                  font=("Helvetica", 18)).pack(pady=20)  # Back to main menu button

    def add_flashcard_to_topic(self):
        """
        Allows user to add flashcards to the selected topic.
        """
        self.clear_window()  # Clear the window before displaying add flashcard interface

        tk.Label(self.root, text=f"Adding flashcards to {self.current_topic}", font=("Helvetica", 20), bg='white').pack(
            pady=20)  # Label indicating topic for adding flashcards

        tk.Label(self.root, text="Enter the front of the flashcard:", font=("Helvetica", 10), bg='white').pack(
            pady=20)  # Label indicating to add front
        card_front = tk.Entry(self.root, width=50, font=("Helvetica", 14))  # Entry widget for flashcard front
        card_front.pack(pady=10)  # Pack the entry widget
        card_front.insert(0, "")  # Default text for flashcard front

        tk.Label(self.root, text="Enter the back of the flashcard:", font=("Helvetica", 10), bg='white').pack(
            pady=20)  # Label indicating to add back
        card_back = tk.Entry(self.root, width=50, font=("Helvetica", 14))  # Entry widget for flashcard back
        card_back.pack(pady=10)  # Pack the entry widget
        card_back.insert(0, "")  # Default text for flashcard back

        def add_card():
            """
            Function called when 'Add Flashcard' button is clicked.
            Adds a new flashcard to the selected topic.
            """
            front = card_front.get()  # Get the text from flashcard front entry
            back = card_back.get()  # Get the text from flashcard back entry
            if front and back:  # If both front and back are non-empty
                self.deck.add_new_flashcard(self.current_topic, front,
                                            back)  # Add the new flashcard to the selected topic
                self.deck.save_deck_json()  # Save the updated deck to JSON file
                messagebox.showinfo("Info", "Flashcard added successfully!")  # Show success message

            card_front.delete(0, tk.END)  # Clear the flashcard front entry widget
            card_back.delete(0, tk.END)  # Clear the flashcard back entry widget
            card_front.insert(0, "Enter the front of the flashcard")  # Reset default text for flashcard front
            card_back.insert(0, "Enter the back of the flashcard")  # Reset default text for flashcard back

        tk.Button(self.root, text="Add Flashcard", command=add_card, bg='#ff66b2', fg='black',
                  font=("Helvetica", 18)).pack(pady=10)  # Add flashcard button
        tk.Button(self.root, text="Back to Main Menu", command=self.create_main_menu, bg='#ff66b2', fg='black',
                  font=("Helvetica", 18)).pack(pady=5)  # Back to main menu button


