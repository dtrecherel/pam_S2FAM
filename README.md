# pam_S2FAM

SMS-based 2-Factor-Authentication Module

Note: this pam only works with Free, the French carrier (see note #2 and #3)

## Description

This python pam module adds an extra layer of security to your SSH authentication mechanism.

In addition to the usual password and/or public key methods, an SMS is sent to your phone with the PIN to use to complete the connection.

I just wanted to develop a 2FA solution for SSH. In no way I can assert this solution to be highly secure and better than [Google Authenticator.][1] Still, it avoids the use of a third party.

## Requirements

Here are the requirements:

 - [Python Requests][2]
 - [Python PAM][3]

## HOW CAN I MAKE IT WORK !!1!

First, you need to log in to your Free account and activate the option 'Notifications par SMS'. Once activated, you'll get an identification key ('clef d'identification'). This key, along with your login ('identifiant') will be necessary to send the SMS. Just edit the module with your credentials.

Then, you need to tell PAM to use the module, and tell SSH to use PAM.

### 1. Install the module

Check whether the directory `/lib/security/` exits. In that case, move the file there, if not, you might want to check for something along the line of `/lib/x86_64-linux-gnu/security/`.

### 2. Configure PAM

Edit `/etc/pam.d/sshd` and add this after `@include common-auth`:

	auth       requisite     pam_python.so pam_S2FAM.py

Note that PAM will check in `/lib/security/` for `pam_python.so` and `pam_S2FAM.py`, so if in the previous step you had a different directory, you might need to add the absolute path to these files. For example:

	auth       requisite     /lib/x86_64-linux-gnu/security/pam_python.so /lib/x86_64-linux-gnu/security/pam_S2FAM.py

Also, it's important to add this line *after* `@include common-auth`. Otherwise, the first method used will be the PIN sent to your phone. So if a bot tries to bruteforce your server, you'll have a bad time receiving a ton of SMS. ;-)

### 3. Configure SSH

Edit `/etc/ssh/sshd_config` and make the following modifications:

	ChallengeResponseAuthentication yes
	AuthenticationMethods publickey keyboard-interactive:pam

## Notes

1. While I was making this module, I noticed that I wasn't the first one to have thought of that. ChokePoint [published a post][4] with their solution. Credit goes to them, that post helped me a lot. :)
2. While they use a third party to send the SMS, I use the SMS gateway provided by the carrier Free to their client.
3. You still might be able to adapt this module to fit your phone carrier, take a look at [Martin Fitzpatrick's blog][5]. If this post is down, check for "SMS gateways" on your favorite search engine.


[1]: https://github.com/google/google-authenticator "Google Authenticator repository"
[2]: http://docs.python-requests.org/en/master/user/install/#install "Python Requests"
[3]: http://pam-python.sourceforge.net "Python PAM"
[4]: http://www.chokepoint.net/2013/12/simple-ssh-2-factor-pam-python-module.html "ChokePoint post"
[5]: http://mfitzp.io/list-of-email-to-sms-gateways/ "Martin Fitzpatrick's list of email to SMS gateways"
