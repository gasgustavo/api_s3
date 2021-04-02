import tornado.web
import boto3
import json

class DeleteFileS3(tornado.web.RequestHandler):

	def delete(self):

		try:

			headers = self.request.headers
			aws_access_key_id = headers.get('aws_access_key_id')
			aws_secret_access_key = headers.get('aws_secret_access_key')
			bucket = headers.get('bucket')
			file_name = headers.get('file_name')

			s3 = boto3.resource(
				's3',
				aws_access_key_id=aws_access_key_id,
				aws_secret_access_key= aws_secret_access_key
			)
			
			response = s3.meta.client.delete_object(
				Bucket=bucket,
				Key=file_name
			)
			self.set_status(200)
			self.finish



		except Exception as exp:
			self.set_status(500)
			print(exp)
