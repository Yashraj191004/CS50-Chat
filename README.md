*/
# CS50Chat

#### Description:

CS50Chat is a real-time messaging platform that enables users to communicate privately with each other. It features a clean, modern, and intuitive user interface, making it easy for users to send and receive messages, and manage their accounts.

**Key Technologies and Structure:**

- **Flask** is used as the web framework, with Jinja2 for dynamic HTML templates.
- **SQLite** (via the CS50 SQL library) is the database backend.
- **User authentication** uses hashed and salted passwords for security.
- **Session management** is handled securely with Flask-Session.
- **Modern UI**: The interface uses Bootstrap and custom CSS for a dark theme with readable, light-colored message bubbles.
- **Database schema** is simplified and robust, with two tables:
    - `users`: Stores usernames and password hashes.
    - `messages`: Stores message content, sender, recipient, and timestamp.
- **Security**: All user input is validated, and passwords are stored securely.
- **Messaging**: Users can send private messages to each other. Each message clearly displays the sender and recipient, with timestamps.
- **User Experience**: The application is responsive and works well on both desktop and mobile devices.

**Design Choices and Improvements:**

- The database schema was streamlined for clarity and maintainability. All message metadata (sender, recipient, timestamp) is stored directly in the `messages` table.
- The UI was modernized: chat bubbles for your own messages are now white or light gray with dark text for high readability, while the background remains dark for contrast.
- All redundant or unused code, CSS, and assets were removed for maintainability.
- The application uses clear error messages and feedback for user actions (like registration, login, or sending messages).
- Security best practices are followed throughout (hashed passwords, session protection, input validation).
- While the original plan included group messaging and real-time updates via WebSockets (using Flask-SocketIO), the current version focuses on robust, secure, and user-friendly private messaging.

**File Structure:**

- `app.py`: Main application script, defines routes, handles user authentication, message sending, and rendering templates.
- `templates/`: Contains all HTML templates, using Jinja2 for dynamic content.
- `static/styles.css`: Contains all custom CSS for the modern, readable UI.
- `schema.sql`: SQL file for initializing the database with the correct tables and default values.

**How to Run:**

1. Initialize the database with `sqlite3 chat.db < schema.sql`.
2. Install dependencies with `pip install -r requirements.txt`.
3. Run the app with `flask run`.
4. Access CS50Chat in your browser at `http://localhost:5000`.

**Summary:**
CS50Chat is a secure, modern, and easy-to-use messaging platform built with Flask and SQLite. It features a clean interface, strong security, and a maintainable codebase, making it a solid foundation for further real-time features or group chat extensions.
/*
