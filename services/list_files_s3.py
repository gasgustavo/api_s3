import tornado.web
import boto3
import json

class ListFilesS3(tornado.web.RequestHandler):
	
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

