#17July 2017Wed Displays front pageshop list
import webapp2
import cgi
import re
form="""
<html>
<head>
</head>
<body style="background-color:rgb(255,167,132);">
<h1> WELCOME TO HEALTH SHOP ! </h1>
<p> Please enter your information below: </p>
    <form method="post">
        <label type="text" style="display:inline-block;width:150px;color:black">Username</label>
        <input type="text" name="username" value="%(username)s">%(username_error)s<br><br>
        <label type="text" style="display:inline-block;width:150px;color:black">Password</label>
        <input type="password" name="password">%(password_error)s<br><br>
        <label type="text" style="display:inline-block;width:150px;color:black">Verify Password</label>
        <input type="password" name="Vpassword">%(Vpassword_error)s<br><br>
        <label type="text" style="display:inline-block;width:150px;color:black">Email Optional</label>
        <input type="text" name="email"value="%(email)s">%(email_error)s<br><br>
        <label type="text" style="display:inline-block;width:150px;color:black">Enter new items</label>
        <input type="text" name="username" value="%(username)s">%(username_error)s<br><br>
    <input type="submit" value="click here for your shopping list">
    </form>
</body>
</html>
"""
list="""
<html>
<head>
</head>
<body style="color:pink;background-color:rgb(12,110,10)">
<h1> shopping list </h1>
    <ul>
      <li> Tylenol </li>
      <li> Ibuprofen    <li>
    </ul>
</body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)
PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        inputinfo = dict(username = "", username_error = "",
                             password_error="",
                             Vpassword_error="",
                             email="",email_error="")# to preserve the data user typed in Username box

        global form# to declare that form is the global variable declared in hTMl above and
                    #it is being assigned to a local variable form which replaces username_error etc
                    # with new values in the " "
        # form= form % inputinfo#overwriting the original form, so I commented this line of code& inserted the line below
        self.response.out.write(form % inputinfo)
    def post(self):
        user =self.request.get("username")
        faulty_form=False
#        validuser = cgi. escaped(user)
        passw = self.request.get("password")
        VerifiedPassword = self.request.get("Vpassword")
        Email = self.request.get("email")
        userwarn = ""
        pwdwarn = ""
        vpwdwarn = ""
        emailwarn = ""
        if not valid_username(user):#If you supply "user" as this parameter, then it is not the same as user = self.request.get("username")
            userwarn = "<label style='color:red'>   This is not valid username.</label>"
            faulty_form = True
        if not valid_password(passw):
            pwdwarn = "<label style='color:red'>   This is not a valid password.</label>"
            faulty_form = True
        elif VerifiedPassword !=passw:
            vpwdwarn ="<label style='color:red'> Passwords do not match.</label>"
            faulty_form = True
        if not valid_email(Email):
            emailwarn = "<label style='color:red'> This is not a valid email.</label>"
            faulty_form = True
        inputinfo = dict(username= user, username_error = userwarn,
                         password_error=pwdwarn,
                         Vpassword_error=vpwdwarn,
                         email=Email,email_error=emailwarn)
        self.response.write( form % inputinfo)
        if faulty_form == False:
            self.redirect('/welcome?username={0}'.format(user))
class WelcomeHandler(webapp2.RequestHandler):
    global list
    def get(self):
        user = self.request.get("username")
        content = " Hi ," + user +" ! Do you want the new item, to be added to your shopping list? "
        self.response.write(content+list)
app = webapp2.WSGIApplication([ ('/',MainHandler),
    ('/welcome',WelcomeHandler)
    ],debug=True)
