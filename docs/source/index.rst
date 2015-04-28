.. Sikre documentation master file, created by
   sphinx-quickstart on Thu Sep 18 17:42:54 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Sikre: Password storage API
===========================

What is Sikre?
--------------

Sikre (or the service equivalent, sikr.io) is a secure password storage API to
protect all your passwords, SSH keys, SSL certificates, or other sensible
information that you might have.

The principle of Sikre is "no one knows nothing" *(insert John Snow joke here)*
so there is no hidden administration, no interfaces to administer the site
or helpers to help you fix something that might go wrong (don't worry, even
if the API fails, the data is secure). Unfortunately, that means also
that we don't implement any methods for recovering data, so if you forget
you master password or accidentally delete something, **no one can recover it**.

Is there any support then?
--------------------------

Yes there is, I actively develop this application, and I'm all ears regarding
new features or bugs that you might have find, specially if they're related
to the security of the API.

Contents:

.. toctree::
   :maxdepth: 2

   installation
   endpoints
   reference
   support
   faq
