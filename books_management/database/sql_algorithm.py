def sqlSplicing(tableName,sqllist,page=0,rows=10):
    print(tableName,sqllist)

    sqlA = f"select * from {tableName} where "
    count_sql = f"select count(1) from (select a.id from {tableName} a where"
    sqlC =f"order by id desc limit {page} ,{rows};"
    num = 0
    sqltextlist=[]
    if len(sqllist) == 0:
        sql = sqlA.replace('where', ' ') + sqlC
        count_sql = f"select count(1) from (select a.id from {tableName} a)b;"
        return {'sql': sql, 'count_sql': count_sql}
    for sqlText in sqllist:
        if num ==0:
            sqlText=sqlText.replace('and','')
        sqltextlist.append(sqlText)
        num+=1
    sqlB = " ".join(sqltextlist)
    sql =sqlA+sqlB+sqlC
    count_sql = count_sql+sqlB+')b;'
    return {'sql':sql,'count_sql':count_sql}