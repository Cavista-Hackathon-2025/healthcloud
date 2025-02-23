# HealthCloud - AI-powered medical reporting for hospitals

HealthCloud is a platform that allows medical professionals keep records of their patient interactions, for future reference and documentation purposes. It aims to simplify the process of medical records-keeping, and this is only the beginning of a medi-cloud revolution.

This repository includes the entire application code; frontend and backend.

### Tech stack

-   **Backend**: The backend application was built using FastAPI, using SQLAlchemy as the ORM, as well as [Groq](https://groq.com)'s suite of AI models for speech transcription, text processing, and report generation.
-   **Frontend:** The frontend is implemented using React + React Router v6, using the Vite build system.

### Running this application

-   First, you'll need to supply your [Groq](https://groq.com) API key, as shown in the .env.template file.
-   Then, you need to install the backend requirements. Run `pip install -r requirements.txt` to do so.
-   Lastly, install the frontend requirements with `npm install`.

The application will be live at `localhost:5173`
