import sqlite3


# 创建数据库连接
conn = sqlite3.connect('user_database.db')
c = conn.cursor()

# 创建用户表
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              日期 TEXT,
              订单号 TEXT,
              姓名 TEXT,
              手机号 TEXT,
              箱子尺寸 TEXT,
              价格 REAL,
              箱数 INTEGER,
              运费 REAL,
              总价 REAL,
              支付方式 TEXT,
              支付截图 BLOB,
              送货日期 TEXT,
              运费_总计 TEXT,
              送货地址 TEXT)''')


# 定义添加用户函数
def add_user(data):
    # 将用户数据插入数据库
    c.execute('''INSERT INTO users (日期,订单号,姓名,手机号,箱子尺寸,价格,箱数,运费,总价,支付方式,支付截图,送货日期,运费_总计,送货地址) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
    conn.commit()


# 定义查询用户函数
def query_users():
    # 查询数据库中的所有用户数据，并按日期排序
    c.execute("SELECT * FROM users ORDER BY 日期 ASC")
    users = c.fetchall()

    # 打印用户数据
    for user in users:
        print(user)


# 定义通用查询函数
def query_users_by_field(field_name, field_value):
    # 查询数据库中与指定字段匹配的用户数据
    query = f"SELECT * FROM users WHERE {field_name}=?"
    c.execute(query, (field_value,))
    users = c.fetchall()

    # 打印用户数据
    for user in users:
        print(user)


# 定义根据日期范围查询用户函数
def query_users_by_date_range(start_date, end_date):
    # 查询数据库中符合日期范围的用户数据，并按日期排序
    query = "SELECT * FROM users WHERE 日期 BETWEEN ? AND ? ORDER BY 日期 ASC"
    c.execute(query, (start_date, end_date))
    users = c.fetchall()

    # 打印用户数据
    for user in users:
        print(user)


# 定义计算全部用户总价之和的函数
def calculate_total_price():
    # 查询数据库中的全部用户总价字段并计算总和
    c.execute("SELECT SUM(总价) FROM users")
    total_price = c.fetchone()[0]

    # 输出总价之和
    print(f"总价之和：{total_price}")


# 定义计算从开始时间到结束时间全部用户总价之和的函数
def calculate_total_price_by_date_range(start_date, end_date):
    # 查询数据库中在指定日期范围内的全部用户总价字段并计算总和
    query = "SELECT SUM(总价) FROM users WHERE 日期 BETWEEN ? AND ?"
    c.execute(query, (start_date, end_date))
    total_price = c.fetchone()[0]

    # 输出总价之和
    print(f"从 {start_date} 到 {end_date} 的总价之和：{total_price}")


# 定义找出箱子尺寸数量最多的函数
def find_most_common_box_size():
    # 查询数据库中的全部箱子尺寸和箱数
    c.execute("SELECT 箱子尺寸, SUM(箱数) FROM users GROUP BY 箱子尺寸")
    box_sizes = c.fetchall()

    # 找出数量最多的箱子尺寸
    most_common_box_size = max(box_sizes, key=lambda x: x[1])[0]

    # 输出数量最多的箱子尺寸
    print(f"数量最多的箱子尺寸：{most_common_box_size}")


# 定义根据姓名查询用户的全部信息
def query_order_by_name(name):
    # 定义根据姓名查询用户的全部信息
    def query_order_by_name(name):
        # 查询满足姓名条件的用户数据
        query = "SELECT * FROM users WHERE 姓名=?"
        c.execute(query, (name,))
        users = c.fetchall()

        # 如果查询结果为空，则提示未找到用户信息
        if not users:
            print("未找到满足条件的用户信息。")
            return

        # 打印用户数据
        for user in users:
            print(user)

# 定义通过日期和姓名删除用户信息的函数
def delete_user_by_date_and_name(date, name):
    # 查询满足日期和姓名条件的用户信息
    query = "SELECT * FROM users WHERE 日期=? AND 姓名=?"
    c.execute(query, (date, name))
    result = c.fetchone()

    # 如果查询结果为空，则提示未找到用户信息
    if result is None:
        print("未找到满足条件的用户信息。")
        return

    # 删除满足日期和姓名条件的用户信息
    delete_query = "DELETE FROM users WHERE 日期=? AND 姓名=?"
    c.execute(delete_query, (date, name))
    conn.commit()
    print("用户信息已成功删除。")

# 定义通过日期和姓名修改用户信息的函数
def update_user_by_date_and_name(date, name, new_data):
    # 查询满足日期和姓名条件的用户信息
    query = "SELECT * FROM users WHERE 日期=? AND 姓名=?"
    c.execute(query, (date, name))
    result = c.fetchall()

    # 如果查询结果为空，则提示未找到用户信息
    if not result:
        print("未找到满足条件的用户信息。")
        return

    # 更新满足日期和姓名条件的用户信息
    update_query = "UPDATE users SET 日期=?, 订单号=?, 姓名=?, 手机号=?, 箱子尺寸=?, 价格=?, 箱数=?, 运费=?, 总价=?, 支付方式=?, 支付截图=?, 送货日期=?, 运费_总计=?, 送货地址=? WHERE 日期=? AND 姓名=?"
    c.execute(update_query, (*new_data, date, name))
    conn.commit()
    print("用户信息已成功更新。")

# 调用修改用户信息的函数
date = "2022-05-18"
name = "lNsde"
new_data = ("2022-05-18", "New Order", "1234567890", "Medium", 50.0, 2, 10.0, 110.0, "Credit Card", None, "2023-05-20", "Shipping", "123 Main St")
update_user_by_date_and_name(date, name, new_data)


# 调用删除用户信息的函数
# delete_user_by_date_and_name("2022-05-01", "John Doe")

# 查询所有用户
query_users()

# 计算全部用户总价之和并输出
calculate_total_price()

# 计算从开始时间到结束时间全部用户总价之和并输出
start_date = "2022-05-01"
end_date = "2022-05-09"
calculate_total_price_by_date_range(start_date, end_date)

# 找出箱子尺寸数量最多并输出
find_most_common_box_size()

# 查询指定姓名的用户的全部信息
name = "John Doe"
query_order_by_name(name)

# 关闭数据库连接
conn.close()
