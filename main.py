import os
import requests

class Client:
	url: str
	access_key: str

	def __init__(self, url, access_key):
		self.url = url
		self.access_key = access_key

	def upload(self, filepath, show_cuts):
		multipart_form_data = {
			'access_key': (None, str(self.access_key)),
			'show_cuts': (None, str(show_cuts)),
			'file': (os.path.basename(filepath), open(filepath, 'rb'), 'image/*'),
		}

		response = requests.post(self.url, files=multipart_form_data)

		return response

if __name__ == "__main__":
	client = Client('https://api.fahrzeugschein-scanner.de', 'your-access-key')
	res = client.upload('path-to-your-file', True)

	# use the response

	print(res.status_code)