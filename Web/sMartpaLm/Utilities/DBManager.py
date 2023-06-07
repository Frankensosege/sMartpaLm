# import psycopg2 as dbl
import MySQLdb as dbl
from sqlalchemy import create_engine, text, engine
import config.settings as conf
import pandas as pd

class DBman:
    def __init__(self):
        dbconf = conf.DATABASES['default']
        # self.prop = cu('./config.ini')
        self.host = dbconf['HOST']   # self.prop.get_property('DB', 'hostname')
        self.dbname = dbconf['NAME']   # self.prop.get_property('DB', 'dbname')
        self.user = dbconf['USER']   # self.prop.get_property('DB', 'username')
        self.password = dbconf['PASSWORD']   # self.prop.get_property('DB', 'password')
        self.port = dbconf['PORT']   # self.prop.get_property('DB', 'port')
        db_engine = dbconf['ENGINE']
        self.dbNm = db_engine.split('.')[3]

    def get_db_nm(self):
        return self.dbNm

    def get_connection(self):
        try:
            if self.dbNm == 'mysql':
                conn = dbl.connect(
                     host=self.host,
                     db=self.dbname,
                     user=self.user,
                     password=self.password,
                     port=int(self.port)
                     )
            elif self.dbNm == 'postgresql':
                conn = dbl.connect(
                    host=self.host,
                    dbname=self.dbname,
                    user=self.user,
                    password=self.password,
                    port=self.port
                )
            else:
                raise Exception("DB를 확인하세요....")
        except Exception as e:
            # sl(__name__).get_logger().error("getDailyPriceNaver : " + str(e))
            return None
        return conn

    def get_alchmy_con(self, mode="REPEATABLE READ"):
        db_pre = 'mysql+mysqldb'
        if self.dbNm == 'postgresql':
            db_pre = 'postgresql+psycopg2'
        engine = create_engine(
            db_pre + f'://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}',
            isolation_level=mode
        )
        return engine

    def get_alchemy_query(self, query):
        return text(query)

    def excuteSQL(self, exec_name, sqlStr, iscommit=True):
        try:
            print(sqlStr)
            # conn = self.get_connection()
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute(sqlStr)
                if iscommit:
                    conn.commit()
        except Exception as e:
            print(e)
            # sl(__name__).get_logger().error(exec_name + str(e))
            return None

        return 0

    def excute_alconn(self, exec_name, sql, alcon_parm='REPEATABLE READ'):
        try:
            print(sql)
            al_conn = self.get_alchmy_con(alcon_parm)
            sql = self.get_alchemy_query(sql)
            with al_conn.begin() as al_conn:
                df = pd.read_sql(sql, al_conn)
        except Exception as e:
            # sl(__name__).get_logger().error("excute_alconn : " + str(e))
            return None

        return df

    def excute_alcon_CUD(self, exec_name, sql):
        try:
            print(sql)
            al_conn = self.get_alchmy_con("AUTOCOMMIT")
            sql = self.get_alchemy_query(sql)
            with al_conn.begin() as al_conn:
                result = al_conn.execute(sql)
        except Exception as e:
            # sl(__name__).get_logger().error("excute_alcon_CUD : " + str(e))
            return None

        return result