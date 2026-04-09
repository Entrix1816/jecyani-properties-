from flask import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json
from dotenv import load_dotenv
import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
import atexit
from apscheduler.schedulers.background import BackgroundScheduler


#@app.after_request
#def debug_csrf(response):
 #   print(f"CSRF Token in session: {session.get('csrf_token', 'No token')}")
 #   return response


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', EMAIL_ADDRESS)
FAILED_EMAILS_FILE = 'failed_emails.json'
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')


csrf = CSRFProtect()
csrf.init_app(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)


def save_failed_email(name, email, phone, service, message, error):
    """Save failed email to local file as backup"""
    try:
        # Load existing failed emails
        failed_emails = []
        if os.path.exists(FAILED_EMAILS_FILE):
            with open(FAILED_EMAILS_FILE, 'r') as f:
                failed_emails = json.load(f)

        # Add new failed email
        failed_emails.append({
            'id': len(failed_emails) + 1,
            'timestamp': datetime.datetime.now().isoformat(),
            'name': name,
            'email': email,
            'phone': phone,
            'service': service,
            'message': message,
            'error': str(error),
            'retry_count': 0,
            'status': 'pending'
        })

        # Save back to file
        with open(FAILED_EMAILS_FILE, 'w') as f:
            json.dump(failed_emails, f, indent=2)

        return True
    except Exception as e:
        print(f"Could not save failed email: {e}")
        return False


def send_admin_notification(name, email, phone, service, message):
    """Send notification email to admin (you)"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = ADMIN_EMAIL
        msg['Reply-To'] = email
        msg['Subject'] = f"🏢 NEW LEAD: {name} - {service}"

        body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Inter', sans-serif; background: #0a0a0a; padding: 20px; }}
                .container {{ max-width: 600px; margin: 0 auto; background: #111111; border-radius: 15px; padding: 30px; border: 1px solid #FFD700; }}
                .header {{ background: linear-gradient(135deg, #FFD700, #e6c200); color: #0a0a0a; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
                .field {{ margin-bottom: 15px; }}
                .label {{ font-weight: bold; color: #FFD700; margin-bottom: 5px; }}
                .value {{ color: #e5e5e5; padding: 10px; background: #1a1a1a; border-radius: 5px; }}
                .footer {{ margin-top: 30px; color: #888; font-size: 12px; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2 style="margin:0;">🏢 JECYANI PROPERTIES</h2>
                    <p style="margin:5px 0 0;">🔔 New Lead Notification</p>
                </div>

                <div class="field">
                    <div class="label">📝 Full Name</div>
                    <div class="value">{name}</div>
                </div>

                <div class="field">
                    <div class="label">📧 Email Address</div>
                    <div class="value">{email}</div>
                </div>

                <div class="field">
                    <div class="label">📞 Phone Number</div>
                    <div class="value">{phone if phone else 'Not provided'}</div>
                </div>

                <div class="field">
                    <div class="label">🛠️ Service Interested In</div>
                    <div class="value">{service}</div>
                </div>

                <div class="field">
                    <div class="label">💬 Message</div>
                    <div class="value" style="white-space: pre-line;">{message}</div>
                </div>

                <div class="footer">
                    Received on {datetime.datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}
                </div>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        return True
    except Exception as e:
        print(f"Admin notification error: {e}")
        # Save to backup file when email fails
        save_failed_email(name, email, phone, service, message, e)
        return False


def send_auto_reply(user_email, name):
    """Send auto-reply email to the user who submitted the form"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = user_email
        msg['Subject'] = "Thank you for contacting Jecyani Properties"

        body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Inter', sans-serif; background: #0a0a0a; padding: 20px; }}
                .container {{ max-width: 600px; margin: 0 auto; background: #111111; border-radius: 15px; padding: 30px; border: 1px solid #FFD700; }}
                .header {{ background: linear-gradient(135deg, #FFD700, #e6c200); color: #0a0a0a; padding: 20px; border-radius: 10px; text-align: center; }}
                .content {{ padding: 20px; }}
                .btn {{ background: #FFD700; color: #0a0a0a; padding: 12px 25px; text-decoration: none; border-radius: 40px; display: inline-block; margin-top: 20px; font-weight: 700; }}
                .footer {{ margin-top: 30px; color: #888; font-size: 12px; text-align: center; border-top: 1px solid #2a2a2a; padding-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2 style="margin:0;">🏢 JECYANI PROPERTIES</h2>
                </div>
                <div class="content">
                    <h3 style="color: #FFD700;">Hello {name}! 👋</h3>
                    <p>Thank you for reaching out to <strong>Jecyani Properties</strong>.</p>
                    <p>We have received your message and one of our real estate advisors will get back to you within <strong>24 hours</strong>.</p>

                    <div style="background: #1a1a1a; padding: 15px; border-radius: 10px; margin: 20px 0;">
                        <p style="margin: 5px 0;"><strong>📞 Need faster response?</strong></p>
                        <p style="margin: 5px 0;">Call or WhatsApp us directly:</p>
                        <p style="margin: 5px 0; font-size: 1.2rem; color: #FFD700;">08160087513</p>
                    </div>

                    <p>In the meantime, feel free to:</p>
                    <ul style="margin-left: 20px; color: #ccc;">
                        <li>📱 Follow us on Instagram: <strong>@jecyani_properties</strong></li>
                        <li>▶️ Subscribe to our YouTube channel for virtual tours</li>
                        <li>🌐 Visit our property listings on our website</li>
                    </ul>

                    <center>
                        <a href="https://wa.me/2348160087513" class="btn" style="color: #0a0a0a;">💬 Chat on WhatsApp</a>
                    </center>
                </div>
                <div class="footer">
                    Jecyani Properties — Trusted Real Estate Solutions<br>
                    © 2026 All Rights Reserved
                </div>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        return True
    except Exception as e:
        print(f"Auto-reply error: {e}")
        return False


def resend_failed_email(failed_entry):
    """Attempt to resend a failed email"""
    try:
        # Try to send admin notification
        admin_sent = send_admin_notification(
            failed_entry['name'],
            failed_entry['email'],
            failed_entry['phone'],
            failed_entry['service'],
            failed_entry['message']
        )

        # Try to send auto-reply
        auto_reply_sent = send_auto_reply(failed_entry['email'], failed_entry['name'])

        if admin_sent or auto_reply_sent:
            failed_entry['status'] = 'success'
            failed_entry['resolved_at'] = datetime.datetime.now().isoformat()
            return True
        else:
            failed_entry['retry_count'] = failed_entry.get('retry_count', 0) + 1
            failed_entry['last_error'] = 'Both emails failed'
            return False

    except Exception as e:
        failed_entry['retry_count'] = failed_entry.get('retry_count', 0) + 1
        failed_entry['last_error'] = str(e)
        return False


def retry_failed_emails():
    """Background job to retry failed emails"""
    print(f"[{datetime.datetime.now()}] Checking for failed emails to retry...")

    if not os.path.exists(FAILED_EMAILS_FILE):
        return

    try:
        with open(FAILED_EMAILS_FILE, 'r') as f:
            failed_emails = json.load(f)

        changed = False
        for entry in failed_emails:
            if entry.get('status') == 'pending' and entry.get('retry_count', 0) < 5:
                print(f"Retrying email for {entry['name']} (attempt {entry.get('retry_count', 0) + 1}/5)")

                if resend_failed_email(entry):
                    changed = True
                    print(f"✅ Successfully resent email for {entry['name']}")
                else:
                    changed = True
                    print(f"❌ Failed to resend email for {entry['name']}")

        if changed:
            with open(FAILED_EMAILS_FILE, 'w') as f:
                json.dump(failed_emails, f, indent=2)

    except Exception as e:
        print(f"Error in retry_failed_emails: {e}")


# Setup scheduler
scheduler = BackgroundScheduler()

scheduler.add_job(
    func=retry_failed_emails,
    trigger="interval",
    minutes=30,
    id="retry_failed_emails",
    name="Retry failed emails every 30 minutes",
    replace_existing=True
)

scheduler.start()
atexit.register(lambda: scheduler.shutdown())


@app.route('/admin/failed-emails')
def view_failed_emails():
    """View all failed emails"""
    password = request.args.get('password', '')

    if password != ADMIN_PASSWORD:
        return "Unauthorized. Add ?password=your-admin-password-here", 401

    if not os.path.exists(FAILED_EMAILS_FILE):
        return "No failed emails"

    with open(FAILED_EMAILS_FILE, 'r') as f:
        failed_emails = json.load(f)

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Failed Emails - Jecyani Properties</title>
        <style>
            body { font-family: Arial; background: #0a0a0a; color: white; padding: 20px; }
            .email-card { border: 1px solid #FFD700; margin: 10px 0; padding: 15px; border-radius: 8px; }
            .success { border-color: green; color: green; }
            .pending { border-color: orange; color: orange; }
            .failed { border-color: red; color: red; }
            button { background: #FFD700; color: black; padding: 8px 16px; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #e6c200; }
        </style>
    </head>
    <body>
        <h1>📧 Failed Emails</h1>
        <button onclick="retryAll()">🔄 Retry All Pending</button>
        <hr>
    """

    for email in failed_emails:
        status_class = email.get('status', 'pending')
        html += f"""
        <div class="email-card {status_class}">
            <strong>ID:</strong> {email.get('id', 'N/A')}<br>
            <strong>Time:</strong> {email.get('timestamp', 'N/A')}<br>
            <strong>Name:</strong> {email.get('name', 'N/A')}<br>
            <strong>Email:</strong> {email.get('email', 'N/A')}<br>
            <strong>Phone:</strong> {email.get('phone', 'N/A')}<br>
            <strong>Service:</strong> {email.get('service', 'N/A')}<br>
            <strong>Message:</strong> {email.get('message', 'N/A')}<br>
            <strong>Retry Count:</strong> {email.get('retry_count', 0)}/5<br>
            <strong>Status:</strong> {email.get('status', 'pending')}<br>
            <strong>Last Error:</strong> {email.get('last_error', 'N/A')}<br>
        </div>
        """

    html += f"""
        <script>
            function retryAll() {{
                fetch('/admin/retry-failed-emails?password={ADMIN_PASSWORD}', {{
                    method: 'POST'
                }}).then(() => {{
                    alert('Retry started! Refresh in a minute.');
                }});
            }}
        </script>
    </body>
    </html>
    """

    return html


@app.route('/admin/retry-failed-emails', methods=['POST'])
def admin_retry_failed():
    """Manually trigger retry of failed emails"""
    password = request.args.get('password', '')

    if password != ADMIN_PASSWORD:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401

    retry_failed_emails()

    return jsonify({
        'status': 'success',
        'message': 'Retry process started'
    })


@app.route('/send-message', methods=['POST'])
@limiter.limit("5 per minute")
def send_message():
    """Handle contact form submission"""
    try:
        data = request.json

        if not data.get('name') or not data.get('email') or not data.get('message'):
            return jsonify({
                'status': 'error',
                'message': 'Please fill in all required fields'
            }), 400

        name = data.get('name')
        user_email = data.get('email')
        phone = data.get('phone', '')
        service = data.get('service', 'General Inquiry')
        message = data.get('message')

        admin_sent = send_admin_notification(name, user_email, phone, service, message)
        auto_reply_sent = send_auto_reply(user_email, name)

        if admin_sent or auto_reply_sent:
            return jsonify({
                'status': 'success',
                'message': 'Thank you! We have received your message. A confirmation email has been sent to your inbox. We\'ll get back to you within 24 hours.'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Unable to send message. Please call us directly at 08160087513'
            }), 500

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Something went wrong. Please try again.'
        }), 500


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/properties')
def property():
    return render_template('properties.html')


@app.route('/investments')
def investment():
    return render_template('investment.html')


@app.route('/services')
def service():
    return render_template('services.html')


@app.route('/sitemap.xml')
def sitemap():
    return render_template('sitemap.xml'), 200, {'Content-Type': 'application/xml'}


@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response


if __name__ == '__main__':
    app.run(debug=False)