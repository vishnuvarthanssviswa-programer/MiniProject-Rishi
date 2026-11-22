STUDENT DASHBOARD PORTAL — STREAMLIT VERSION

Technology:
- Frontend: HTML/CSS markup rendered by Streamlit (NO JavaScript files)
- Backend: Python + Streamlit
- Database: SQLite

RUN LOCALLY:
1. Extract the ZIP and open the folder in VS Code.
2. Open Terminal in the folder containing app.py.
3. Install dependencies:
   py -m pip install -r requirements.txt
4. Run the app:
   py -m streamlit run app.py
5. Open the local URL shown in the terminal (usually http://localhost:8501).

DEPLOY ON STREAMLIT COMMUNITY CLOUD:
1. Upload/push app.py and requirements.txt (plus this README) to a GitHub repository.
2. Go to https://share.streamlit.io/ and sign in with GitHub.
3. Select the repository and branch.
4. Set Main file path to: app.py
5. Click Deploy.

IMPORTANT:
- This version does NOT use Flask, JavaScript, or a separate frontend server.
- Streamlit provides the interactive form controls; the page layout and styling use HTML/CSS.
- Student profile values are demo data. Edit the student dictionary in app.py.
- SQLite on Streamlit Cloud may not persist reliably across app restarts/redeployments.
  Use a hosted database for permanent production data.
