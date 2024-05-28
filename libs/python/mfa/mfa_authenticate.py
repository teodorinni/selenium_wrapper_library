import os

from pyotp import *


def get_mfa_code():
    otp = TOTP(os.getenv("MFA_SECRET_KEY_DEV"))
    code = otp.now()
    return code
