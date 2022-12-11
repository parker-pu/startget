# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2022-2025
"""
from PyQt6.QtCore import QObject
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from src.apps.comm.msg import Msg


class DB(QObject, Msg):
    """
    操作数据库
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = None
        self.db_connect()
        self.create_table()

    def db_connect(self):
        """
        创建连接
        :return:
        """
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName("start_get.db")
        if not self.db.open():
            self.error(self.db.lastError().text())

    def closeEvent(self, *args, **kwargs):
        self.db.close()

    def __del__(self):
        self.db.close()

    def exec(self, sql, *args, **kwargs):
        """
        执行sql
        :param sql:
        :param args:
        :param kwargs:
        :return:
        """
        query = QSqlQuery(db=self.db)
        query.exec(sql)
        return query

    def create_table(self):
        """
        创建数据库表
        :return:
        """
        # downloads 记录下载信息的表
        self.exec("CREATE TABLE IF NOT EXISTS downloads ("
                  "id INTEGER primary key AUTOINCREMENT,"
                  "name varchar(255) NOT NULL,"
                  "data_size varchar(255) NOT NULL,"
                  "data_md5 varchar(255) NOT NULL,"
                  "url TEXT not null,"
                  "status varchar(10) not null default 'WAIT', "
                  "loaded int(3) not null default 0, "
                  "file_path text not null)")
        # constance_config 配置表
        self.exec("CREATE TABLE IF NOT EXISTS constance_config ("
                  "id INTEGER primary key AUTOINCREMENT,"
                  "key varchar(255) NOT NULL,"
                  "value longtext )")

        # self.exec("INSERT INTO constance_config (key, value) VALUES('FILE_PATH', 'E:/code/startget');")
