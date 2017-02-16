#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re
# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <style type="text/css">
        span {
            color: red;
        }
        label {
            display:inline-block;
            width: 125px;
            margin-bottom: 5px;
        }
    </style>
</head>
<body>
    <h1>
        Signup
    </h1>
"""
form = """
<form method='post'>
    <label>Username</label>
    <input type='text' name='username' value='%(username)s'>
    <span>%(error_u)s</span>
    <br>
    <label>Password</label>
    <input type='password' name='password'>
    <br>
    <label>Verify Password</label>
    <input type='password' name='verifypassword'>
    <span>%(error)s</span>
    <br>
    <label>Email(optional)</label>
    <input type='text' name='email' value='%(email)s'>
    <span>%(error_e)s</span>
    <br>
    <input type='submit'>
</form>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""
def escaped_html(text):
    return cgi.escape(text)

def ValidEmail(email):
    if len(email) > 7:
        if re.match("^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email) != None:
            return True
    return False

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

class Index(webapp2.RequestHandler):
    def write_form(self, error="", error_u="", error_e="", username="",email=""):
        self.response.out.write(page_header + (form % {"error": error,
                                                        "error_u": error_u,
                                                        "error_e": error_e,
                                                        "username": username,
                                                        "email": email})
                                                        + page_footer)

    def get(self):
        self.write_form()

    def post(self):
        User_name = self.request.get('username')
        Pass_word = self.request.get('password')
        Verify_password = self.request.get('verifypassword')
        E_mail = self.request.get('email')

        username = escaped_html(User_name)
        password = escaped_html(Pass_word)
        verifypassword = escaped_html(Verify_password)
        email = escaped_html(E_mail)
        welcome = "<h2>" + "Welcome, " + username + "!</h2>"
        if Pass_word != Verify_password:
            self.write_form("Password don't match", "", "", username, email)
        elif username == "":
            self.write_form("","Must fill out form", "", username, email)
        elif password == "" or verifypassword == "":
            self.write_form("Must fill out form", "", "", username, email)
        elif valid_username(username) == True:
            self.write_form("", "Invalid username", "", username, email)
        elif ValidEmail == True:
            self.write_form("", "", "Must submit a valid email", username, email)
        else:
            self.response.out.write(welcome)








app = webapp2.WSGIApplication([
    ('/', Index)
], debug=True)
