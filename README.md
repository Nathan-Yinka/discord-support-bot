# Discord Support Bot

The Discord Support Bot is designed to streamline the support process in a Discord server. It includes features such as ticket creation, issue selection, and linking to relevant resources to assist users effectively.

## Features

- **Ticket System**: Automatically creates ticket channels with unique numbering and access permissions for support staff and users.
- **Issue Selection**: Allows users to select predefined issues and provides links to relevant resources.
- **Slash Commands**: Easy-to-use slash commands for interacting with the bot.
- **Extensible Architecture**: Built using the `discord.py` library with cogs for modular functionality.

---

## Requirements

- Python 3.8 or higher
- A Discord Bot Token (from the Discord Developer Portal)
- The `discord.py` library version 2.x
- Any additional dependencies listed in `requirements.txt`

---

## Setup

### 1. Clone the Repository
```bash
git https://github.com/Nathan-Yinka/discord-support-bot.git
cd discord-support-bot
```

### 2. Install Dependencies
Use pip to install the required Python libraries:
```bash
pip install -r requirements.txt
```

### 3. Configure the .env
Create a .env file in the root directory and add the following:
```python
BOT_TOKEN = "your-discord-bot-token"
```
Replace "your-discord-bot-token" with your actual Discord Bot Token.




## How to Run the Bot

### On macOS
1. Open a terminal.
2. Navigate to the bot directory:
```bash
cd /path/to/discord-support-bot
```
3. Run the bot:
```bash
python main.py
```

### On Windows
1. Open Command Prompt.
2. Navigate to the bot directory:
```bash
cd /path/to/discord-support-bot
```
3. Run the bot:
```bash
python main.py
```

### Using Docker

1. Build the Docker image
```bash
docker build -t discord-support-bot .
```

2. Run the bot container:
```bash
docker run -e BOT_TOKEN=your-discord-bot-token discord-support-bot
```
Make sure to replace your-discord-bot-token with your actual token.

---

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---