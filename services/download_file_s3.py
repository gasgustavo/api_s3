import tornado.web
import boto3
import json

class DownloadFileS3(tornado.web.RequestHandler):
	
	def post(self):

		try:
			headers = self.request.headers
			aws_access_key_id = headers.get('aws_access_key_id')
			aws_secret_access_key = headers.get('aws_secret_access_key')
			bucket = headers.get('bucket')
			file_name = headers.get('file_name')
			file_name_out= headers.get('file_name_out')

			# Se o nao enviar um nome especifico para mandar pro s3 o arquivo tera o mesmo nome no s3
			file_name_out = file_name if file_name_out is None else file_name_out

			s3 = boto3.resource(
				's3',
				aws_access_key_id=aws_access_key_id,
				aws_secret_access_key= aws_secret_access_key
			)

			# Download
			s3.meta.client.download_file(bucket, file_name, file_name_out)

			self.set_status(200)
			self.finish

		except Exception as exp:
			self.set_status(500)
			print(exp)

