"""Email sender.

Basic module to send emails from the platform using the standard Python SMTP
mechanishm.
"""

from email.mime.text import MIMEText
from datetime import date
import smtplib
from urllib.parse import urlparse

from sikre import settings
from sikre.utils.logs import logger

from_addr = settings.DEFAULT_EMAIL_FROM
site_domain = urlparse(settings.SITE_DOMAIN).netloc
EMAIL_SPACE = ", "


def send_email(subject='', to_address=[], from_address=from_addr, content=''):
    """Send an email to a specified user or users.

    This is a basic wrapper around python's STMPLIB library that allows us to
    send emails to the users in case it's necessary. Any failure of this
    script is considered fatal.
    """
    try:
        msg = MIMEText(content)
        msg['Subject'] = "[{0}] {1} {2}".format(site_domain, subject,
                                                date.today().strftime("%Y%m%d"))
        msg['To'] = EMAIL_SPACE.join(to_address)
        msg['From'] = from_address
        logger.debug("All parameters set")
        mail = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
        logger.debug("Instantiated the SMTP")
        if settings.SMTP_TLS:
            mail.starttls()
            logger.debug("Started SMTP TLS connection")
        mail.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        logger.debug("Login success")
        mail.sendmail(from_addr, to_address, msg.as_string())
        logger.debug("Sent email")
        mail.quit()
    except Exception as e:
        logger.error("Email send failed. Error: {0}".format(e))
