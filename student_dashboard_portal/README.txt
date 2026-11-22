STUDENT DASHBOARD PORTAL — RUN INSTRUCTIONS

Technology:
- Frontend: HTML, CSS, JavaScript
- Backend: Python + Flask
- Database: SQLite (created automatically)

WHERE TO RUN:
Use Visual Studio Code (recommended) on your computer.

1. Extract this ZIP file.
2. Open the extracted student_dashboard_portal folder in VS Code.
3. Open Terminal > New Terminal.
4. Create and activate a virtual environment (recommended):

   Windows:
   py -m venv venv
   venv\Scripts\activate

   macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate

5. Install backend dependencies:

   pip install -r requirements.txt

6. Start the Python backend:

   Windows:
   py app.py

   macOS/Linux:
   python3 app.py

7. Open this address in your browser:

   http://127.0.0.1:5000

IMPORTANT:
- Run app.py from the main extracted folder, not from the frontend folder.
- Do not open index.html directly. The Flask server serves the frontend and API.
- Keep the terminal running while using the portal.
- The SQLite database file student_portal.db is created automatically.
- Sample student information is demo data. Edit the student object in app.py
  to use your own details.
