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
   In the `backend/` folder, create a `.env` file:
