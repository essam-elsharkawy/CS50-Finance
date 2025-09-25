# Final Project: Finance Web Application

## Introduction
This project is my final submission for CS50x. It is a **web application built with Flask, SQLite, and Python** that allows users to register for an account, log in securely, and manage a virtual portfolio. The idea behind this project is to apply the knowledge I gained throughout the course—particularly in web programming, databases, and user authentication—towards building something that simulates a real-world system.

The application focuses on financial management at a simplified level. Users can create an account, log in with their credentials, and then view their balance, buy or sell “virtual” stocks, and check their transaction history. Although this project does not connect to a live stock API, it demonstrates the core mechanics of how such a system might work in practice.

The primary goals were to:
1. Implement **user registration and login** with hashed passwords.
2. Store and retrieve data using a **SQLite database**.
3. Design a clean interface with **HTML templates and CSS**.
4. Provide a secure, multi-user environment where each user only has access to their own data.

---

## Files and Structure

The project directory is organized as follows:

- **`app.py`**
  The core of the application. It initializes Flask, configures the database, and defines all routes. Each route handles different parts of the application:
  - `/register`: Allows a new user to sign up, storing their username and a hashed password in the database.
  - `/login`: Allows existing users to log in, verifying their credentials against the stored hash.
  - `/logout`: Clears the session and logs the user out.
  - `/quote`: Allows the user to input a stock symbol (simplified) and displays a dummy price.
  - `/buy`: Enables the user to purchase shares if they have sufficient balance.
  - `/sell`: Allows the user to sell shares they already own.
  - `/history`: Displays the user’s past transactions in reverse chronological order.

- **`finance.db`**
  A SQLite database file containing the following tables:
  - `users`: Stores user IDs, usernames, and hashed passwords.
  - `transactions`: Stores all user transactions, including stock symbol, number of shares, price, and timestamp.
  - (Optional) `cash`: A field inside `users` table to keep track of available balance.

- **`/templates/`**
  Contains all HTML files used by Flask to render pages:
  - `layout.html`: The base template, includes navigation bar and shared structure.
  - `index.html`: Displays the user’s portfolio.
  - `login.html`: Login form.
  - `register.html`: Registration form.
  - `quote.html`: Input field for stock lookup.
  - `buy.html`: Form to buy shares.
  - `sell.html`: Form to sell shares.
  - `history.html`: Table of transactions.

- **`/static/`**
  Contains `styles.css` for custom styling. I kept the design simple but functional, with clear navigation and readable fonts.

---

## Design Decisions

During development, I faced several choices:

1. **Database choice:** I used SQLite since it integrates well with Flask and is lightweight for this kind of project. Although MySQL or PostgreSQL could have been used, SQLite is simpler to set up and works well for a single-user or demo environment.

2. **Password security:** I chose to use Werkzeug’s `generate_password_hash` and `check_password_hash` functions to ensure that passwords are never stored in plain text. This was an important step in applying best practices in authentication.

3. **Session management:** I used Flask’s session object to keep track of the currently logged-in user. This allows the app to restrict access to pages like `/buy` or `/sell` unless the user is logged in.

4. **Stock data:** Instead of integrating a real API (which could complicate deployment), I implemented a dummy lookup function that simulates stock prices. This keeps the project focused on demonstrating backend logic rather than dealing with API keys or rate limits.

---

## Challenges Faced

- **Authentication logic:** Initially, I struggled with handling login errors (e.g., wrong password or missing username). By carefully checking for null values and using clear error messages, I improved the user experience.

- **Database errors:** At one point, my database became malformed due to repeated testing. I learned the importance of using `CREATE TABLE IF NOT EXISTS` statements and testing with fresh databases to avoid corruption.

- **Balancing simplicity and completeness:** It was tempting to add too many features, but I focused on building a solid, working foundation. I preferred clean code with good comments instead of rushing into unnecessary complexity.

---

## Future Improvements

If I had more time, I would like to extend the project with:
1. **Real stock API integration** (such as IEX Cloud) to fetch live prices.
2. **More detailed portfolio analysis**, including graphs and statistics.
3. **User-to-user transactions**, such as sending balance between accounts.
4. **Improved UI/UX** using Bootstrap or a modern frontend framework.
5. **Error handling and validation** with clearer messages and protections.

---

## How to Run

1. Clone the project into your Codespace or local machine.
2. Run `pip install -r requirements.txt` to install Flask and any other dependencies.
3. Initialize the database by running `sqlite3 finance.db < schema.sql` (or create manually using the schema inside `app.py`).
4. Start the Flask app using:
   ```bash
   flask run

## Video
Here is a demonstration of my project:
https://youtu.be/o-zmGakiivQ
