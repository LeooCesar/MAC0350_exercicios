# Meus Torneios de Badminton 🏸

A full-stack web application built to manage badminton tournaments, track match scores, and analyze player performance. Developed using Python, FastAPI, SQLAlchemy, and HTMX.

## Features

In this app, users can:
* **Manage Tournaments:** Create new tournaments and view a list of all participating events.
* **Log Matches (Create):** Record detailed match data, including category, stage, partner, opponents, and set-by-set scores.
* **View Results (Read):** View match history in a fully responsive, mobile-friendly UI inspired by official BWF (Badminton World Federation) scorecards.
* **Edit Inline (Update):** Seamlessly update match details and scores directly on the page without reloading, powered by HTMX.
* **Remove Matches (Delete):** Safely delete incorrect match entries from the tournament.
* **Performance Dashboard:** Automatically calculate and display tournament statistics, including total matches, win/loss record, win rate (%), and point differential.

## Tech Stack

* **Frontend:** HTML, CSS (Custom Responsive Dark Theme), HTMX, Jinja2 Templates (used AI for help on Frontend)
* **Backend:** Python, FastAPI
* **Database:** SQLite (via SQLAlchemy)
