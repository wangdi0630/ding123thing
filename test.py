import web

from weixinInterface import WeixinInterface


urls = (
    '/wx', 'WeixinInterface'
)
app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()