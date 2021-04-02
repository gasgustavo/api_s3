import tornado.ioloop
import tornado.web

from tornado.options import define, options, parse_command_line

from services.upload_file_s3 import UploadFileS3
from services.download_file_s3 import DownloadFileS3
from services.list_files_s3 import ListFilesS3
from services.delete_file_s3 import DeleteFileS3

def main():
    
    port, debug = parse_command_line()
    debug = bool(debug)
    print(f'Servidor iniciado na porta {port} com debug={debug}')
    # tornado.options.parse_config_file("server.conf")
    
    app = tornado.web.Application(
        [
            ("/s3/files/upload/", UploadFileS3),
            ("/s3/files/download/", DownloadFileS3),
            ("/s3/files/list/", ListFilesS3),
            ("/s3/files/delete/", DeleteFileS3),
        ],
        debug=debug,
    )
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()