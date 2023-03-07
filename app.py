import os
import json
import ast
import datetime
import tornado.httpserver
import tornado.options
import tornado.ioloop
import tornado.web
import tornado.wsgi

from tornado import gen, web

tornado.options.define('port', default='8000', help='REST API Port', type=int)

class BaseHandler(tornado.web.RequestHandler):
  """
  Base handler gonna to be used instead of RequestHandler
  """
  def write_error(self, status_code, **kwargs):
    if status_code in [403, 404, 500, 503]:
      self.write('Error %s' % status_code)
    else:
      self.write('BOOM!')


class ErrorHandler(tornado.web.ErrorHandler, BaseHandler):
  """
  Default handler gonna to be used in case of 404 error
  """
  pass

class StatusHandler(BaseHandler):
  """
  GET handler to check the status on the web service
  """
  def get(self):
    self.set_status(200)
    self.finish({'status': 'Rest API Service status is ok...'})

class ParamsHandler(BaseHandler):
  """
  GET handler for multiple parameters
  """
  def get(self, **params):
    print("get: ", params)
    self.set_status(200)
    self.finish({'ok': 'GET success'})

class MainHandler(BaseHandler):
  """
  GET handler for main page, loads the index.html
  """
  def get(self):
    self.set_status(200)
    self.render('index.html')

def make_app():
    settings = dict(
      cookie_secret=str(os.urandom(45)),
      template_path=os.path.join(os.path.dirname(__file__), "templates"),
      static_path=os.path.join(os.path.dirname(__file__), "static"),
      default_handler_class=ErrorHandler,
      default_handler_args=dict(status_code=404)
    )
    return tornado.web.Application([
      (r"/", MainHandler),
      (r"/api/status", StatusHandler),
      (r"/api/tornado", MainHandler),
      (r"/api/tornado/(?P<one>[^\/]+)/?(?P<two>[^\/]+)?/?(?P<three>[^\/]+)?/?(?P<four>[^\/]+)?", ParamsHandler),
    ], **settings)  

def main():
    app = make_app()
    return app

app = main()  

if __name__ == '__main__':
    print("starting tornado server..........")
    app.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()