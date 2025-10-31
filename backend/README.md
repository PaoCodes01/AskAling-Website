# AskAling Backend

This backend stores contact form submissions in a local SQLite database using Python Flask.

## Setup Instructions

1. Open a terminal in the `backend` folder.
2. (Recommended) Create a virtual environment:
    python -m venv venv
   
    Activate it:
    - On Windows: venv\Scripts\activate
    - On Mac/Linux: source venv/bin/activate

3. Install dependencies:
    pip install flask flask-cors python-dotenv

4. Create a `.env` file in the `backend` folder with this content:
    ADMIN_PASSWORD=Math22413

5. Start the server:
    python app.py

6. The backend will run on http://localhost:5000

## API Endpoints
- POST /api/contact — Save a contact form submission. (Fields: firstName, lastName, email, phone, message)
- GET /api/contacts?admin_password=Math22413 — View all submissions (admin only).

## Security
- The admin endpoint is protected by a password in `.env`.
- Do not share your admin password publicly.
