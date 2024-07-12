from flask import Flask, jsonify, request
from datetime import datetime
import logging
import pandas as pd
from sqlalchemy import create_engine, text

app = Flask(__name__)

@app.route("/sql_api", methods=['POST'])  # POST method
def sql_api():
    try:
        if request.method == 'POST':
            '''JSON Format
            {
                "operation":"create",
                "host":"localhost",
                "user":"root",
                "password":"root",
                "db":"tuto",
                "table":"flask_crud"
            }
            '''
            # logging.info("Request: %s",request.json)       #log all the request and response into log file that shown in console
            operation = request.json['operation']  # get operation from request
            host = request.json['host']  # get host from request
            user = request.json['user']  # get user from request
            password = request.json['password']  # get password from request
            db = request.json['db']  # get db from request
            table = request.json['table']  # get table from request
            engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{db}")  # connect to database

            with engine.connect() as connection:
                if operation == 'create':  # create table
                    '''
                    for creating table
                    Json Format
                    {
                        "columns":{"columns_name":"data_type(size)",..."}
                    }
                    '''
                    col = request.json['columns']  # get columns from request
                    columns = ''
                    for i in col:
                        columns += i + ' ' + col.get(i) + ','  # create columns with data type and size
                    columns = columns[:-1]  # remove last comma
                    query = text(f"CREATE TABLE {table} ({columns})")
                    connection.execute(query)  # create table
                    msg = {"status": "success", "msg": f"Table '{table}' Created !"}  # create success message

                elif operation == 'insert':  # insert data into table
                    '''
                    for inserting data
                    Json Format
                    {
                        'data':"data separated by comma"
                    }
                    '''
                    data = request.json['data']  # get data from request
                    query = text(f'INSERT INTO {table} VALUES {data}')
                    connection.execute(query)  # insert data into table
                    msg = {"status": "success", "msg": f"Data inserted into {table}"}  # create success message

                elif operation == 'update':  # update data into table
                    '''
                    for updating data
                    Json Format
                    {
                        "set": "key=value" pair of columns & values to be updated
                        "where": "condition"
                    }
                    '''
                    set = request.json['set']  # get set from request
                    where = request.json['where']  # get where from request

                    if len(set) > 0 and len(where) > 0:
                        query = text(f'UPDATE {table} SET {set} WHERE {where}')
                        out = connection.execute(query)  # update data into table
                        if out.rowcount > 0:  # check if data updated or if updated that means data is present if not then data is not present
                            msg = {"status": "success", "msg": "Data Updated !"}  # create success message
                        else:  # if data not updated
                            msg = {"status": "failed", "msg": "Unable to Update! Please check SET and WHERE conditions !"}  # create failed message
                    else:
                        msg = {"status": "error", "msg": "Please provide valid SET and WHERE conditions !"}

                elif operation == 'delete':  # delete data into table
                    '''
                    for deleting data
                    Json Format
                    {
                        "table":"tb_name",
                        "where": "condition"
                    }
                    '''
                    where = request.json['where']  # get where from request
                    if len(where) > 0:
                        query = text(f"DELETE FROM {table} WHERE {where}")
                        out = connection.execute(query)  # delete data into table
                        if out.rowcount > 0:  # check if data deleted or if deleted that means data is present if not then data is not present
                            msg = {"status": "success", "msg": "Data Deleted !"}  # create success message
                        else:  # if data not deleted
                            msg = {"status": "error", "msg": "Data not found"}  # create error message
                    else:
                        msg = {"status": "error", "msg": "Please provide 'WHERE' condition !"}

                elif operation == 'bulk':  # bulk insert data into table
                    '''
                    for bulk inserting data
                    Json Format
                    {
                        "f_path":"file_path",
                        "table":"tb_name",
                        "columns":"columns_name"
                    }
                    '''
                    f_path = request.json['filepath']  # get filepath from request
                    col = request.json['columns']  # get columns from request if columns is not given("") or given asterisk ("*"") then it will take all columns

                    if col == '*' or col == '':
                        df = pd.read_csv(f_path)
                        df.to_sql(table, connection, index=False, if_exists='append')
                    else:
                        df = pd.read_csv(f_path, usecols=col.split(","))
                        df.to_sql(table, connection, index=False, if_exists='append')

                    msg = {"status": "success", "msg": f"Data Loaded to table - {table} !"}

                elif operation == 'download':  # download data from table
                    '''
                    for downloading data
                    Json Format
                    {
                        "table":"tb_name",
                        "where": "condition"
                    }
                    '''
                    where = request.json['where']  # get where from request
                    col = request.json['columns']

                    if len(where) == 0:
                        if col == '*' or col == '':
                            df = pd.read_sql(f"SELECT * FROM {table}", con=connection)
                        else:
                            df = pd.read_sql(f"SELECT {col} FROM {table}", con=connection)
                    else:
                        if col == '*' or col == '':
                            df = pd.read_sql(f"SELECT * FROM {table} WHERE {where}", con=connection)
                        else:
                            df = pd.read_sql(f"SELECT {col} FROM {table} WHERE {where}", con=connection)

                    if df.empty:
                        msg = {"status": "error", "msg": "No data found with matched conditions !"}
                    else:
                        df.to_csv(f'outfile/{table}-{str(datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p"))}.csv', index=False)
                        msg = {"status": "success", "msg": "Data Downloaded at 'outfile' folder"}

                else:  # if operation is not given
                    msg = {"status": "fail", "msg": "Invalid Operation"}  # create fail message

            return jsonify(msg)  # return success message in json format

    except Exception as e:  # if any exception occurs
        # logging.error("Exception: %s",e)  # log error
        return jsonify({"status": "fail", "errors": f"Exception -{str(e)}"})  # return error message in json format with exception

if __name__ == '__main__':
    app.run()
