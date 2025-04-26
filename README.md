# 🤖 Discord Bot with Supabase Integration

This Discord bot integrates with Supabase to provide user information retrieval and verification functionality.

## 🛠️ Features

- `/ping`: Display bot latency
- `/get`: Retrieve user information from Supabase
- `/verify`: Send verification embed messages

## 🚀 Setup

1. Clone the repository
2. Create a `.env` file with the following variables:
   ```
   TOKEN=your_discord_bot_token
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
   SUPABASE_SERVICE_ROLE_KEY=your_supabase_key
   ROLE_ID=your_discord_role_id
   ```
3. Install dependencies: `pip install -r requirements.txt`
4. Run the bot: `python main.py`

## 💬 Commands

### 🔔 /ping
Displays the current latency of the bot.

### 🔍 /get
Retrieves user information from the Supabase database.
- Required parameter: `user_id`
- Appropriate role permissions required

### ✓ /verify
Creates a verification embed with a button link.
- Required parameters: `title`, `description`, `link`, `button_text`
- Appropriate role permissions required
