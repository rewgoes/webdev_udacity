import webapp2
import cgi
import string

def escape_html(s):
	return cgi.escape(s, quote = True)

form = """
<h1>Enter some text to ROT13:</h1>
<form method="post">
    <textarea name="text" style="height: 100px; width: 400px;">%(text)s</textarea>
    <br />
    <input type="submit" />
</form>
"""

rot13 = string.maketrans("ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz","NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")

class MainPage(webapp2.RequestHandler):
	def write_form(self, text=""):
		self.response.out.write(form %{"text": escape_html(text)})

	def get(self):
		self.write_form()

	def post(self):
		user_text = self.request.get('text')
		self.write_form(user_text.encode("rot13"))

application = webapp2.WSGIApplication([('/unit2/rot13', MainPage)],debug=True)
