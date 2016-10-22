#!/usr/bin/python
# encoding=utf-8
import sys

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import SysConsts
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.gen
import traceback
import os
import ConfigParser

__version__ = "1.0.0"

# 解决linux下中文编码问题
reload(sys)
sys.setdefaultencoding('utf-8')


class UploadFileHandler(tornado.web.RequestHandler):
    """文件上传"""

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        """处理客户端post请求"""
        try:
            file_metas = self.request.files['file']
            upload_path = self.get_argument('src')
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            for meta in file_metas:
                filename = meta['filename']
                filepath = os.path.join(upload_path, filename)
                SysConsts.logger.info('upload:' + filepath)
                with open(filepath, 'wb') as up:  # 有些文件需要已二进制的形式存储，实际中可以更改
                    up.write(meta['body'])
            print '上传文件：' + filepath
        except Exception:
            SysConsts.logger.error(traceback.format_exc())
        self.finish("success")


class DeleteFileHandler(tornado.web.RequestHandler):
    """删除文件"""

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        """处理客户端post请求"""
        try:
            file_path = self.get_argument('src')
            if os.path.exists(file_path) and os.path.isfile(file_path):
                os.remove(file_path)
            SysConsts.logger.info('delete:' + file_path)
        except Exception:
            SysConsts.logger.error(traceback.format_exc())
        self.finish()


def get_server_port():
    if not 1024 < SysConsts.SERVER_PORT < 65535:
        SysConsts.SERVER_PORT = 8080
    SysConsts.logger.info('Now, listening at port ' + str(SysConsts.SERVER_PORT))
    return SysConsts.SERVER_PORT


def start_server():
    """启动http服务"""
    application = tornado.web.Application([
        (r"/icloudboss/upload", UploadFileHandler),
        (r"/icloudboss/delete", DeleteFileHandler)
    ], "", None, log_function=log_request)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(get_server_port())
    tornado.ioloop.IOLoop.instance().start()


def init_config():
    """初始化配置文件"""
    cf = ConfigParser.ConfigParser()

    if not cf.read("../ibserver.conf"):
        cf.read("ibserver.conf")

    SysConsts.SERVER_PORT = int(cf.get("address", "server_port"))


def main():
    # 初始化配置
    init_config()
    # 启动http服务
    start_server()


def log_request(handler):
    pass


if __name__ == '__main__':
    try:
        main()
    except Exception:
        SysConsts.logger.error(traceback.format_exc())
