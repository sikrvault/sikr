# Copyright 2014-2015 Clione Software and Havas Worldwide London
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

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

    """Send an email to a specified user or users

    This is a basic wrapper around python's STMPLIB library that allows us to
    send emails to the users in case it's necessary. Any failure of this
    script is considered fatal.
    """
    try:
        msg = MIMEText(content)
        msg['Subject'] = "[{0}] {1} {2}".format(site_domain, subject, date.today().strftime("%Y%m%d"))
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
