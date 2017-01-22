# S2FAM for Free (French carrier)
# SMS-based 2 Factor Authentication Module for SSH
# Free Mobile user only (French carrier)!
# (See README.md)
#

import hashlib, random, requests

# Credentials
USER = '<your-login-here>'
PASS = '<your-identification-key-here>'

# PIN length
PIN_LENGTH = 12
MAX_ATTEMPTS = 3

class FreeUser:
	def __init__(self, user, pwd):
		self.user = user
		self.pwd = pwd
		self.url  = 'https://smsapi.free-mobile.fr/sendmsg'

	def send_sms(self, user, pin):
		msg = 'User: ' + user + '\nPIN: ' + pin
		r = requests.get(self.url+'?user=' + self.user + '&pass=' + self.pwd + '&msg=' + msg)
		return r.status_code


def gen_pin():
	pin = str(random.randint(0,100000000))
	pin = '0' * (8-len(pin)) + pin
	return pin


def send_pin(user, pin):
	me = FreeUser(USER, PASS)
	return me.send_sms(user, pin)


def pam_sm_authenticate(pamh, flags, argv):
	try:
		user = pamh.get_user(None)
	except pamh.exception, e:
		return e.pam_result
	
	if (user == None):
		msg = pamh.Message(pamh.PAM_ERROR_MSG, 'User not found.\nAuthentication aborted.')
		pamh.conversation(msg)
		return pamh.PAM_ABORT

	pin = gen_pin()
	if (pin == -1):
		msg = pamh.Message(pamh.PAM_ERROR_MSG, 'PIN generation failed.\nAuthentication aborted.')
		pamh.conversation(msg)
		return pamh.PAM_ABORT

	retval = send_pin(user, pin)	
	if (retval == False):
		msg = pamh.Message(pamh.PAM_ERROR_MSG, 'Unable to send PIN.\nAuthentication aborted.')
		pamh.conversation(msg)
		return pamh.PAM_ABORT

	msg = pamh.Message(pamh.PAM_TEXT_INFO, 'A PIN has been generated and sent to you by SMS.')
	pamh.conversation(msg)

	for attempt in range(MAX_ATTEMPTS):
		msg = pamh.Message(pamh.PAM_PROMPT_ECHO_OFF, 'PIN: ')
		response = pamh.conversation(msg)

		if (response.resp == pin):
			return pamh.PAM_SUCCESS
		else:
			if (attempt < MAX_ATTEMPTS):
				msg = pamh.Message(pamh.PAM_ERROR_MSG, 'Permission denied, please try again.')
				pamh.conversation(msg)

	msg = pamh.Message(pamh.PAM_ERROR_MSG, '3 incorrect PIN attempts.')
	pamh.conversation(msg)
	return pamh.PAM_AUTH_ERR


def pam_sm_setcred(pamh, flags, argv):
	return pamh.PAM_SUCCESS


def pam_sm_acct_mgmt(pamh, flags, argv):
	return pamh.PAM_SUCCESS


def pam_sm_open_session(pamh, flags, argv):
	return pamh.PAM_SUCCESS


def pam_sm_close_session(pamh, flags, argv):
	return pamh.PAM_SUCCESS


def pam_sm_chauthtok(pamh, flags, argv):
	return pamh.PAM_SUCCESS
