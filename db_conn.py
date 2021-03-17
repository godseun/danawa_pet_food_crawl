import mysql.connector
import json
import config

config = config.config

def push_prod_data(data):
    try:
        conn = mysql.connector.connect(**config)
        # db select, insert, update, delete 작업 객체
        cursor = conn.cursor()
        # 실행할 select 문 구성
        sql = f"SELECT * FROM danawa_product where parent_pcode = '{data['pcode']}' "
        # cursor 객체를 이용해서 수행한다.
        cursor.execute(sql)
        resultList = cursor.fetchall()
        conn.close()

        if len(resultList) == 0:
            add_product(data)
        else:
            modify_product(data)

    except:
        print(sql)
        print(mysql.connector.Error)

def modify_product(data):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        sql = f"UPDATE danawa_product SET parent_pcode='{data['pcode']}', prod_name='{data['prod_name']}', thumb='{data['thumb']}', `desc`='{data['desc']}', href='{data['href']}'  where parent_pcode='{data['pcode']}'"
        cursor.execute(sql)
        conn.commit()
        conn.close()

    except Exception as e:
        print("update ", mysql.connector.Error)
        print(data)
        print(e)

def add_product(data):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        sql = f"INSERT INTO danawa_product (`parent_pcode`, `prod_name`, `thumb`, `desc`, `href`) \
            values('{data['pcode']}', '{data['prod_name']}', '{data['thumb']}', '{data['desc']}', '{data['href']}');"
        cursor.execute(sql)
        conn.commit()
        conn.close()

    except Exception as e:
        print("insert ", mysql.connector.Error)
        print(data)
        print(e)


def push_prod_data2(data):
    try:
        conn = mysql.connector.connect(**config)
        # db select, insert, update, delete 작업 객체
        cursor = conn.cursor()
        # 실행할 select 문 구성
        sql = f"SELECT * FROM danawa_product_detail where pcode = '{data['pcode']}' and parent_pcode = '{data['parent_pcode']}' "
        # cursor 객체를 이용해서 수행한다.
        cursor.execute(sql)
        resultList = cursor.fetchall()
        conn.close()

        if len(resultList) == 0:
            add_product2(data)
        else:
            modify_product2(data)

    except:
        print(mysql.connector.Error)

def modify_product2(data):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        sql = f"UPDATE danawa_product_detail SET parent_pcode='{data['parent_pcode']}', pcode='{data['pcode']}', price='{data['price']}', href='{data['href']}', ext1='{data['ext1']}', ext2='{data['ext2']}'  where pcode='{data['pcode']}' and parent_pcode = '{data['parent_pcode']}'"
        cursor.execute(sql)
        conn.commit()
        conn.close()

    except Exception as e:
        print("update ", mysql.connector.Error)
        print(data)
        print(e)

def add_product2(data):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        sql = f"INSERT INTO danawa_product_detail(`parent_pcode`, `pcode`, `price`, `href`, `ext1`, `ext2`) \
            values('{data['parent_pcode']}', '{data['pcode']}', '{data['price']}', '{data['href']}', '{data['ext1']}', '{data['ext2']}');"
        cursor.execute(sql)
        conn.commit()
        conn.close()

    except Exception as e:
        print("insert ", mysql.connector.Error)
        print(data)
        print(e)