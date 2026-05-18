# StudyFlow 🌙

A clean and minimal Django-based study management web application designed to help students organize subjects, manage tasks, track deadlines, and keep notes in one place.

---

## ✨ Features

- User authentication system (Signup/Login/Logout)
- Subject management
- Task management
- Mark tasks as completed or pending
- Edit and delete tasks
- Priority-based task system
- Due date tracking
- Overdue task indication
- Search tasks
- Filter tasks by:
  - Priority
  - Status
  - Subject
- Notes section for each subject
- Dashboard with statistics
- Today's tasks section
- Clean responsive UI

---

## 🛠 Tech Stack

- Python
- Django
- HTML
- CSS
- SQLite
- Git & GitHub

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/HaniyaIrshad/StudyFlow.git
```

### 2. Move into the project folder

```bash
cd StudyFlow
```

### 3. Create virtual environment

```bash
python -m venv myenv
```

### 4. Activate virtual environment

#### Windows

```bash
myenv\Scripts\activate
```

#### Mac/Linux

```bash
source myenv/bin/activate
```

### 5. Install dependencies

```bash
pip install django
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Start the server

```bash
python manage.py runserver
```

---

## 📂 Project Structure

```text
StudyFlow/
│
├── config/          # Project settings
├── tasks/           # Task and subject management app
├── users/           # Authentication system
├── templates/       # HTML templates
├── static/          # CSS and static files
├── media/           # Media files
├── manage.py
├── db.sqlite3
└── README.md
```

---

## 🌱 Future Improvements

- Dark mode
- Calendar integration
- Task reminders
- Profile customization
- Better mobile responsiveness
- File uploads for notes
- Deployment

---

## 💡 Purpose of the Project

StudyFlow was created as a learning project to improve Django backend development skills and build a real-world web application with authentication, CRUD operations, filtering, and dashboard features.

---

## 👩‍💻 Author

### Haniya Irshad

BSc Computer Science student interested in backend development, thoughtful digital spaces, and UI/UX.

GitHub: https://github.com/HaniyaIrshad
