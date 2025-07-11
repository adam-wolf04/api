Note on .env File
-----------------

Yes, the `.env` file is included in this repository. This is intentional for demonstration purposes only.

In real-world projects, `.env` files should always be excluded using `.gitignore` to avoid exposing sensitive data.  
Here, it's shown openly to simplify testing and clearly demonstrate how the application works end-to-end.


# Currency Exchange Rates App

This project is a web application for displaying currency exchange rates.

- FastAPI backend: fetches and stores currency data from an external API.
- React frontend: presents the exchange rate data in an interactive user interface. Fetches locally from backend
- Tailwind CSS: provides a modern, responsive design.

## Backend Setup (FastAPI)

1. **Install dependencies**:
   ```bash
   cd path/to/ur/folder
   python -m venv venv
   source venv/bin/activate     # On Windows: venv\\Scripts\\activate
   pip install -r requirements.txt

2. **Run the server ON 3000! (FE is on 3001)**:
   ```bash
   uvicorn main:app --reload --port 3000 
   ```

3. **Check if running**:  
Open in your browser:

- `http://localhost:3000/status` – checks if backend is running  
- `http://localhost:3000/api/rates?usedb=true` – returns data from local DB  
- `http://localhost:3000/api/rates?usedb=false` – fetches from external API and updates DB if changed

## Frontend Setup (React)

1. **Install dependencies**:
   ```bash
   cd path/to/ur/folder
   npm install
   ```

2. **Run the frontend**:
   ```bash
   npm start
   ```
   The frontend will open at **http://localhost:3001** and make API calls to **3000**.

## Notes
- **Backend** runs on port **3000**
- **Frontend** runs on port **3001**

.gitignore and Repository Notes
-------------------------------

This repository includes a `.env` file intentionally for demonstration purposes.
In a real-world project, such files should be excluded from version control.

The following items are excluded via `.gitignore`:
- `node_modules/` (Node dependencies)
- `venv/` (Python virtual environment)
- `__pycache__/` and `*.pyc` (Python cache)
- `rates.db` (SQLite database)
