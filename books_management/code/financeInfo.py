from books_management.database import mysql_server
def Finance_info():
    if request.method == 'GET':
        # jwt_token=request.META.get("HTTP_AUTHORIZATION")
        # auth=decode_token(jwt_token)
        auth = [True,False]
        # auth[0]=False
        print(auth)
        if auth[0]==True:
            page = request.GET.get('page')
            rows = request.GET.get('rows')
            id = request.GET.get('id')
            project = request.GET.get('project')
            payee = request.GET.get('payee')
            date = request.GET.get('date')
            Payment = request.GET.get('Payment')
            Revenue_expenditure = request.GET.get('Revenue_expenditure')

            field=mysql_server.column_name('finance_info')
            delete_status = 1
            if (not page)or (not rows):
                page=0
                rows=10
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
            sqlText=sql_algorithm.sqlSplicing('finance_info',sqlList,page,rows)
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