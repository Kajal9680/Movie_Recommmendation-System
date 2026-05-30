# 🎨 Frontend Layer

This folder contains all the client-side assets and user interface files.

### 📂 Subfolders
- **`static/`**: Contains `style.css` for application styling and any client-side JavaScript.
- **`templates/`**: Contains the HTML files (Jinja2 templates) for different pages:
  - `index.html`: Home page with search.
  - `result.html`: Search results and recommendations.
  - `login.html` & `signup.html`: Authentication pages.

### ⚙️ How it works
The backend serves these files using Flask's `render_template` function. Static files are automatically served from the `static/` folder.
