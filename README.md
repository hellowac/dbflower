# dbflower

flower 的二次开发，可以存储任务状态到mysql数据库中


#### 将此项目拷贝到目标项目作为一个包使用

```text
├── app     # 项目web模块
│   ├── mixin
│   ├── models
│   ├── static
│   ├── templates
│   ├── utils
│   └── views
├── to       # celery 任务模块
│   ├── celery
│   └── tasks
├── flower   # flower单独作为一个包使用
│   ├── api
│   ├── db
│   ├── static
│   ├── templates
│   ├── utils
│   └── views
└── spider   # 项目其他模块
```


#### 和其他使用celery的项目一起调用方式

```bash
# 任务信息不存储到mysql启动方式
python flower.py -A to.celery:app -l info

# 任务信息存储mysql启动方式
python flower.py -A to.celery:app -l info --db-mysql=root:root@localhost:3306/test
```

#### 修改数据连接地址

flower.db.api.conn_str

