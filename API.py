from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('user_database.db')
c = conn.cursor()

# 添加用户
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    add_user_to_db(data)
    return jsonify({'message': 'User added successfully'})

# 查询所有用户
@app.route('/query_users', methods=['GET'])
def query_all_users():
    users = query_users_from_db()
    return jsonify(users)

# 根据字段查询用户
@app.route('/query_users_by_field', methods=['POST'])
def query_users_by_field():
    field_name = request.json['field_name']
    field_value = request.json['field_value']
    users = query_users_by_field_from_db(field_name, field_value)
    return jsonify(users)

# 根据日期范围查询用户
@app.route('/query_users_by_date_range', methods=['POST'])
def query_users_by_date_range():
    start_date = request.json['start_date']
    end_date = request.json['end_date']
    users = query_users_by_date_range_from_db(start_date, end_date)
    return jsonify(users)

# 计算全部用户总价之和
@app.route('/calculate_total_price', methods=['GET'])
def calculate_total_price():
    total_price = calculate_total_price_from_db()
    return jsonify({'total_price': total_price})

# 计算从开始时间到结束时间全部用户总价之和
@app.route('/calculate_total_price_by_date_range', methods=['POST'])
def calculate_total_price_by_date_range():
    start_date = request.json['start_date']
    end_date = request.json['end_date']
    total_price = calculate_total_price_by_date_range_from_db(start_date, end_date)
    return jsonify({'total_price': total_price})

# 找出箱子尺寸数量最多
@app.route('/find_most_common_box_size', methods=['GET'])
def find_most_common_box_size():
    box_size = find_most_common_box_size_from_db()
    return jsonify({'most_common_box_size': box_size})

# 根据姓名查询用户的全部信息
@app.route('/query_order_by_name', methods=['POST'])
def query_order_by_name():
    name = request.json['name']
    users = query_order_by_name_from_db(name)
    return jsonify(users)

# 删除用户
@app.route('/delete_user', methods=['POST'])
def delete_user():
    date = request.json['date']
    name = request.json['name']
    delete_user_from_db(date, name)
    return jsonify({'message': 'User deleted successfully'})

# 更新用户
@app.route('/update_user', methods=['POST'])
def update_user():
    date = request.json['date']
    name = request.json['name']
    new_data = tuple(request.json['new_data'])
    update_user_in_db(date, name, new_data)
    return jsonify({'message': 'User updated successfully'})

# 添加用户到数据库
def add_user_to_db(data):
    c.execute('''INSERT INTO users (日期,订单号,姓名,手机号,箱子尺寸,价格,箱数,运费,总价,支付方式,支付截图,送货日期,运费_总计,送货地址) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
    conn.commit()

# 从数据库查询所有用户
def query_users_from_db():
    c.execute("SELECT * FROM users ORDER BY 日期 ASC")
    users = c.fetchall()
    return users

# 从数据库根据字段查询用户
def query_users_by_field_from_db(field_name, field_value):
    query = f"SELECT * FROM users WHERE {field_name}=?"
    c.execute(query, (field_value,))
    users = c.fetchall()
    return users

# 从数据库根据日期范围查询用户
def query_users_by_date_range_from_db(start_date, end_date):
    query = "SELECT * FROM users WHERE 日期 BETWEEN ? AND ? ORDER BY 日期 ASC"
    c.execute(query, (start_date, end_date))
    users = c.fetchall()
    return users

# 从数据库计算全部用户总价之和
def calculate_total_price_from_db():
    c.execute("SELECT SUM(总价) FROM users")
    total_price = c.fetchone()[0]
    return total_price

# 从数据库计算从开始时间到结束时间全部用户总价之和
def calculate_total_price_by_date_range_from_db(start_date, end_date):
    query = "SELECT SUM(总价) FROM users WHERE 日期 BETWEEN ? AND ?"
    c.execute(query, (start_date, end_date))
    total_price = c.fetchone()[0]
    return total_price

# 从数据库找出箱子尺寸数量最多
def find_most_common_box_size_from_db():
    c.execute("SELECT 箱子尺寸, SUM(箱数) FROM users GROUP BY 箱子尺寸")
    box_sizes = c.fetchall()
    most_common_box_size = max(box_sizes, key=lambda x: x[1])[0]
    return most_common_box_size

# 从数据库根据姓名查询用户的全部信息
def query_order_by_name_from_db(name):
    query = "SELECT * FROM users WHERE 姓名=?"
    c.execute(query, (name,))
    users = c.fetchall()
    return users

# 从数据库删除用户
def delete_user_from_db(date, name):
    query = "DELETE FROM users WHERE 日期=? AND 姓名=?"
    c.execute(query, (date, name))
    conn.commit()

# 从数据库更新用户
def update_user_in_db(date, name, new_data):
    query = "SELECT * FROM users WHERE 日期=? AND 姓名=?"
    c.execute(query, (date, name))
    result = c.fetchall()
    if not result:
        return
    update_query = "UPDATE users SET 日期=?, 订单号=?, 姓名=?, 手机号=?, 箱子尺寸=?, 价格=?, 箱数=?, 运费=?, 总价=?, 支付方式=?, 支付截图=?, 送货日期=?, 运费_总计=?, 送货地址=? WHERE 日期=? AND 姓名=?"
    c.execute(update_query, (*new_data, date, name))
    conn.commit()

if __name__ == '__main__':
    app.run()
