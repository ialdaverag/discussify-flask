# Discussify Flask

Welcome to **Discussify Flask**, a modern and lightweight solution for managing discussions and forums in your Flask-based web applications.

---

## 🚀 What is Discussify?

Discussify is a flexible and easy-to-integrate system for threads, comments, and user conversations. Built on Python and Flask, it enables you to add powerful forum and discussion features to any web project with minimal setup.

---

## 🛠️ Features

- **User Authentication**  
  Register, login, and manage user profiles.
- **Thread & Comment Management**  
  Create, reply, and moderate discussions in real time.
- **Admin Panel**  
  Full control over users, threads, and moderation.
- **RESTful API**  
  Integrate Discussify with your own apps or consume data from any frontend.
- **Modern Design**  
  Built with Bootstrap, easy to customize.
- **Scalable & Secure**  
  Production-ready and adaptable to your needs.

---

## 🌐 Prefer PHP? Try Discussify Laravel!

A PHP/Laravel version is also available:  
[Discussify Laravel](https://github.com/ialdaverag/discussify-laravel) — offering the same powerful features for the Laravel ecosystem.

---

## 📦 Quickstart

1. **Create a PostgreSQL database:**  
   Example using `psql`:
   ```sql
   CREATE DATABASE discussifydb;
   ```
   Make sure to note your database credentials for the next step.

2. **Clone the repository:**
   ```bash
   git clone https://github.com/ialdaverag/discussify-flask.git
   cd discussify-flask
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables**  
   Rename `.env.example` to `.env` and adjust as needed, including your PostgreSQL credentials.
5. **Initialize the database:**
   ```bash
   flask db upgrade
   ```
6. **Run the app:**
   ```bash
   flask run
   ```

---

## 📄 License

This project is licensed under the MIT License.  
See the [`LICENSE`](./LICENSE) file for details.

---

**Questions or feedback?**  
Open an [Issue](https://github.com/ialdaverag/discussify-flask/issues) or reach out to [@ialdaverag](https://github.com/ialdaverag).

---
