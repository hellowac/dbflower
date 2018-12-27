# encoding=utf-8

"""
    @Date       : 2017-10-09
    @Author     : wangchao
    Description : 存储数据库
"""

from __future__ import unicode_literals, absolute_import

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tornado.options import options
from .models import Task

session = None


def insert_task_received(event):
    """ 新增任务记录 """
    fields = {
        'state': 'received',
        'uuid': event.get('uuid', ''),
        'name': event.get('name', ''),
        'args': event.get('args', ''),
        'kwargs': event.get('kwargs', ''),
        'retries': event.get('retries', ''),
        'eta': event.get('eta', ''),
        'hostname': event.get('hostname', ''),
        'timestamp': event.get('timestamp', None),
        'root_id': event.get('root_id', ''),
        'parent_id': event.get('parent_id', ''),
        'received': datetime.fromtimestamp(event['timestamp']),
    }
    task = Task(**fields)
    session.add(task)


def update_task_started(event):
    """ 开始执行任务 """
    # session.query(Task).filter_by(id=123).update({"name": u"Bob Marley"})
    session.query(Task).filter_by(uuid=event['uuid']).update({
        'state': 'started',
        'pid': event.get('pid', 0),
        'timestamp': event.get('timestamp'),
        'started': datetime.fromtimestamp(event['timestamp']),
    })


def update_task_succeeded(event):
    """ 执行任务成功 """
    session.query(Task).filter_by(uuid=event['uuid']).update({
        'state': 'success',
        'result': event.get('result', ''),
        'runtime': event.get('runtime', 0.0),
        'timestamp': event.get('timestamp'),
        'succeeded': datetime.fromtimestamp(event['timestamp']),
    })


def update_task_failed(event):
    """ 执行任务失败 """
    session.query(Task).filter_by(uuid=event['uuid']).update({
        'state': 'failure',
        'exception': event.get('exception', ''),
        'traceback': event.get('traceback', ''),
        'timestamp': event.get('timestamp'),
        'failed': datetime.fromtimestamp(event['timestamp']),
    })


def update_task_rejected(event):
    """ 任务处于被驳回状态 """
    session.query(Task).filter_by(uuid=event['uuid']).update({
        'state': 'rejected',
        'rejected': True,
    })


def update_task_revoked(event):
    """ 任务处于被取消状态 """
    session.query(Task).filter_by(uuid=event['uuid']).update({
        'state': 'revoked',
        'terminated': event.get('terminated', ''),
        'signum': event.get('signum', ''),
        'expired': event.get('expired', ''),
    })


def update_task_retried(event):
    """ 任务处于重试中... """
    session.query(Task).filter_by(uuid=event['uuid']).update({
        'state': 'retrying',
        'exception': event.get('exception', ''),
        'traceback': event.get('traceback', ''),
        'timestamp': event.get('timestamp'),
    })


event_func_map = {
    'task-failed': update_task_failed,
    'task-started': update_task_started,
    'task-revoked': update_task_revoked,
    'task-retried': update_task_retried,
    'task-received': insert_task_received,
    'task-rejected': update_task_rejected,
    'task-succeeded': update_task_succeeded,
}


def make_session():
    global session

    # conn_str = '{}+{}://{}:{}@{}:{}/{}'.format(
    #         'mysql', 'mysqldb', 'datacenter', 'datacenter', '192.168.2.6', '3306', 'datacenter')

    conn_str = '{}+{}://{}'.format('mysql', 'mysqldb', options.db_mysql)

    engine = create_engine(conn_str, echo=False)  # 是否显示日志

    session = sessionmaker(bind=engine, autocommit=True)()

    if not engine.dialect.has_table(engine, Task.__tablename__):
        Task.metadata.create_all(engine)  # 创建表.


def store_event(event_type, event):
    global event_func_map, session

    ignore_events = ['worker-heartbeat', ]

    if event_type in ignore_events:
        return

    if options.db_mysql and not session:
        make_session()

    if event_type.startswith('task'):
        event_func_map[event_type](event)
    else:
        print(f'unknow event: {event_type}')


