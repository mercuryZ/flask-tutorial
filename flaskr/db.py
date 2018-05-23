# -*- coding:utf-8 -*-

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    # g是面向框架的,框架与数据库之间的联系
    # 比如有这样一次请求-我要吃土豆肉丝, 可能涉及的操作包括买土豆, 削皮, 翻炒, 上桌, 多个操作(函数), 但
    # 都只涉及了这一个请求
    # current_app是另一个特殊对象, 它是指向Flask应用, 用来处理一次请求. 因为我们之前写了工厂函数, 所以
    # 在应用未创建时, 没有应用. 当应用在创建之后, get_db会被调用, 当处理一次请求时, current_app会被使
    # 用
    if 'db' not in g:
       g.db = sqlite3.connect(
           #  
           current_app.config['DATABASE'],
           detect_types = sqlite3.PARSE_DECLTYPES
       )
       # sqlite3.Row告诉连接以字典的形式返回Row. 
       g.db.row_factory = sqlite3.Row
    
    return g.db
        
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    # open_source()打开文件relative to the flaskr包, 这非常有用, 这样你就不必知道以后你在哪里部署应用. 
    # get_db返回数据库连接, 用来执行从文件中读取的指令. 
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8')) 

# click.command()定义了一个cmd命令, 叫init-db, 它会调用init_db函数, 然后显示一个连接成功的信息给用户. 
# with_appcontext Wraps a callbackk so that it's guaranteed to be executed with the script's
#  application context. If callbacks are registered directly to the app.cli object then they are
#  warapped with function by default unless it's disabled.
@click.command('init-db')
@with_appcontext
def init_db_command():
    """clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized with database.')


def init_app(app):
    # app.teardown_appcontext()告诉Flask去调用此函数. 当teardown_appcontext执行时, 会调用close_db
    app.teardown_appcontext(close_db)
    # app.cli.add_command()添加一条新命令, 能够随着'flask'一起被调用
    app.cli.add_command(init_db_command)