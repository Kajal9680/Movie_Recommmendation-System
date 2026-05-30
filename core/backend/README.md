# 🖥️ Backend Layer

This folder contains the server-side logic and API routes for the application.

### 📄 Files
- **`auth_routes.py`**: Handles user authentication (Signup, Login, Logout).
- **`movie_routes.py`**: Handles the main movie search and recommendation logic.

### ⚙️ How it works
It uses **Flask Blueprints** to keep the code modular. Each file defines a set of routes that are registered in the main application factory (`core/__init__.py`).
