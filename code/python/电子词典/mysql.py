import pymysql
import hashlib

SALT='&&'

class Database:
    def __init__(self,host='localhost',
                 port=3306,
                 user='root',
                 password='f',
                 charset='utf8',
                 database=None):
        self.host=host
        self.port=port
        self.user=user
        self.password=password
        self.database=database
        self.charset=charset
        self.connect_database()

    def connect_database(self):
        self.db=pymysql.connect(host=self.host,
                                port=self.port,
                                user=self.user,
                                password=self.password,
                                database=self.database,
                                charset=self.charset)
    def close(self):
        self.db.close()

    def create_cursor(self):
        self.cur=self.db.cursor()

    def register(self,name,password):
        sql='select * from user where name="%s"'%name
        self.cur.execute(sql)
        r=self.cur.fetchone()
        
        # 密码加密
        hash=hashlib.md5((name+SALT).encode())
        hash.update(password.encode())
        password=hash.hexdigest()

        # 同if r!=None:
        if r:
            print('用户存在')
            return False
        print('用户不存在')
        sql='insert into user (name,passwd) values ("%s","%s")'%(name,password)
        
        try:
            self.cur.execute(sql)
            self.db.commit()
            print('插入成功')
            return True
        except Exception:
            print('插入失败')
            self.db.rollback()
            return False

    def login(self,name,passwd):
        # 密码加密
        hash=hashlib.md5((name+SALT).encode())
        hash.update(passwd.encode())
        passwd=hash.hexdigest()

        sql='select * from user where name="%s" and passwd="%s"'%(name,passwd)
        self.cur.execute(sql)
        r=self.cur.fetchone()
        if r:
            return True
        else:
            return False
        
    def query(self,word):
        sql='select mean from words where word="%s"'%word
        self.cur.execute(sql)
        r=self.cur.fetchone()
        if r:
            return r[0]

    def insert_hist(self,name,word):
        sql='insert into hist (name,word) \
                values (%s,%s)'
        try:
            self.cur.execute(sql,[name,word])
            self.db.commit()
        except Exception:
            self.db.rollback()

    def history(self,name):
        sql='select name,word,time from hist \
                where name="%s" order by time desc limit 10'%name
        self.cur.execute(sql)
        return self.cur.fetchall()


