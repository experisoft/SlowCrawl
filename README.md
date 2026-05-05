# SlowCrawl

**SlowCrawl** is an automated tool for collecting vouchers associated with multiple email addresses. It slowly and responsibly scrapes vouchers from various sources, compiles them into a single PDF document, and delivers the PDF to the user via email on a regular schedule.

---

## 🚀 Features

- 📥 **Automated Voucher Collection**  
  Gathers voucher data associated with specified email addresses through controlled scraping.

- 🐢 **Slow and Responsible Crawling**  
  Designed to scrape at a deliberate pace to avoid overwhelming source servers or triggering anti-bot defenses.

- 🧾 **PDF Compilation**  
  Consolidates all collected vouchers into a single PDF file for convenience.

- 📧 **Scheduled Email Delivery**  
  Emails the compiled PDF to the user at a preset interval (e.g., twice weekly).

---

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager and installer

### Setup

1. Clone or navigate to the project directory.

2. Install dependencies using `uv`:
   ```bash
   uv sync
   ```
   This command will install all required packages specified in `pyproject.toml` and create a `uv.lock` file for reproducible builds.

3. Create a `.env` file in the project root with your configuration (refer to `.env.example` for required variables).

---

## 🏃 Running the Project

To start the main automation workflow, run:

```bash
uv run python main.py
```

This will initialize the environment, set up necessary directories, and begin the voucher collection and processing pipeline.
