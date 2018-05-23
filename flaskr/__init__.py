#-*- coding:utf-8 -*-

import os

from flask import Flask


"""
create_app是工厂函数. 随着本文你会加入越来越多的内容到此函数中, 但现在它已经能做非常多的事了.
"""
def create_app(test_config=None):
    """
    创建一个Flask实例, app. 
    __name__是当前模块的名称. app需要知道它在什么地方, 然后建立起一些路径, 而__name__很容易告诉它路径信息.
    instance_relative_config=True告诉app配置文件与实例文件夹的相对位置. 此实例文件夹在flaskr包的外面, 不应该被版本控制, 比如配置密码和数据库文件.
    """
    app = Flask(__name__, instance_relative_config=True)
    """
    app.config.from_mapping()设置一些app会用到的默认配置. 把配置写到配置文件中.

    """
    app.config.from_mapping(
        # """
        # SECRET_KEY是用来保证Flask与外部插件保持数据安全.
        # """
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        """
        app.config.from_pyfile()从配置文件中重载默认配置.
        """
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    try:
        """
        os.makedirs确认app.instance_path存在
        """
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        # a simple page that says hello
        return 'Hello, World!'
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app