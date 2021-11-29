import os
import requests
import io
import base64
import cv2
from PIL import Image

class Client:
	url: str
	access_key: str

	def __init__(self, url, access_key):
		self.url = url
		self.access_key = access_key

	def img_to_base64(self, img):
		if img.any():
			im = Image.fromarray(img)
			rawBytes = io.BytesIO()
			im.save(rawBytes, "PNG")
			rawBytes.seek(0)
			return str(base64.b64encode(rawBytes.read()), 'utf-8')
		
		return ''

	def upload(self, filepath, show_cuts):
		multipart_form_data = {
			'access_key': (None, str(self.access_key)),
			'show_cuts': (None, str(show_cuts)),
			'file': (os.path.basename(filepath), open(filepath, 'rb'), 'image/*'),
		}

		response = requests.post(self.url, files=multipart_form_data)

		return response

	def upload_json_body(self, filepath, show_cuts):
		headers = {'access_key' : self.access_key, 'Accept' : 'application/json', 'Content-Type' : 'application/json'}
		img = cv2.imread(filepath)
		imgBase64 = self.img_to_base64(img)
		payload = { 'image': imgBase64, 'show_cuts': show_cuts }

		response = requests.post(self.url + '/scan', json=payload, headers=headers)

		return response


if __name__ == "__main__":
	client = Client('https://api.fahrzeugschein-scanner.de', 'your-access-key')
	res = client.upload('path-to-your-file', True)
	#res = client.upload_json_body('path-to-your-file', False)

	# use the response

	print(res.status_code)
	j = res.json()
	print(j)