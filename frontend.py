import tkinter as tk
import backend

class ChatbotInterface(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.title("lawful.ly")
        self.geometry("400x600")
        self.configure(bg="#1E3A5F")  # Deep Blue background for the window

        # Header
        header_frame = tk.Frame(self, bg="#1E3A5F", pady=10)  # Deep Blue header background
        header_frame.pack(fill="x")

        # Header label with White or Light Gold text
        self.header_label = tk.Label(
            header_frame, text="lawful.ly!", 
            font=("Bahnschrift Light SemiCondensed", 22, "bold"), 
            bg="#1E3A5F", fg="#FFD700"  # Initial Light Gold text color
        )
        self.header_label.pack()

        # Elegant color change effect
        self.shine_header()

        # Chat area frame
        chat_frame = tk.Frame(self, bg="#1E3A5F")  # Set same Deep Blue background
        chat_frame.pack(fill="both", expand=True)

        # Chat display area (Read-only Text widget)
        self.chat_display = tk.Text(
            chat_frame, wrap="word", state="disabled", 
            bg="#FFD700", fg="white",  # White text color as default
            font=("Bahnschrift Light SemiCondensed", 12), padx=10, pady=10
        )
        self.chat_display.pack(fill="both", expand=True, padx=5, pady=5)

        # Entry frame for user input
        entry_frame = tk.Frame(self, bg="#1E3A5F")  # Match the Deep Blue background
        entry_frame.pack(fill="x", side="bottom", pady=10)

        # User input entry field
        self.user_entry = tk.Entry(
            entry_frame, font=("Bahnschrift Light SemiCondensed", 20), bg="white", fg="#1E3A5F",  # Deep Blue text color
            relief="flat"
        )
        self.user_entry.pack(fill="x", padx=10, pady=5)
        self.user_entry.bind("<Return>", self.send_message)

        # Send button
        send_button = tk.Button(
            entry_frame, text="Send", font=("Bahnschrift Light SemiCondensed", 16),
            bg="#FFD700", fg="#1E3A5F", relief="flat", command=self.send_message
        )
        send_button.pack(side="right", padx=10, pady=5)

        # Display a welcome message from the bot on startup
        welcome_message = (
            "Welcome to lawful.ly: Your Legal Digest! "
            "\nThis project is designed to help you navigate complex legal articles with ease. "
            "\nSimply type in your query, and I’ll assist you by summarizing legal documents and answering any questions you may have. "
            "\nLet’s make legal research simpler and more accessible!"
        )
        self.display_message("Bot", welcome_message, user=False)

    def shine_header(self):
        # Elegant color transition effect: Change color gradually between Gold and Silver
        current_fg = self.header_label.cget("fg")
        new_fg = "#FFD700" if current_fg == "#C0C0C0" else "#C0C0C0"  # Transition between Gold and Silver
        self.header_label.config(fg=new_fg)
        self.after(1500, self.shine_header)  # Change color every 1500ms (1.5 seconds)

    def send_message(self, event=None):
        user_message = self.user_entry.get()
        if user_message.strip():
            self.display_message("You", user_message, user=True)
            self.user_entry.delete(0, tk.END)
            
            # Gather all messages from the chat_display
            self.chat_display.configure(state="normal")
            all_messages = self.chat_display.get("1.0", "end-1c")
            self.chat_display.configure(state="disabled")
            
            # Prepare the context for the backend
            context = "system: You are a Chatbot designed to legally assist users. Right now you are running inside of a tkinter window, so no Markdown Syntax please.\n"
            lines = all_messages.split("\n")
            for line in lines:
                if line.startswith("You: "):
                    context += "user: " + line[5:] + "\n"
                elif line.startswith("Bot: "):
                    context += "bot: " + line[5:] + "\n"
        
        # Call the backend function to get the bot's response
        bot_response = backend.get_response(context)
        self.display_message("Bot", bot_response, user=False)


    def display_message(self, sender, message, user):
        # Insert messages with distinct text colors for user and bot
        self.chat_display.configure(state="normal")
        
        # Insert sender label and message text
        self.chat_display.insert("end", f"{sender}: ", ("sender",))
        self.chat_display.insert("end", f"{message}\n\n", ("user_message" if user else "bot_message",))

        # Configuring tag styles for each message type
        self.chat_display.tag_config("sender", font=("Bahnschrift", 18, "bold"), foreground="#1E3A5F")
        self.chat_display.tag_config("user_message", font=("Bahnschrift Light SemiCondensed", 18), foreground="black")  # Teal for user
        self.chat_display.tag_config("bot_message", font=("Bahnschrift Light SemiCondensed", 18), foreground="black")      # Black for bot
        
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")  # Auto-scroll to the end

if __name__ == "__main__":
    app = ChatbotInterface()
    app.mainloop()
