import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

def send_appointment_notification(summary, appointment_date, start_time, end_time, attendees_emails, doctor_name=None):
    # Gmail credentials
    sender_email = 'dsproject987@gmail.com'
    sender_password = 'tilakisbest!'  # Use App Password for better security

    # Set up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)

    # Update summary with doctor name if provided
    
    if doctor_name:
        summary = f"{summary} with {doctor_name}"

    # Format the date and time for the email content
    start_datetime = datetime.strptime(f"{appointment_date} {start_time}", "%Y/%m/%d %H:%M")
    end_datetime = datetime.strptime(f"{appointment_date} {end_time}", "%Y/%m/%d %H:%M")

    # Email message content
    message_content = (
        f"Appointment Details:\n\n"
        f"Title: {summary}\n"
        f"Date: {start_datetime.strftime('%Y-%m-%d')}\n"
        f"Start Time: {start_datetime.strftime('%H:%M')}\n"
        f"End Time: {end_datetime.strftime('%H:%M')}\n"
        f"Doctor: {doctor_name}\n\n"
        f"Please ensure you are available at the given time."
    )

    # Loop through each attendee and send email
    for email in attendees_emails:
        # Construct email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = summary
        msg.attach(MIMEText(message_content, 'plain'))

        # Send the email
        server.sendmail(sender_email, email, msg.as_string())

    # Close the SMTP server connection
    server.quit()

    print("Appointment notifications sent successfully.")

# Usage example
attendees_emails = ['attendee1@example.com', 'attendee2@example.com']
appointment_title = "Consultation"
appointment_date = "2024/11/09"
start_time = "00:42"
end_time = "01:42"
doctor_name = "Dr. B - General Practitioner"

send_appointment_notification(appointment_title, appointment_date, start_time, end_time, attendees_emails, doctor_name)
