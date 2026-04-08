# InstaOrder - Telegram Bot for Product Ordering

A Django-based Telegram bot that enables customers to browse products, place orders, and manage purchases through conversational interface.

## Features
- Product catalog with prices
- Order management (create, confirm, cancel)
- Phone number verification for orders
- Order history tracking
- Interactive inline keyboards
- Rate limiting protection

## Tech Stack
- **Backend**: Django 6.0.3 + Django REST Framework
- **Database**: PostgreSQL
- **API**: Telegram Bot API
- **Deployment**: Gunicorn + WhiteNoise

## Installation

```bash
git clone <repository-url>
cd instaorder
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Environment Variables

```env
SECRET_KEY=your-secret-key
DEBUG=True
ENV=dev
DB_NAME=instaorder
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
BOT_TOKEN=your-telegram-bot-token
META_VERIFY_TOKEN=your-verify-token
```

## Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Bot Commands
- `/start` - Show main menu
- `/status` - View order history

## Project Structure
```
bot/
├── models/         # Lead, Product, Order, Conversation
├── services/       # Business logic handlers
├── views.py        # Webhook endpoint
└── urls.py         # URL routing
```

## Testing

```bash
python manage.py test
```
