# Northstar-support-deflection-mvp
Northstar Retail Co. Support Deflection MVP chatbot for order-status and stock-availability questions.


## Client
Northstar Retail Co.

## Product
Support Deflection Chatbot

## Supported Ticket Types
1. Order Status
2. Stock Availability

## Objective
Reduce repetitive support tickets by allowing customers
to obtain automated answers without contacting a support agent.

## Team
- Victor Otieno
- Jane Ndungu
- Mark Oigo
- George Gachuiri
- Nathalie Juma
- Swalha Ahmed

## Project Board
Northstar Sprint Board

## Tech Stack
- **Backend:** Python + Flask
- **Database:** MySQL (via XAMPP)
- **Frontend:** Plain HTML/CSS/JavaScript

## Prerequisites
- Python 3.x installed and added to PATH
- XAMPP installed (for MySQL)

## Setup Instructions

1. **Start MySQL**
   Open XAMPP Control Panel and click "Start" next to MySQL.

2. **Create the database**
   Open `http://localhost/phpmyadmin`, create a database called `northstar_chatbot`, and run the SQL script in `docs/db-schema.sql` to create the tables and sample data.

3. **Set up environment variables**
   In the `backend/` folder, create a `.env` file

4. **Install dependencies**
   cd backend
    pip install flask mysql-connector-python python-dotenv requests
6.  **Run the app**
   python app.py
7.  **Open the chatbot**
   Go to `http://127.0.0.1:5000/` in your browser.

## Testing
Run `python test_db.py` to verify database lookups, or `python test_chat.py` to test the full conversation flow via terminal.

## Sample Questions to Try
- "Where is order NS-1001?"
- "Do you have Nike Air Force 1 in size 42?"
- "Is this available?" (bot will ask follow-up questions)
## Demo Videos

Video walkthroughs demonstrating the chatbot's functionality, corresponding to Phase D testing tasks:

-Order-status conversations — successful lookup, multi-turn (missing order ID), and failure case WATCH VIDEO (https://youtu.be/xcp8LaZAXlE)
-Stock-availability conversations — in-stock, out-of-stock, alternative sizes suggested, and product not found WATCH VIDEO (https://youtu.be/6FGO5qa2zyQ)
-End-to-end integration — full conversation through the live chat UI, covering greetings, order status, stock checks, and out-of-scope handling WATCH VIDEO (https://youtu.be/9ym_bpBgcd4) 


