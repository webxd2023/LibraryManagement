import json

from django.shortcuts import render
import time
from django.http import JsonResponse, HttpResponse
from books_management.database import sql_algorithm
from books_management.tools.jwt_token import decode_token, encode_token
from books_management.database import mysql_server
from books_management.tools.logGenerator import ret_logger
from books_management.tools.ran_code import vvcode
from books_management.config import conf
from books_management.tools.AesDec import decrypt
from books_management.tools.AesEnc import encrypt
from books_management.code.financeInfo import Finance_info


# Create your views here.
def nowTime():
  return int(time.time())

def is_time_str(times):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(times))

loger = ret_logger("books_management/log/books.log")

def user_info(request):
    if request.method == 'GET':
        jwt_token=request.META.get("HTTP_AUTHORIZATION")
        auth=decode_token(jwt_token)
        # auth = [False,True]
        # auth[0]=False
        print(auth)
        if auth[0]==True:
            page = request.GET.get('page')
            rows = request.GET.get('rows')
            user_id = request.GET.get('id')
            user_name = request.GET.get('user_name')
            user_phone = request.GET.get('user_phone')
            status = request.GET.get('status')
            field=mysql_server.column_name('user_info')
            delete_status = 1
            if (not page)or (not rows):
                page=0
                rows=10
            page = int(page) * int(rows)
            sqlList = []
            if user_id:
                sqlList.append(f'and id = {user_id} ')
            if user_name:
                sqlList.append(f'and user_name = "{user_name}" ')
            if user_phone:
                sqlList.append(f'and user_phone = "{user_phone}" ')
            if status:
                sqlList.append(f'and status = "{status}" ')
            if delete_status:
                sqlList.append(f'and delete_status = "{delete_status}" ')
            loger.info(f'sqllist:{sqlList}')
            data = []
            valst = []
            keylst = []
            sqlText=sql_algorithm.sqlSplicing('user_info',sqlList,page,rows)
            loger.info(f'sqlText:{sqlText}')
            countsql=sqlText.get('count_sql')
            sql=sqlText.get('sql')
            datanum=mysql_server.get_user_info_list(countsql)[0][0]
            sqldata=mysql_server.get_user_info_list(sql)
            for i in range(len(sqldata)):
                dds = sqldata[i]
                for ix in range(len(dds)):
                   vals = dds[ix]
                   if (field[ix] == 'register_date') or (field[ix] == 'expiration_date'):
                       vals = is_time_str(int(dds[ix]))
                   valst.append(vals)
                   keylst.append(field[ix])
                kvjson=dict(zip(keylst,valst))
                data.append(kvjson)
            itemzise = len(data)
            infos = {'code': 200, 'msg': '获取成功','itemzise': itemzise, 'datazise':datanum,'data': data}
        else:
            infos={'code':401,'msg':'登录已过期','data':'null'}
        return JsonResponse(infos)
    elif request.method == 'POST':
        jwt_token = request.META.get("HTTP_AUTHORIZATION")
        auth = decode_token(jwt_token)
        # auth = [False, True]
        if auth[0]==True:
            body=request.body
            json_body = eval(body.decode())
            avatar = json_body.get('avatar')
            sex = json_body.get('sex')
            user_name = json_body['user_name']
            user_phone = json_body['user_phone']
            user_address = json_body['user_address']
            ntime = nowTime()
            sql = f"INSERT INTO user_info VALUES (null,'{avatar}',{sex},'{user_name}','{user_phone}','{user_address}','{ntime}','{ntime+31536000}',1,1);"
            loger.info(f'sql:{sql}')
            user_id = mysql_server.add_user_info(sql)
            info = {'code': 200, 'msg': '添加成功', 'user_info': {'user_id': user_id, 'avatar':avatar,'sex':sex,'user_name': user_name, 'user_phone': user_phone}}
            return JsonResponse(info)
    elif request.method  == 'PUT':
        jwt_token = request.META.get("HTTP_AUTHORIZATION")
        auth = decode_token(jwt_token)
        # auth = [True, True]
        if auth[0]==True:
            body=request.body
            json_body = eval(body.decode())
            id=json_body['id']
            avatar = json_body.get('avatar')
            user_name = json_body.get('user_name')
            sex = json_body.get('sex')
            user_phone = json_body.get('user_phone')
            user_address = json_body.get('user_address')
            status = json_body.get('status')
            sql = f"update user_info set  user_name = '{user_name}',user_phone='{user_phone}',sex = '{sex}',avatar='{avatar}',user_address='{user_address}',status={status} where id = {id} ;"
            loger.info(f'sql:{sql}')
            re=mysql_server.com_up(sql)
        else:
            re={'code':401,'msg':'登录已过期','data':'null'}
        return JsonResponse(re)
    elif request.method  == 'DELETE':
        jwt_token = request.META.get("HTTP_AUTHORIZATION")
        auth = decode_token(jwt_token)
        # auth = [True, True]
        if auth[0]==True:
            body=request.body
            if not body:
                return JsonResponse({'code': 403, 'msg': '未收到参数', 'data': 'null'})
            else:

                json_body = eval(body.decode())
                id = json_body.get("id")
                if not id:
                    return JsonResponse({'code': 403, 'msg': '缺少用户id', 'data': 'null'})
                else:
                    if type(id)==int:
                        id = [id]
                    if len(id) == 0:
                        return JsonResponse({'code': 403, 'msg': '缺少用户id', 'data': 'null'})
                    else:
                        for i in id:
                            sql = f"update user_info set  delete_status = 2 where id = {i} ;"
                            loger.info(f'sql:{sql}')
                            mysql_server.delsql(sql)
                        return JsonResponse({'code': 200, 'msg': f'删除了{len(id)}数据', 'data': 'null'})
        else:
            re={'code':401,'msg':'登录已过期','data':'null'}
        return JsonResponse(re)
    else:
        return HttpResponse('method error')

def books_info(request):
    if request.method == 'GET':
        jwt_token=request.META.get("HTTP_AUTHORIZATION")
        auth=decode_token(jwt_token)
        # auth = [False,True]
        # auth[0]=False
        print(auth)
        if auth[0] ==True:
            page = request.GET.get('page')
            rows = request.GET.get('rows')
            books_id = request.GET.get('id')
            books_name = request.GET.get('books_name')  # 图书名称
            books_author = request.GET.get('author')   # 作者
            books_press = request.GET.get('press')    # 出版社
            books_classify = request.GET.get('classify')  # 图书分类
            book_status = request.GET.get('book_status')  # 图书状态
            print(f"图书状态:{book_status}")
            delete_status = 1
            field=mysql_server.column_name('books_info')
            if (not page)or (not rows):
                page=0
                rows=10
            page = int(page) * int(rows)
            sqlList = []
            if books_id:
                sqlList.append(f'and id = {books_id} ')
            if books_name:
                sqlList.append(f'and book_name = "{books_name}" ')
            if books_author:
                sqlList.append(f'and author = "{books_author}" ')
            if books_press:
                sqlList.append(f'and press = "{books_press}" ')
            if books_classify:
                sqlList.append(f'and classify = "{books_classify}" ')
            if book_status:
                sqlList.append(f'and book_status = "{book_status}" ')
            if delete_status:
                sqlList.append(f'and delete_status = "{delete_status}" ')
            print(sqlList)
            data = []
            valst = []
            keylst = []
            sqlText=sql_algorithm.sqlSplicing('books_info',sqlList,page,rows)
            countsql=sqlText.get('count_sql')
            sql=sqlText.get('sql')
            loger.info(f'sql:{sql}')
            loger.info(f'countsql:{countsql}')
            datanum=mysql_server.get_user_info_list(countsql)[0][0]
            sqldata=mysql_server.get_user_info_list(sql)
            for i in range(len(sqldata)):
                dds = sqldata[i]
                for ix in range(len(dds)):
                   vals = dds[ix]
                   if (field[ix] == 'books_add_time'):
                       vals = is_time_str(int(dds[ix]))
                   valst.append(vals)
                   keylst.append(field[ix])
                kvjson=dict(zip(keylst,valst))
                data.append(kvjson)
            itemzise = len(data)
            infos = {'code': 200, 'msg': '获取成功','itemzise': itemzise, 'datazise':datanum,'data': data}
        else:
            infos={'code':401,'msg':'登录已过期','data':'null'}
        return JsonResponse(infos)
    elif request.method == 'POST':
        # jwt_token = request.META.get("HTTP_AUTHORIZATION")
        # auth = decode_token(jwt_token)
        auth = [False, True]
        if auth[0] != True:
            body = request.body
            json_body = eval(body.decode())
            book_name = json_body.get('book_name')
            book_press = json_body.get('press')
            book_author = json_body.get('author')
            book_price = json_body.get('price')
            book_classify = json_body.get('classify')
            book_image_url = json_body.get('book_image_url')
            ntime = nowTime()
            sql = f"INSERT INTO books_info VALUES (null,'{book_name}','{book_press}','{book_author}','{book_price}','{book_classify}','{book_image_url}','{ntime}',1,1,1);"
            loger.info(f'insertsql:{sql}')
            book_id = mysql_server.add_user_info(sql)
            info = {'code': 200, 'msg': '添加成功',
                    'book_info': {'book_id': book_id, 'book_name': book_name, 'book_press':book_press,'book_author': book_author}}
            return JsonResponse(info)
    elif request.method == "PUT":
        # jwt_token = request.META.get("HTTP_AUTHORIZATION")
        # auth = decode_token(jwt_token)
        auth = [True, True]
        if auth[0] == True:
            body = request.body
            json_body = eval(body.decode())
            id = json_body['id']
            book_name = json_body.get('book_name')
            book_press = json_body.get('press')
            book_author = json_body.get('author')
            book_price = json_body.get('price')
            book_classify = json_body.get('classify')
            book_image_url = json_body.get('book_image_url')
            book_status = json_body.get('book_status')
            sql = f"update books_info set  book_name = '{book_name}',press='{book_press}',author='{book_author}',price='{book_price}',classify='{book_classify}',book_image_url='{book_image_url}',book_status = '{book_status}' where id = {id} ;"
            loger.info(f'updatesql:{sql}')
            re = mysql_server.com_up(sql)
        else:
            re = {'code': 401, 'msg': '登录已过期', 'data': 'null'}
        return JsonResponse(re)
    if request.method  == 'DELETE':
        # jwt_token = request.META.get("HTTP_AUTHORIZATION")
        # auth = decode_token(jwt_token)
        auth = [True, True]
        if auth[0]==True:
            body=request.body
            if not body:
                return JsonResponse({'code': 403, 'msg': '未收到参数', 'data': 'null'})
            else:

                json_body = eval(body.decode())
                if not json_body.get("id"):
                    return JsonResponse({'code': 403, 'msg': '请输入图书id', 'data': 'null'})
                else:
                    id = json_body.get("id")
                    sql = f"update books_info set  delete_status = 2 where id = {id} ;"
                    loger.info(f'deletesql:{sql}')
                    re=mysql_server.delsql(sql)
        else:
            re={'code':401,'msg':'登录已过期','data':'null'}
        return JsonResponse(re)
    else:
        return HttpResponse('method error')


def admin_info(request):
    if request.method == 'GET':
        # jwt_token=request.META.get("HTTP_AUTHORIZATION")
        # auth=decode_token(jwt_token)
        auth = [False,True]
        # auth[0]=False
        print(auth)
        if auth[0]!=True:
            page = request.GET.get('page')
            rows = request.GET.get('rows')
            admin_id = request.GET.get('id')
            admin_name = request.GET.get('admin_name')  # 管理员名称
            admin_status = request.GET.get('status')    # 管理员状态
            delete_status = 1
            field=mysql_server.column_name('admin_info')
            if (not page)or (not rows):
                page=0
                rows=10
            page = int(page) * int(rows)
            sqlList = []
            if admin_id:
                sqlList.append(f'and id = {admin_id} ')
            if admin_name:
                sqlList.append(f'and admin_name = "{admin_name}" ')
            if admin_status:
                sqlList.append(f'and admin_status = "{admin_status}" ')
            if delete_status:
                sqlList.append(f'and delete_status = "{delete_status}" ')
            print(sqlList)
            data = []
            valst = []
            keylst = []
            sqlText=sql_algorithm.sqlSplicing('admin_info',sqlList,page,rows)
            countsql=sqlText.get('count_sql')
            sql=sqlText.get('sql')
            loger.info(f'sql:{sql}')
            loger.info(f'countsql:{countsql}')
            datanum=mysql_server.get_user_info_list(countsql)[0][0]
            sqldata=mysql_server.get_user_info_list(sql)
            for i in range(len(sqldata)):
                dds = sqldata[i]
                for ix in range(len(dds)):
                   vals = dds[ix]
                   valst.append(vals)
                   keylst.append(field[ix])
                kvjson=dict(zip(keylst,valst))
                data.append(kvjson)
            itemzise = len(data)
            infos = {'code': 200, 'msg': '获取成功','itemzise': itemzise, 'datazise':datanum,'data': data}
        else:
            infos={'code':401,'msg':'登录已过期','data':'null'}
        return JsonResponse(infos)
    elif request.method == 'POST':
        # jwt_token = request.META.get("HTTP_AUTHORIZATION")
        # auth = decode_token(jwt_token)
        auth = [False, True]
        if auth[0] != True:
            body = request.body
            json_body = eval(body.decode())
            admin_name = json_body.get('admin_name')
            admin_password = json_body.get('admin_password')
            ntime = nowTime()
            sql = f"INSERT INTO admin_info VALUES (null,'{admin_name}','{admin_password}',1,1);"
            loger.info(f'insertsql:{sql}')
            admin_id = mysql_server.add_user_info(sql)
            info = {'code': 200, 'msg': '添加成功',
                    'book_info': {'id': admin_id, 'admin_name': admin_name}}
            return JsonResponse(info)
    elif request.method == "PUT":
        # jwt_token = request.META.get("HTTP_AUTHORIZATION")
        # auth = decode_token(jwt_token)
        auth = [True, True]
        if auth[0] == True:
            body = request.body
            json_body = eval(body.decode())
            id = json_body.get('id')
            admin_name = json_body.get('admin_name')
            admin_status = json_body.get('admin_status')
            sql = f"update admin_info set  admin_name = '{admin_name}',admin_status='{admin_status}' where id = {id} ;"
            loger.info(f'updatesql:{sql}')
            re = mysql_server.com_up(sql)
        else:
            re = {'code': 401, 'msg': '登录已过期', 'data': 'null'}
        return JsonResponse(re)
    if request.method  == 'DELETE':
        # jwt_token = request.META.get("HTTP_AUTHORIZATION")
        # auth = decode_token(jwt_token)
        auth = [True, True]
        if auth[0]==True:
            body=request.body
            if not body:
                return JsonResponse({'code': 403, 'msg': '未收到参数', 'data': 'null'})
            else:

                json_body = eval(body.decode())
                if not json_body.get("id"):
                    return JsonResponse({'code': 403, 'msg': '管理员id为空', 'data': 'null'})
                else:
                    id = json_body.get("id")
                    sql = f"update admin_info set  delete_status = 2 where id = {id} ;"
                    loger.info(f'deletesql:{sql}')
                    re=mysql_server.delsql(sql)
        else:
            re={'code':401,'msg':'登录已过期','data':'null'}
        return JsonResponse(re)
    else:
        return HttpResponse('method error')


def classify_info(request):
    if request.method == 'GET':
        # jwt_token=request.META.get("HTTP_AUTHORIZATION")
        # auth=decode_token(jwt_token)
        auth = [False,True]
        # auth[0]=False
        print(auth)
        if auth[0]!=True:
            page = request.GET.get('page')
            rows = request.GET.get('rows')
            classify_id = request.GET.get('id')
            classify_name = request.GET.get('classify_name')  # 分类名称
            classify_status = request.GET.get('classify_status')   # 分类状态
            delete_status = 1
            field=mysql_server.column_name('classify_info')
            if (not page)or (not rows):
                page=0
                rows=10
            page = int(page) * int(rows)
            sqlList = []
            if classify_id:
                sqlList.append(f'and id = {classify_id} ')
            if classify_name:
                sqlList.append(f'and classify_name = "{classify_name}" ')
            if classify_status:
                sqlList.append(f'and classify_status = "{classify_status}" ')
            if delete_status:
                sqlList.append(f'and delete_status = "{delete_status}" ')
            print(sqlList)
            data = []
            valst = []
            keylst = []
            sqlText=sql_algorithm.sqlSplicing('classify_info',sqlList,page,rows)
            countsql=sqlText.get('count_sql')
            sql=sqlText.get('sql')
            loger.info(f'sql:{sql}')
            loger.info(f'countsql:{countsql}')
            datanum=mysql_server.get_user_info_list(countsql)[0][0]
            sqldata=mysql_server.get_user_info_list(sql)
            for i in range(len(sqldata)):
                dds = sqldata[i]
                for ix in range(len(dds)):
                   vals = dds[ix]
                   valst.append(vals)
                   keylst.append(field[ix])
                kvjson=dict(zip(keylst,valst))
                data.append(kvjson)
            itemzise = len(data)
            infos = {'code': 200, 'msg': '获取成功','itemzise': itemzise, 'datazise':datanum,'data': data}
        else:
            infos={'code':401,'msg':'登录已过期','data':'null'}
        return JsonResponse(infos)
    elif request.method == 'POST':
        # jwt_token = request.META.get("HTTP_AUTHORIZATION")
        # auth = decode_token(jwt_token)
        auth = [False, True]
        if auth[0] != True:
            body = request.body
            json_body = eval(body.decode())
            classify_name = json_body.get('classify_name')
            ntime = nowTime()
            sql = f"INSERT INTO classify_info VALUES (null,'{classify_name}',1,1);"
            loger.info(f'insertsql:{sql}')
            classify_id = mysql_server.add_user_info(sql)
            info = {'code': 200, 'msg': '添加成功',
                    'book_info': {'id': classify_id, 'classify_name': classify_name}}
            return JsonResponse(info)
    elif request.method == "PUT":
        # jwt_token = request.META.get("HTTP_AUTHORIZATION")
        # auth = decode_token(jwt_token)
        auth = [True, True]
        if auth[0] == True:
            body = request.body
            json_body = eval(body.decode())
            id = json_body.get('id')
            classify_name = json_body.get('classify_name')
            classify_status = json_body.get('classify_status')
            sql = f"update classify_info set  classify_name = '{classify_name}',classify_status='{classify_status}' where id = {id} ;"
            loger.info(f'updatesql:{sql}')
            re = mysql_server.com_up(sql)
        else:
            re = {'code': 401, 'msg': '登录已过期', 'data': 'null'}
        return JsonResponse(re)
    if request.method  == 'DELETE':
        # jwt_token = request.META.get("HTTP_AUTHORIZATION")
        # auth = decode_token(jwt_token)
        auth = [True, True]
        if auth[0]==True:
            body=request.body
            if not body:
                return JsonResponse({'code': 403, 'msg': '未收到参数', 'data': 'null'})
            else:

                json_body = eval(body.decode())
                if not json_body.get("id"):
                    return JsonResponse({'code': 403, 'msg': '分类id为空', 'data': 'null'})
                else:
                    id = json_body.get("id")
                    sql = f"update classify_info set  delete_status = 2 where id = {id} ;"
                    loger.info(f'deletesql:{sql}')
                    re=mysql_server.delsql(sql)
        else:
            re={'code':401,'msg':'登录已过期','data':'null'}
        return JsonResponse(re)
    else:
        return HttpResponse('method error')
def vercode(request):
    if request.method == 'GET':
        verifCode=vvcode()
        return JsonResponse({'code': 200, 'verCode': verifCode})
    else:
        return HttpResponse('method error')

def admin_login(request):
    if request.method  == 'POST':
        body=request.body.decode('utf-8')
        if not body:
            return JsonResponse({'code': -1, 'msg': '参数不能为空'})
        else:
            json_body = json.loads(body)
            try:
                user = json_body['user']
                pwd = json_body['pwd']
            except Exception as e:
                info={'code': -1, 'msg': f'{e}-参数解析失败'}
            if not user:
                info={'code':-1,'msg':'用户名不能为空'}
            elif not pwd:
                info = {'code': -1, 'msg': '密码不能为空'}
            elif len(user)<5:
                info={'code': -1, 'msg': '用户名不能小于5位字符'}
            elif len(str(pwd))<8:
                info={'code': -1, 'msg': '密码不能小于8位字符'}
            else:
                key = conf.KEY
                try:
                    sql = f"select id,password,username from users where  user = '{user}';"
                    userinfo = mysql_server.get_user_info_list(sql)[0]
                    user_id=userinfo[0]
                    name=userinfo[2]
                    dbpwd=decrypt(key,userinfo[1])
                    print(dbpwd)
                    if pwd==dbpwd[1]:
                        jwt_token = encode_token(user_id, name)
                        info={'code': 200, 'msg': f'登录成功','jwt_token':jwt_token,'user_info':{'user_id':user_id,'user_name':name,}}
                    else:
                        print('用户名密码错误')
                        info={'code': -1, 'msg': f'用户名或密码错误'}
                except Exception as e:
                    print(e)
                    info = {'code': -2, 'msg': f'登录出错{e}'}
        return JsonResponse(info)

def financeInfos(request):
    if request.method == 'GET':
        # jwt_token=request.META.get("HTTP_AUTHORIZATION")
        # auth=decode_token(jwt_token)
        auth = [True, False]
        # auth[0]=False
        print(auth)
        if auth[0] == True:
            page = request.GET.get('page')
            rows = request.GET.get('rows')
            id = request.GET.get('id')
            project = request.GET.get('project')
            payee = request.GET.get('payee')
            date = request.GET.get('date')
            Payment = request.GET.get('Payment')
            Revenue_expenditure = request.GET.get('Revenue_expenditure')

            field = mysql_server.column_name('finance_info')
            delete_status = 1
            if (not page) or (not rows):
                page = 0
                rows = 10
            page = int(page) * int(rows)
            sqlList = []
            if id:
                sqlList.append(f'and id = {id} ')
            if project:
                sqlList.append(f'and project = "{project}" ')
            if payee:
                sqlList.append(f'and payee = "{payee}" ')
            if date:
                sqlList.append(f'and date = "{date}" ')
            if Payment:
                sqlList.append(f'and Payment = "{Payment}" ')
            if Revenue_expenditure:
                sqlList.append(f'and Revenue_expenditure = "{Revenue_expenditure}" ')
            loger.info(f'sqllist:{sqlList}')
            data = []
            valst = []
            keylst = []
            sqlText = sql_algorithm.sqlSplicing('finance_info', sqlList, page, rows)
            loger.info(f'sqlText:{sqlText}')
            countsql = sqlText.get('count_sql')
            sql = sqlText.get('sql')
            datanum = mysql_server.get_user_info_list(countsql)[0][0]
            sqldata = mysql_server.get_user_info_list(sql)
            loger.info(f'财务数据库返回:{sqldata}')
            for i in range(len(sqldata)):
                dds = sqldata[i]
                for ix in range(len(dds)):
                    vals = dds[ix]
                    if (field[ix] == 'register_date') or (field[ix] == 'expiration_date'):
                        vals = is_time_str(int(dds[ix]))
                    valst.append(vals)
                    keylst.append(field[ix])
                kvjson = dict(zip(keylst, valst))
                data.append(kvjson)
            itemzise = len(data)
            infos = {'code': 200, 'msg': '获取成功', 'itemzise': itemzise, 'datazise': datanum, 'data': data}
        else:
            infos = {'code': 401, 'msg': '登录已过期', 'data': 'null'}
        loger.info(f'接口返回:{infos}')
        return JsonResponse(infos)
# print(is_time_str(1672986180))