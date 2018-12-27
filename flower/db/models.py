# encoding=utf-8

"""
    @Date       : 2017/09/28
    @Author     : Wangchao
    Description : 存储flower任务的数据库原型定义.
"""

from __future__ import unicode_literals, absolute_import

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Unicode, UnicodeText, DateTime, Float

Base = declarative_base()


class Task(Base):
    __tablename__ = 'celery_flower_task'
    id = Column(Integer, primary_key=True)
    pid = Column(Integer, default=0)                    # 执行任务的进程ID.
    uuid = Column(String(255), unique=True)             # 任务ID
    name = Column(String(255), default='')              # 任务名称
    hostname = Column(String(255), default='')          # 执行任务的机器
    state = Column(String(255), default='')             # 任务状态
    args = Column(Unicode(255), default='')             # 任务位置参数
    kwargs = Column(Unicode(255), default='')           # 任务关键字参数
    result = Column(UnicodeText(), default='')          # 任务结果
    expired = Column(String(255), default='False')      # 任务是否过期
    signum = Column(String(255), default='')            # 取消任务时使用的信号
    retries = Column(Integer, default=0)                # 重试了几次
    rejected = Column(String(255), default='')          # 是否被取消
    exception = Column(UnicodeText, default='')         # 发生的异常描述
    traceback = Column(UnicodeText, default='')         # 调用栈(发生异常时)
    timestamp = Column(Float, nullable=True, default=0)            # 发生时间.
    runtime = Column(Float, nullable=True, default=0)   # 运行时间.
    started = Column(DateTime(), nullable=True, default=None)       # 开始时间
    received = Column(DateTime(), nullable=True, default=None)      # 到达时间
    succeeded = Column(DateTime(), nullable=True, default=None)     # 成功时间
    failed = Column(DateTime(), nullable=True, default=None)        # 失败时间
    eta = Column(String(255), default='')               # 预计执行时间
    retried = Column(String(255), default='')           # 是否重试过
    parent_id = Column(String(255), default='')         # 父任务ID
    root_id = Column(String(255), default='')           # 根任务ID



