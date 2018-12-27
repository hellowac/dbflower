# dbflower

flower 的二次开发，可以存储任务状态到mysql数据库中


#### 和其他使用celery的项目一起调用方式

```bash
python flower.py -A celery_module.celery:app -l info --db=flower.db
```

#### 修改数据连接地址

flower.db.api.conn_str

