# Jecyani Properties - Real Estate Website

A professional real estate website for Jecyani Properties, a Nigerian real estate agency helping clients buy, sell, and invest in prime properties across Aba, Umuahia, Abuja, Asaba, and Enugu.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Email Configuration](#email-configuration)
- [Security Features](#security-features)
- [Deployment](#deployment)
- [SEO & Social Media](#seo--social-media)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## ✨ Features

- **Responsive Design** - Works on desktop, tablet, and mobile devices
- **Property Listings** - Browse available estates with filtering by location
- **Investment Opportunities** - Flexible payment plans (3, 6, 12 months)
- **Virtual Tours** - YouTube and local video walkthroughs
- **Contact Form** - Email notifications with auto-reply to users
- **Flyer Carousel** - Clickable announcement bar with auto-sliding flyers
- **Booking Modal** - One-click call or WhatsApp for property inspections
- **Admin Dashboard** - View and retry failed emails
- **SEO Optimized** - Meta tags, sitemap, robots.txt
- **Security** - Rate limiting, CSRF protection, security headers

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Flask | Backend web framework |
| Python 3.10+ | Programming language |
| SMTP | Email sending (Gmail) |
| APScheduler | Background email retry jobs |
| HTML5/CSS3 | Frontend structure & styling |
| JavaScript | Interactivity & form submission |
| AOS Library | Scroll animations |

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/jecyani-properties.git
cd jecyani-properties
```

### 2. Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

Create a `.env` file in the root directory:

```env
# Email Configuration
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
ADMIN_EMAIL=jayny57@gmail.com

# SMTP Settings
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Security
SECRET_KEY=your_random_secret_key_here
ADMIN_PASSWORD=your_strong_admin_password
```

### 5. Generate a Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and paste as `SECRET_KEY` in your `.env` file.

## 🚀 Running the Application

### Development Mode

```bash
python app.py
```

The app will run at: `http://127.0.0.1:5000`

### Production Mode

```bash
# Using gunicorn (Linux/Mac)
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Using waitress (Windows)
waitress-serve --host=0.0.0.0 --port=8000 app:app
```

## 📁 Project Structure

```
jecyani-properties/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in git)
├── .gitignore                  # Git ignore file
│
├── static/                     # Static files
│   ├── video/                  # Local video files
│   │   ├── vid1.mp4
│   │   └── vid2.mp4
│   ├── logo.png                # Company logo
│   ├── og-image.jpg            # Social media sharing image
│   ├── fly.jpeg                # Flyer images
│   ├── flyer1.jpeg
│   ├── flyer2.jpeg
│   └── ...
│
├── templates/                  # HTML templates
│   ├── index.html              # Homepage
│   ├── about.html              # About page
│   ├── properties.html         # Properties listing
│   ├── services.html           # Services page
│   ├── investments.html        # Investment page
│   └── sitemap.xml             # XML sitemap for SEO
│
└── failed_emails.json          # Backup for failed email sends
```

## 📧 Email Configuration

### Gmail Setup (Recommended)

1. **Enable 2-Factor Authentication** on your Google account
2. **Generate an App Password:**
   - Go to Google Account → Security → 2-Step Verification
   - Scroll to "App passwords"
   - Select "Mail" and generate
   - Copy the 16-character password

3. **Add to `.env`:**
```env
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_16_character_app_password
```

### How Email System Works

| Email Type | Recipient | Purpose |
|------------|-----------|---------|
| Admin Notification | `ADMIN_EMAIL` | You receive user inquiry details |
| Auto-reply | User | Confirmation email to the person who filled the form |

### Failed Email Handling

- Failed emails are saved to `failed_emails.json`
- Automatic retry every 30 minutes (up to 5 attempts)
- Admin can manually retry via `/admin/failed-emails?password=your_password`

## 🔒 Security Features

| Feature | What it does |
|---------|--------------|
| Rate Limiting | Max 5 messages per minute per IP |
| CSRF Protection | Prevents form hijacking |
| Security Headers | X-Content-Type-Options, X-Frame-Options, X-XSS-Protection |
| Environment Variables | Secrets never hardcoded |
| .gitignore | Prevents committing sensitive files |

## 🌐 Deployment

### Option 1: PythonAnywhere (Free tier)

1. Upload files to PythonAnywhere
2. Set up a new web app with Flask
3. Configure WSGI file
4. Add environment variables in Web tab
5. Set debug=False in app.py

### Option 2: Render (Free tier)

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn app:app`

### Option 3: Railway (Free tier)

1. Install Railway CLI
2. Run `railway init`
3. Run `railway up`
4. Add environment variables in dashboard

## 🔍 SEO & Social Media

### Files Created for SEO

| File | Purpose |
|------|---------|
| `robots.txt` | Tells search engines what to crawl |
| `sitemap.xml` | Lists all pages for Google |
| Meta tags | Description, keywords, author |
| Open Graph tags | Social media sharing (Facebook, WhatsApp) |
| Twitter Cards | Social media sharing (Twitter/X) |

### Submit to Search Engines

- **Google Search Console:** https://search.google.com/search-console
- **Bing Webmaster Tools:** https://www.bing.com/webmasters

### Social Media Image

Place `og-image.jpg` (1200 x 630 pixels) in `static/` folder for social sharing.

## 🐛 Troubleshooting

### Emails not sending

```bash
# Check if Gmail allows less secure apps (use App Password instead)
# Verify .env file has correct credentials
# Check console for error messages
```

### Videos not playing

```
# Make sure video files are in static/video/ folder
# Check file paths: /static/video/vid1.mp4
# Verify file names match exactly (case-sensitive)
```

### 404 Errors

```
# Check that all static files exist
# Verify Flask is running (debug=True for local)
# Check browser console for exact error
```

### Port already in use

```bash
# Change port in app.py
if __name__ == '__main__':
    app.run(debug=False, port=5001)
```

## 📝 Requirements

Create `requirements.txt`:

```txt
Flask==2.3.3
python-dotenv==1.0.0
flask-limiter==3.5.0
flask-wtf==1.1.1
APScheduler==3.10.4
WTForms==3.0.1
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is for Jecyani Properties. All rights reserved.

## 📞 Contact

- **Email:** jayny57@gmail.com
- **Phone/WhatsApp:** 08160087513
- **Instagram:** @jecyani_properties
- **YouTube:** @jecyanimult-resourcesltd

---

## 🎯 Quick Start Commands

```bash
# Clone and setup
git clone https://github.com/yourusername/jecyani-properties.git
cd jecyani-properties
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Create .env file
echo "EMAIL_ADDRESS=your_email@gmail.com" > .env
echo "EMAIL_PASSWORD=your_app_password" >> .env
echo "ADMIN_EMAIL=jayny57@gmail.com" >> .env
echo "SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')" >> .env
echo "ADMIN_PASSWORD=your_password" >> .env

# Run the app
python app.py
```

---

**Built with ❤️ for Jecyani Properties**
```

## Also create a `.gitignore` file:

```gitignore
# Environment
.env
venv/
env/
ENV/

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
failed_emails.json

# Database
*.db
*.sqlite

# OS
.DS_Store
Thumbs.db

# Flask
instance/
.webassets-cache

# Deployment
*.pid
```
