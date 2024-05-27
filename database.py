import sqlite3

def make_db():
    conn = sqlite3.connect("pizza_db.db")
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS customer_info (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50) NOT NULL,
        phone_number INT NOT NULL,
        address VARCHAR(100) NOT NULL
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS pizza_info (
        pizza_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        price INT NOT NULL
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders_info (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INT NOT NULL,
        order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        total_amount DECIMAL(10, 2) NOT NULL,
        status VARCHAR(50) NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customer_info(customer_id)
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INT NOT NULL,
        pizza_id INT NOT NULL,
        quantity INT NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders_info(order_id),
        FOREIGN KEY (pizza_id) REFERENCES pizza_info(pizza_id)
    )''')
    
    conn.commit()
    cursor.close()
    conn.close()

def insertion_operation(query):
    try:
        conn=sqlite3.connect("pizza_db.db")
        cursor=conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()
        return "operation successfull"
    except Exception as e:
        return str(e)
    
def reading_operation(query):
    try:
        conn=sqlite3.connect("pizza_db.db")
        cursor=conn.cursor()
        cursor.execute(query)
        existing_data=cursor.fetchall()
        print(existing_data)
        conn.close()
        return existing_data
    except Exception as e:
        return str(e)

# def delete_data(query):
#     print(f"query in delete : {query} ")
#     if query.startswith("DELETE"):
#         return "Delete Operation is not alloweed"

def check_calling(status,query):
    if status == "read":
        return reading_operation(query)
    # elif status== "delete":
    #     return delete_data(query)

    else:
        return insertion_operation(query)


# make_db()

# insertion_operation('''INSERT INTO customer_info (name, phone_number, address) VALUES ('ismail', '03329052129', 'g9 islamabad')''')

































































# make_db()

# data=[
# ('Pepperoni', 'Delicious pizza topped with pepperoni slices and mozzarella cheese.', 950),
# ('BBQ Chicken', 'Pizza with BBQ sauce, grilled chicken, red onions, and cilantro.', 1100),
# ('Hawaiian', 'A unique pizza with ham, pineapple, and mozzarella cheese.', 900),
# ('Veggie Delight', 'Loaded with bell peppers, onions, mushrooms, olives, and mozzarella.', 850),
# ('Four Cheese', 'A rich blend of mozzarella, cheddar, parmesan, and gorgonzola cheeses.', 1200),
# ('Meat Lovers', 'Topped with pepperoni, sausage, ham, bacon, and mozzarella cheese.', 1300),
# ('Buffalo Chicken', 'Spicy buffalo chicken, red onions, and mozzarella, drizzled with ranch.', 1150),
# ('Supreme', 'Pepperoni, sausage, bell peppers, onions, mushrooms, and olives.', 1250),
# ('Spinach & Feta', 'Fresh spinach, feta cheese, red onions, and mozzarella.', 950),
# ('Pesto Chicken', 'Pesto sauce, grilled chicken, sun-dried tomatoes, and mozzarella.', 1100),
# ('Mexican Fiesta', 'Spicy tomato sauce, jalapeños, ground beef, onions, and cheddar cheese.', 1050),
# ('White Pizza', 'Creamy Alfredo sauce, mozzarella, ricotta, and garlic.', 950),
# ('Mushroom Lover', 'Loaded with mushrooms, garlic, and mozzarella cheese.', 900),
# ('Tandoori Chicken', 'Tandoori marinated chicken, onions, bell peppers, and mozzarella.', 1150),
# ('Seafood Special', 'Shrimp, calamari, garlic, and mozzarella on a tomato base.', 1400),
# ('Prosciutto Arugula', 'Prosciutto, fresh arugula, parmesan, and mozzarella.', 1200),
# ('Capricciosa', 'Ham, mushrooms, artichokes, olives, and mozzarella.', 1050),
# ('Mediterranean', 'Feta cheese, olives, tomatoes, red onions, and mozzarella.', 950),
# ('Truffle Mushroom', 'Truffle oil, wild mushrooms, and mozzarella.', 1500)]


# def insertINfo():
#     conn=sqlite3.connect("pizza_db.db")
#     cursor=conn.cursor()
#     for i in data:
#         cursor.execute('''INSERT INTO pizza_info (name, description, price) VALUES (?, ?, ?)''',i)
#     conn.commit()
#     cursor.close()
#     conn.close()
# insertINfo()


#  cursor.execute('''INSERT INTO chat (user_id,question,answer) VALUES (?, ?, ?)''',(userid,question,answer,))