import tornado.web
import boto3
import json

class ManipulateS3(tornado.web.RequestHandler):
	
	def get(self):
		try:
			headers = self.request.headers
			aws_access_key_id = headers.get('aws_access_key_id')
			aws_secret_access_key = headers.get('aws_secret_access_key')
			bucket = headers.get('bucket')

			s3 = boto3.resource(
				's3',
				aws_access_key_id=aws_access_key_id,
				aws_secret_access_key= aws_secret_access_key
			)
			response = s3.meta.client.list_objects(
				Bucket=bucket,
			#     Prefix='im'
			)
			status_code = response['ResponseMetadata']['HTTPStatusCode']
			assert status_code == 200, 'Requisicao incorreta, status {}'.format(status_code)

			lista_arquivos = []
			if 'Contents' in response:
				lista_arquivos = [i['Key'] for i in response['Contents']]
			
			
			self.set_status(200)
			self.write(json.dumps(lista_arquivos))
			self.finish

		except Exception as exp:
			self.set_status(500)
			self.write(json.dumps([]))
			self.finish

			print(exp)

	def post(self):

		try:
			headers = self.request.headers
			aws_access_key_id = headers.get('aws_access_key_id')
			aws_secret_access_key = headers.get('aws_secret_access_key')
			bucket = headers.get('bucket')
			file_name = headers.get('file_name')
			operation = headers.get('operation')
			file_name_out= headers.get('file_name_out')

			# Se o nao enviar um nome especifico para mandar pro s3 o arquivo tera o mesmo nome no s3
			file_name_out = file_name if file_name_out is None else file_name_out

			s3 = boto3.resource(
				's3',
				aws_access_key_id=aws_access_key_id,
				aws_secret_access_key= aws_secret_access_key
			)

			assert operation in ['upload', 'download'], 'The operation {} do not exists'.format(operation)
			if operation == 'upload':
				# Upload
				s3.Object(bucket, file_name_out).upload_file(
					Filename=file_name)

			elif operation == 'download':
				# Download
				s3.meta.client.download_file(bucket, file_name, file_name_out)


			self.set_status(200)
			self.finish

		except Exception as exp:
			self.set_status(500)
			print(exp)

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
