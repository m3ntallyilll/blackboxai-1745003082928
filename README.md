
Built by https://www.blackbox.ai

---

```markdown
# Bean Genie Bot

## Project Overview
Bean Genie Bot is a powerful Discord bot tailored for Bigo Live streamers, designed to facilitate currency conversion, track streamer progress, manage event participation, provide growth strategies, and simulate credit score checks. The bot uses advanced command processing capabilities, leveraging natural language input to enhance user interaction.

## Installation

### Prerequisites
- Python 3.7 or higher
- Pip (Python package installer)

### Step-by-Step Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/bean-genie-bot.git
   cd bean-genie-bot
   ```
2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```
   If `requirements.txt` is not provided, manually install the dependencies listed below.

3. **Set up environment variables:**
   Create a `.env` file in the root directory and add your `GROQ_API_KEY`:
   ```plaintext
   GROQ_API_KEY=your_actual_api_key_here
   ```

4. **Initialize the database:**
   The bot includes an SQLite database (`chat_memory.db`). The database is automatically initialized upon running the application for the first time.

5. **Run the bot:**
   From the command line, you can run the bot CLI or the web interface:
   - For CLI:
     ```bash
     python bean_genie_bot.py
     ```
   - For Web UI:
     ```bash
     python web_ui.py
     ```

## Usage
To interact with the bot, you can use commands prefixed with `!`. Here are a few examples:
- `!convert beans 1000`
- `!track 10000 50`
- `!events`
- `!growth instagram`

### Web UI
Access the web interface by navigating to `http://localhost:5000` in your web browser. Sign up or log in to the system and start chatting with the bot directly through the web app.

## Features
- **Currency Conversion:** Easily convert between beans, diamonds, and USD.
- **Progress Tracking:** Check your current status and next tier requirements based on beans earned and hours streamed.
- **Event Management:** See upcoming events and join them.
- **Growth Strategies:** Get tailored strategies for multiple platforms including Instagram, TikTok, and YouTube.
- **Sponsorship Information:** Find out what sponsorship tier you're eligible for based on follower count.
- **Wishlist Guide:** Get a guide on how to set up an Amazon wishlist.
- **Credit Score Simulation:** Check a simulated credit score to see loan eligibility.

## Dependencies
The project uses the following main dependencies:
- `flask`: For building the web application
- `werkzeug`: For hashing passwords and handling server functionalities
- `pydantic`: For data validation and parsing commands
- `groq`: To interact with Groq API
- `python-dotenv`: For loading environment variables from a `.env` file
- `sqlite3`: For database operations (included in Python standard library)

Please ensure to have all these packages installed. If using `pip`, a `requirements.txt` can be created with the specific versions.

## Project Structure
```
bean-genie-bot/
│
├── bean_genie_bot.py    # Main bot logic and command processing
├── web_ui.py             # Flask web application for user interaction
├── chat_memory.db        # SQLite database for storing chat messages
├── requirements.txt       # List of Python dependencies (optional)
└── .env                  # Environment variables configuration
```

## Contributing
Contributions are welcome! Please submit your pull requests, or report issues via GitHub.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```