import json
import pymysql
from typing import Optional
from pymysql import connect
from pymysql.err import OperationalError, IntegrityError
from pymysql.err import InterfaceError


class UserDatabase:

    def __init__(self, config: dict) -> None:
        self.config = config
        self.cursor = None
        self.connection = None

    def __enter__(self) -> Optional[pymysql.cursors.Cursor]:
        try:
            self.conn = pymysql.connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except OperationalError as err:
            if err.args[0] == 1045:
                print('Неверный логин и пароль, повторите подключение')
                return None
            if err.args[0] == 2003:
                print('Неверно введен порт или хост для подключения к серверу')
                return None
            if err.args[0] == 1049:
                print('Такой базы данных не существует')
                return None
        except UnicodeEncodeError as err:
            print('Были введены символы на русском языке')
            return None
        except TypeError as err:
            print('Неверный формат конфига\n')
        except InterfaceError as err:
            print(err)
            return err

    def __exit__(self, exc_type, exc_value, exc_trace):
        if exc_value:
            if exc_value == 'Курсор не был создан':
                print('Курсор не создан')
            elif exc_value.args[0] == 1064:
                print('Синтаксическая ошибка в запросе!')
                self.conn.commit()
                self.conn.close()
            elif exc_value.args[0] == 1146:
                print('Ошибка в запросе! Такой таблицы не существует.')
                self.conn.commit()
                self.conn.close()
            elif exc_value.args[0] == 1054:
                print('Ошибка в запросе! Такого поля не существует.')
                self.conn.commit()
                self.conn.close()
            exit(1)
        else:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            return True


def get_db_config() -> dict:
    try:
        with open("configs/config.json", 'r') as config:
            db_config = json.load(config)
    except FileNotFoundError as err:
        if err.args[0] == 2:
            print('Такой файл не найден\n')
        print(err.args[1])
        exit(0)
    except json.decoder.JSONDecodeError as err:
        print('Не является файлом .json\n')
        exit(0)
    return db_config


def work_with_db(config: dict, sql: str) -> (list or None):
    with UserDatabase(config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не был создан')
        elif cursor:
            try:
                cursor.execute(sql)
            except pymysql.err.ProgrammingError as err:
                if err.args[0] == 1146:
                    print('Таблицы не существует\n')
                if err.args[0] == 1064:
                    print('Неверный синтаксис запроса\n')
                print(err.args[1])
                return None
            except pymysql.err.OperationalError as err:
                if err.args[0] == 1054:
                    print('Столбец не найден\n')
                print(err.args[1])
                return None
            schema = [column[0] for column in cursor.description]
            result = []
            cursor_result = cursor.fetchall()
            for string in cursor_result:
                result.append(dict(zip(schema, string)))
            #if len(cursor_result)==0:
                #result.append(dict(zip(schema, [""]*len(schema))))
    return result


def change_db(dbconfig, _SQL):

    try:
        with UserDatabase(dbconfig) as cursor:
            cursor.execute(_SQL)
        return True

    except IntegrityError:
        return False


def make_update(config: dict, sql: str) -> bool:
    success = False
    with UserDatabase(config) as cursor:
        if cursor is None:
            raise ValueError('is None')
        cursor.execute(sql)
        success = True
    return success