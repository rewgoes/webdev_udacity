import webapp2
import cgi
import string
import re

def escape_html(s):
	return cgi.escape(s, quote = True)

form1 = """
<form method="post">
    What is your birthday?
    <br>
    <label>
        Month
        <input type="text" name="month" value="%(month)s">
    </label>
    <label>
        Day
        <input type="text" name="day" value="%(day)s">
    </label>
    <label>
        Year
        <input type="text" name="year" value="%(year)s">
    </label>
    <div style="color: red">%(error)s</div>
    <br><br>
    <input type="submit">
</form>
"""

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                        'September', 'October', 'November', 'December']

def valid_day(day):
	if(day and day.isdigit()):
        	day = int(day)
	if(day < 32 and day > 0):
		return day

def valid_month(month):
	if(month):
		month = month.capitalize()
	if(month in months):
		return month

def valid_year(year):
	if(year and year.isdigit()):
		year = int(year)
	if(year < 2020 and year > 1880):
		return year

class MainPage(webapp2.RequestHandler):
	def write_form(self, error="", month="", day="", year=""):
		self.response.out.write(form1 %{"error": error,
						"month": escape_html(month),
						"day": escape_html(day),
						"year": escape_html(year)})

	def get(self):
		self.write_form()

	def post(self):
		user_month = self.request.get('month')
		user_day = self.request.get('day')
		user_year = self.request.get('year')

		month = valid_month(user_month)
		day = valid_day(user_day)
		year = valid_year(user_year)

		if not(month and day and year):
			self.write_form("That doesn't look valid to me, friend.", user_month, user_day, user_year)
		else:
			self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Thanks! That's a totally valid day!")

form2 = """
<h1>Enter some text to ROT13:</h1>
<form method="post">
    <textarea name="text" style="height: 100px; width: 400px;">%(text)s</textarea>
    <br />
    <input type="submit" />
</form>
"""

rot13 = string.maketrans("ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz","NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")

class Rot13Handler(webapp2.RequestHandler):
	def write_form(self, text=""):
                self.response.out.write(form2 %{"text": escape_html(text)})

        def get(self):
                self.write_form()

        def post(self):
                user_text = self.request.get('text')
                self.write_form(user_text.encode("rot13"))

formSingUp = """
<html>
   <head>
    <title>Sign Up</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>

    <style type="text/css"></style>
  </head>

  <body>
    <h2>Signup</h2>
    <form method="post">
      <table>
        <tbody><tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(username)s">
          </td>
          <td class="error">
            %(usernameError)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password">
          </td>
          <td class="error">
            %(passwordError)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify">
          </td>
          <td class="error">
            %(vPasswordError)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(email)s">
          </td>
          <td class="error">
            %(emailError)s
          </td>
        </tr>
      </tbody></table>

      <input type="submit">
    </form>
   </body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
EMAIL_RE = re.compile(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$")

def valid_username(username):
	return USER_RE.match(username)

def valid_email(email):
	return EMAIL_RE.match(email)

class UserSingupHandler(webapp2.RequestHandler):

	def write_form(self, username="", email="", usernameError="", passwordError="", vPasswordError="", emailError=""):
		self.response.out.write(formSingUp %{"username": escape_html(username),
						     "email": escape_html(email),
						     "usernameError": usernameError,
						     "passwordError": passwordError,
						     "vPasswordError": vPasswordError,
						     "emailError": emailError})

	def get(self):
		self.write_form()

	def post(self):
		user_username = self.request.get("username")
		user_password = self.request.get("password")
		user_vPassword = self.request.get("verify")
		user_email = self.request.get("email")
		
		usernameError = ""
		passwordError = ""
		vPasswordError = ""
		emailError = ""

		fail=False

		if not (user_username and valid_username(user_username)):
			usernameError="That's not a valid username."
			fail=True
			
		if not user_password:
			passwordError="That wasn't a valid password."
			fail=True
			
		if not user_password == user_vPassword:
			vPasswordError="Your passwords didn't match."
			fail=True
			
		if user_email and not valid_email(user_email):
			emailError = "That's not a valid email."
			fail=True
			
		if not fail:
			self.redirect("/unit2/welcome?username=%s" % user_username)
		else:
			self.write_form(username=user_username,
					email=user_email,
					usernameError=usernameError,
					passwordError=passwordError,
					vPasswordError=vPasswordError,
					emailError=emailError)

class SingupThanksHandler(webapp2.RequestHandler):
	def get(self):
		user_username = self.request.get("username")

		self.response.out.write("Welcome, %s!" % user_username)

application = webapp2.WSGIApplication([('/', MainPage),
				       ('/thanks', ThanksHandler),
                                       ("/unit2/rot13",Rot13Handler),
                                       ("/unit2/singup",UserSingupHandler),
				       ("/unit2/welcome",SingupThanksHandler)],debug=True)
