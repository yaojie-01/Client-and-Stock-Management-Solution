

from datetime import datetime


def display_menu():
    
    print("=" * 63)
    print("💼 Welcome to KLCC Customer and Inventory Management System 💼")
    print("=" * 63)
    print("\nPlease choose an option:")
    print("1️⃣  Register")
    print("2️⃣  Login")
    print("3️⃣  Exit")
    print("\n" + "=" * 63)


def generate_order_id(orders):
    
    order_count = len(orders) + 1
    return f"ORD{order_count:03d}"

def generate_inventory_id(inventory):
    
    inventory_count = len(inventory) + 1
    return f"INV{inventory_count:03d}"



def is_strong_password(password, settings):
    
    if len(password) < settings["MIN_PASSWORD_LENGTH"]:
        return False

    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False
    special_characters = "!@#$%^&*()-+"

    
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in special_characters:
            has_special = True

    return has_upper and has_lower and has_digit and has_special


def register_user(users, username, password, settings):
    
    
    if not username or not password:
        print("❌ Invalid input: All fields are required.")
        return

    if not is_strong_password(password, settings):
        print("❌ Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, a digit, and a special character.")
        return

    user_type = ""
    
    while user_type not in ["admin", "customer", "inventory"]:
        user_type = input("Enter user type (admin/customer/inventory): ").strip().lower()
        if user_type not in ["admin", "customer", "inventory"]:
            print("⚠️ Invalid user type. Please enter 'admin', 'customer', or 'inventory'.")

    status = settings["STATUS_PENDING"]
    
    phone_number = input("Enter phone number (or leave blank if not applicable): ").strip()
    
    registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    users.append([username, password, user_type, status, phone_number, registration_date])

    save_users(users, settings)

    print(f"✅ User {username} registered successfully!")


def login(users, username, password, settings):
    

    print("\n" + "="*50)
    print("🔑 User Login".center(50))
    print("="*50)

    for user in users:
        if user[0] == username and user[1] == password:
            if user[3] == settings["STATUS_APPROVED"]:
                print(f"\n🎉 Welcome, {username}! You are successfully logged in.")
                return user
            else:
                print(f"❌ User {username} is not approved yet.")
                return None

    print("❌ Invalid username or password. Please try again.")
    return None



def load_users(settings):
    
    users = []
    try:
        with open(settings["USERS_FILE"], "r") as file:
            for line in file:
                
                users.append(line.strip().split(","))
    except FileNotFoundError:
        print(f"File {settings['USERS_FILE']} not found. Starting with an empty user list.")

    
    found = False

    for user in users:
        if user[0] == settings["DEFAULT_SUPER_USER"][0]:
            found = True
            break

    
    if not found:
        users.append(list(settings["DEFAULT_SUPER_USER"]))

    return users

def save_users(users, settings):
    
    with open(settings["USERS_FILE"], "w") as file:
        for user in users:
            file.write(",".join(user) + "\n")


def load_orders(settings):
    
    orders = []
    try:
        with open(settings["ORDERS_FILE"], "r") as file:
            for line in file:
                orders.append(eval(line.strip()))
    except FileNotFoundError:
        print(f"File {settings['ORDERS_FILE']} not found. Starting with an empty orders list.")
    except SyntaxError:
        print("Error in file format. Starting with an empty orders list.")
    return orders

def save_orders(orders, settings):
    
    with open(settings["ORDERS_FILE"], "w") as file:
        for order in orders:
            file.write(str(order) + "\n")

def load_inventory(settings):
    
    inventory = []
    try:
        with open(settings["INVENTORY_FILE"], "r") as file:
            for line in file:
                inventory.append(eval(line.strip()))
    except FileNotFoundError:
        print(f"File {settings['INVENTORY_FILE']} not found. Starting with an empty inventory list.")
    except SyntaxError:
        print("Error in file format. Starting with an empty inventory list.")
    return inventory

def save_inventory(inventory, settings):
    
    with open(settings["INVENTORY_FILE"], "w") as file:
        for item in inventory:
            file.write(str(item) + "\n")

def load_prices(settings):
    
    prices = {}
    try:
        with open(settings["PRICES_FILE"], "r") as file:
            for line in file:
                item, price = line.strip().split(',')
                prices[item] = float(price)
    except FileNotFoundError:
        print(f"File {settings['PRICES_FILE']} not found. Starting with an empty price list.")
    except ValueError:
        print("Error in file format. Starting with an empty price list.")
    return prices

def save_prices(prices, settings):
    
    with open(settings["PRICES_FILE"], "w") as file:
        for item, price in prices.items():
            file.write(f"{item},{price}\n")

def load_stock(settings):
    
    stock = {}
    try:
        with open(settings["STOCK_FILE"], "r") as file:
            for line in file:
                item, quantity = line.strip().split(',')
                stock[item] = int(quantity)
    except FileNotFoundError:
        print(f"File {settings['STOCK_FILE']} not found. Starting with an empty stock list.")
    except ValueError:
        print("Error in file format. Starting with an empty stock list.")
    return stock

def save_stock(stock, settings):
    
    with open(settings["STOCK_FILE"], "w") as file:
        for item, quantity in stock.items():
            file.write(f"{item},{quantity}\n")



def add_user(users, settings):
    """Add User"""
    print("\n" + "="*50)
    print("👤 Add New User".center(50))
    print("="*50)

    username = input("Enter username: ")
    password = input("Enter password: ")

    while not is_strong_password(password, settings):
        print("❌ Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, a digit, and a special character.")
        password = input("Enter password: ")

    user_type = ""
    while user_type not in ["admin", "customer", "inventory"]:
        user_type = input("Enter user type (admin/customer/inventory): ").strip().lower()
        if user_type not in ["admin", "customer", "inventory"]:
            print("⚠️ Invalid user type. Please enter 'admin', 'customer', or 'inventory'.")

    phone_number = input("Enter phone number (or leave blank if not applicable): ").strip()
    status = settings["STATUS_PENDING"] if user_type == "customer" else settings["STATUS_APPROVED"]
    registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    users.append([username, password, user_type, status, phone_number, registration_date])
    save_users(users, settings)
    print(f"✅ User {username} added successfully!")


def verify_users(users, settings):
    print("\n" + "="*50)
    print("🔍 Verify Users".center(50))
    print("="*50)

    all_users_verified = True

    for user in users:
        if user[3] == settings["STATUS_PENDING"]:
            print(f"Username: {user[0]}, Role: {user[2]}")
            all_users_verified = False

    if all_users_verified:
        print("✅ All users have already been verified!")
    else:
        username = input("Select username to verify: ")
        for user in users:
            if user[0] == username:
                if user[3] == settings["STATUS_PENDING"]:
                    user[3] = settings["STATUS_APPROVED"]
                    print(f"✅ User {user[0]} verified successfully!")
                elif user[3] == settings["STATUS_APPROVED"]:
                    print(f"🔄 User {user[0]} has already been verified.")
                break
        else:
            print("❌ Invalid input or user not found.")

        save_users(users, settings)

def verify_all_users(users, settings):
    print("\n" + "="*50)
    print("✅ Verify All Users".center(50))
    print("="*50)

    all_users_verified = True
    verified_users = []

    for user in users:
        if user[3] == settings["STATUS_PENDING"]:
            user[3] = settings["STATUS_APPROVED"]
            verified_users.append(user[0])  # Collect verified user names
            all_users_verified = False

    if all_users_verified:
        print("✅ All users have been verified.")
    else:
        print("Verified Users:")
        for username in verified_users:
            print(f"✔️ {username} has been verified successfully!")

    save_users(users, settings)

def modify_user_details(users, settings):
    
    print("\n" + "="*50)
    print("✏️ Modify User Details".center(50))
    print("="*50)

    print("🔍 Available Users:")
    for user in users:
        print(f"👤 {user[0]}")

    
    username = input("Enter username to modify: ")
    for user in users:
        if user[0] == username:
            new_password = input("Enter new password: ")
            while not is_strong_password(new_password, settings):
                print("❌ Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, a digit, and a special character.")
                new_password = input("Enter new password: ")
            user[1] = new_password
            print(f"✅ User {username} details modified successfully!")
            save_users(users, settings)
            return
    print("❌ User not found.")


def disable_user_access(users, settings):
    
    print("\n" + "="*50)
    print("🚫 Disable/Enable User Access".center(50))
    print("="*50)

    action = input("Would you like to:\n1. 🚫 Disable user access\n2. 🔄 Re-enable user access\nEnter choice: ").strip()

    if action == '1':
        
        print("🔍 Available Users:")
        for user in users:
            print(f"👤 {user[0]}")

        
        username = input("Enter username to disable: ").strip()
        for user in users:
            if user[0] == username:
                user[3] = "disabled"
                print(f"✅ User {username} access disabled successfully!")
                save_users(users, settings)
                return
        print("❌ User not found.")

    elif action == '2':
        
        print("🔍 Disabled Users:")
        disabled_users_found = False
        for user in users:
            if user[3] == "disabled":
                print(f"👤 {user[0]}")
                disabled_users_found = True
        if not disabled_users_found:
            print("✅ No disabled users found.")

        
        username = input("Enter username to re-enable: ").strip()
        for user in users:
            if user[0] == username and user[3] == "disabled":
                user[3] = "active"
                print(f"✅ User {username} access re-enabled successfully!")
                save_users(users, settings)
                return
        print("❌ User not found or user is not disabled.")

    else:
        print("❌ Invalid choice.")


def inquiry_user_system_usage(users):
    
    print("\n" + "="*50)
    print("🔍 Inquiry User System Usage".center(50))
    print("="*50)

    if not users:
        print("📋 No users available.")
        return

    print("🔍 Available Users:")
    for user in users:
        print(f"👤 {user[0]}")

    username = input("Enter username to inquire: ").strip()
    for user in users:
        if user[0] == username:
            print(f"\n📊 User {username} Usage Details:")
            print(f"\n👤 Username: {user[0]}")
            print(f"🔑 Role: {user[2]}")
            print(f"✅ Status: {user[3]}")
            print(f"📞 Phone Number: {user[4]}")
            print(f"📅 Registration Date: {user[5]}")
            print(f"🔒 Password: {user[1]}")
            return

    print("❌ User not found.")


def check_customer_order_status(users, orders):
    
    print("\n" + "="*50)
    print("📦 Check Customer Order Status".center(50))
    print("="*50)

    if not users:
        print("📋 No users available.")
        return

    print("🔍 Available Users:")
    for user in users:
        print(f"👤 {user[0]}")

    username = input("Enter customer username to check order status: ").strip()
    user_orders = [order for order in orders if order["username"] == username]

    if user_orders:
        print(f"\n📦 Orders for {username}:")
        for order in user_orders:
            print(f"\n📝 Order ID: {order['order_id']}")
            print(f"📦 Item: {order['item']}")
            if 'quantity' in order:
                print(f"🔢 Quantity: {order['quantity']}")
            if 'issue' in order:
                print(f"🛠️ Issue: {order['issue']}")
            print(f"✅ Status: {order['status']}")
    else:
        print("❌ No orders found for this user.")


def generate_admin_reports(users, orders, inventory):
    
    print("\n" + "="*50)
    print("📊 Generate Admin Reports".center(50))
    print("="*50)

    has_users = any(users)
    has_orders = any(orders)
    has_inventory = any(inventory)

    report_generated = False

    if has_users:
        report_generated = True
        print("📋 Users Report:")
        for user in users:
            print(f"\n👤 Username: {user[0]}")
            print(f"🔑 Role: {user[2]}")
            print(f"✅ Status: {user[3]}")
            print(f"📞 Phone Number: {user[4]}")
            print(f"📅 Registration Date: {user[5]}")
            print(f"🔒 Password: {user[1]}")
        print("\n" + "="*50)

    if has_orders:
        report_generated = True
        print("📋 Orders Report:")
        for order in orders:
            print(f"\n📝 Order ID: {order['order_id']}")
            print(f"📦 Item: {order['item']}")
            if 'quantity' in order:
                print(f"🔢 Quantity: {order['quantity']}")
            if 'issue' in order:
                print(f"🛠️ Issue: {order['issue']}")
            print(f"✅ Status: {order['status']}")
        print("\n" + "="*50)

    if has_inventory:
        report_generated = True
        print("📋 Inventory Report:")
        for item in inventory:
            print(f"\n🗃️ Inventory ID: {item['inventory_id']}")
            print(f"📦 Item: {item['item']}")
            print(f"🔢 Quantity: {item['quantity']}")
            print(f"✅ Status: {item['status']}")
        print("\n" + "="*50)

    if report_generated:
        print("✅ Reports generated successfully!")




def generate_customer_reports(username, orders):
    """Generate a report of orders for the logged-in user."""
    print("\n" + "="*50)
    print("📊 Generating Orders Report".center(50))
    print("="*50)

    
    user_orders = [order for order in orders if order["username"] == username]

    
    if user_orders:
        print(f"\n📦 **Orders Report for {username}:**")
        for order in user_orders:
            print(f"\n📝 Order ID: {order['order_id']}")
            print(f"📦 Item: {order['item']}")

            
            if 'quantity' in order:
                print(f"🔢 Quantity: {order['quantity']}")

            
            if 'issue' in order:
                print(f"🛠️ Issue: {order['issue']}")

           
            print(f"✅ Status: {order['status']}")

        print("\n✅ Orders report generated successfully!")
    else:
        print("❌ No orders found for this user.")


def place_customer_order(username, orders, stock):
    
    print("\n" + "="*50)
    print("🛒 Place Customer Order".center(50))
    print("="*50)

    order_id = generate_order_id(orders)
    item_input = input("Enter item to order: ").strip().title()  # Capitalize item input

    
    stock_normalized = {k.title(): v for k, v in stock.items()}

    if item_input in stock_normalized:  # Check if item exists in stock
        available_quantity = stock_normalized[item_input]
        quantity = -1
        while quantity <= 0:
            try:
                quantity = int(input("Enter quantity: "))
                if quantity <= 0:
                    print("⚠️  Quantity must be a positive integer.")
                elif quantity > available_quantity:
                    print(f"⚠️  Quantity exceeds available stock. Only {available_quantity} units available.")
                    quantity = -1  # Prompt for input again
                else:
                    break
            except ValueError:
                print("❌ Invalid input. Please enter a valid quantity.")

        if quantity > 0:
            orders.append({
                "order_id": order_id,
                "username": username,
                "item": item_input,
                "quantity": quantity,
                "status": "pending",
                "order_type": "product",
                "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            print(f"✅ Purchase order placed successfully! Your Order ID is {order_id}.")
    else:
        print(f"❌ Item '{item_input}' not found in stock.")



def place_service_repair(username, orders, settings):
    
    print("\n" + "="*50)
    print("🔧 Request Service/Repair".center(50))
    print("="*50)

    order_id = generate_order_id(orders)
    item = input("Enter item for service/repair: ")
    issue = input("Describe the issue: ")
    orders.append({
        "order_id": order_id,
        "username": username,
        "item": item,
        "issue": issue,
        "status": settings["STATUS_PENDING"],
        "order_type": "service",
        "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_orders(orders, settings)
    print(f"✅ Service/Repair order placed successfully! Your Order ID is {order_id}.")


def modify_customer_order(username, orders, settings):
    
    print("\n" + "="*50)
    print("✏️ Modify Customer Order".center(50))
    print("="*50)

    order_id = input("Enter order ID to modify: ")
    for order in orders:
        if order["order_id"] == order_id and order["username"] == username:
            if order["status"] == "completed":
                print("❌ Cannot modify a completed order.")
                return
            new_item = input("Enter new item (leave blank to keep current): ")
            if new_item:
                order["item"] = new_item
            new_quantity = -1
            while new_quantity <= 0:
                try:
                    new_quantity = int(input("Enter new quantity: "))
                    if new_quantity <= 0:
                        print("⚠️  Quantity must be a positive integer.")
                except ValueError:
                    print("❌ Invalid input. Please enter a valid quantity.")
            order["quantity"] = new_quantity
            save_orders(orders, settings)
            print(f"✅ Order {order_id} modified successfully!")
            return
    print("❌ Order not found or you do not have permission to modify it.")

def cancel_customer_order(username, orders, settings):
    
    print("\n" + "="*50)
    print("❌ Cancel Customer Order".center(50))
    print("="*50)

    order_id = input("Enter order ID to cancel: ")
    for order in orders:
        if order["order_id"] == order_id and order["username"] == username:
            if order["status"] == "completed":
                print("❌ Cannot cancel a completed order.")
                return
            orders.remove(order)
            save_orders(orders, settings)
            print(f"✅ Order {order_id} cancelled successfully!")
            return
    print("❌ Order not found or you do not have permission to cancel it.")


def make_customer_payment(username, orders, stock, prices, settings):
    
    print("\n" + "="*50)
    print("💳 Make Customer Payment".center(50))
    print("="*50)

    order_id = input("Enter order ID to make payment: ").strip()

    for order in orders:
        if order["order_id"] == order_id and order["username"] == username:
            if order["status"] == "completed":
                print("❌ Payment already completed for this order.")
                return

            item_name = order["item"]
            order_type = order["order_type"]

            if order_type == "product":
                if item_name not in prices:
                    print(f"❌ Item '{item_name}' not found in price list.")
                    return

                expected_total = prices[item_name] * order["quantity"]
            elif order_type == "service":
                expected_total = 100  # Fixed price for service/repair
            else:
                print("❌ Unknown order type.")
                return

            amount = -1
            while amount <= 0:
                try:
                    amount = float(input(f"Enter payment amount (Expected RM{expected_total:.2f}): "))
                    if amount <= 0:
                        print("⚠️  Amount must be a positive number.")
                    elif amount != expected_total:
                        print(f"⚠️  Amount does not match the expected total of RM{expected_total:.2f}.")
                        amount = -1
                except ValueError:
                    print("❌ Invalid input. Please enter a valid amount.")

            order["status"] = "completed"
            save_orders(orders, settings)

            
            if order_type == "product":
                if item_name in stock:
                    stock[item_name] -= order["quantity"]
                    if stock[item_name] < 0:
                        print(f"⚠️  Warning: Stock for item '{item_name}' is insufficient.")
                        stock[item_name] += order["quantity"]
                        return
                    print(f"📉 Stock updated. {item_name} quantity is now {stock[item_name]}.")
                    save_stock(stock, settings)
                else:
                    print(f"❌ {item_name} not found in stock.")

            print(f"✅ Payment for order {order_id} completed successfully!")
            return

    print("❌ Order not found or does not belong to the user.")


def inquiry_order_status(username, orders):
    
    print("\n" + "="*50)
    print("🔍 Inquiry Order Status".center(50))
    print("="*50)

    try:
        order_id = input("Enter order ID to inquire: ")
    except ValueError:
        print("❌ Invalid input. Please enter a valid order ID.")
        return

    for order in orders:
        if order["order_id"] == order_id and order["username"] == username:
            print(f"Order {order_id} status: {order['status']}")
            return
    print("❌ Order not found or you do not have permission to inquire about it.")



def place_inventory_order(inventory, prices, settings):
    """Place a new inventory order to replenish stock."""
    print("\n" + "="*50)
    print("📦 Place Inventory Order".center(50))
    print("="*50)

    inventory_id = generate_inventory_id(inventory)
    item_input = input("Enter item to order: ").strip().title()  # Capitalize item input

    
    item = None
    for key in prices:
        if key.title() == item_input:
            item = key
            break

    if item is None:
        print(f"❌ Item '{item_input}' not found in price list.")
        return

    quantity = -1
    while quantity <= 0:
        try:
            quantity = int(input("Enter quantity: "))
            if quantity <= 0:
                print("⚠️ Quantity must be a positive integer.")
        except ValueError:
            print("❌ Invalid input. Please enter a valid quantity.")

    unit_price = prices[item]
    total = unit_price * quantity
    inventory.append({"inventory_id": inventory_id, "item": item, "quantity": quantity, "status": "pending"})

    print(f'✅ Purchase order placed successfully! Your Inventory ID is {inventory_id}.')
    print(f'📝 Your order for item "{item}" with a quantity of {quantity} and a unit price of RM{unit_price} has been recorded.')
    print(f"\n💰 Based on your order, the total cost is RM{total}")

    
    save_inventory(inventory, settings)

def check_stock(stock):
    print("\n" + "="*50)
    print("📊 Available Stocks".center(50))
    print("="*50)
    for item, quantity in stock.items():
        print(f"{item}: {quantity}")

def check_purchase_order_status(inventory):
    
    print("\n" + "="*50)
    print("📋 Purchase Order Statuses".center(50))
    print("="*50)

    if not inventory:
        print("❌ No purchase orders found.")
        return

    print("📦 Purchase Orders Report:")
    for order in inventory:
        print(f"\n📝 Inventory ID: {order['inventory_id']}")
        print(f"📦 Item: {order['item']}")
        print(f"🔢 Quantity: {order['quantity']}")
        print(f"✅ Status: {order['status']}")

    print("✅ Purchase order statuses displayed successfully!")


def modify_inventory_order(inventory, prices, settings):
    
    print("\n" + "="*50)
    print("✏️ Modify Inventory Order".center(50))
    print("="*50)

    inventory_id = input("Enter inventory ID to modify: ")
    for order in inventory:
        if order["inventory_id"] == inventory_id:
            if order["status"] == "completed":
                print("❌ Cannot modify a completed order.")
                return
            new_item = input("Enter new item (leave blank to keep current): ")
            if new_item:
                if new_item in prices:
                    order["item"] = new_item
                else:
                    print("❌ Item not found in price list.")
                    return
            new_quantity = -1
            while new_quantity <= 0:
                try:
                    new_quantity = int(input("Enter new quantity: "))
                    if new_quantity <= 0:
                        print("⚠️ Quantity must be a positive integer.")
                except ValueError:
                    print("❌ Invalid input. Please enter a valid quantity.")
            order["quantity"] = new_quantity
            order["status"] = "pending"
            save_inventory(inventory, settings)
            print(f"✅ Inventory order {inventory_id} modified successfully!")
            return
    print("❌ Inventory order not found.")

def cancel_inventory_order(inventory, settings):
    
    print("\n" + "="*50)
    print("❌ Cancel Inventory Order".center(50))
    print("="*50)

    inventory_id = input("Enter inventory ID to cancel: ")
    for order in inventory:
        if order["inventory_id"] == inventory_id:
            if order["status"] == "completed":
                print("❌ Cannot cancel a completed order.")
                return
            inventory.remove(order)
            save_inventory(inventory, settings)
            print(f"✅ Inventory order {inventory_id} cancelled successfully!")
            return
    print("❌ Inventory order not found.")

def make_inventory_payment(inventory, stock, prices, settings):
    
    print("\n" + "="*50)
    print("💳 Make Inventory Payment".center(50))
    print("="*50)

    inventory_id = input("Enter inventory ID to make payment: ").strip()

    
    order_found = False

    for order in inventory:
        if order["inventory_id"] == inventory_id:
            order_found = True

            if order["status"] == "completed":
                print("❌ Payment already completed for this inventory order.")
                return

            
            item_name = order.get("item")
            if item_name is None:
                print("❌ Error: Item name is missing in the order.")
                return

            if item_name not in prices:
                print(f"❌ Item '{item_name}' not found in price list.")
                return

            expected_total = prices[item_name] * order["quantity"]
            amount = -1
            while amount <= 0:
                try:
                    amount = float(input(f"Enter payment amount (Expected RM{expected_total:.2f}): "))
                    if amount <= 0:
                        print("⚠️  Amount must be a positive number.")
                    elif amount != expected_total:
                        print(f"⚠️  Amount does not match the expected total of RM{expected_total:.2f}.")
                        amount = -1
                except ValueError:
                    print("❌ Invalid input. Please enter a valid amount.")

            order["status"] = "completed"
            save_inventory(inventory, settings)

            # Update stock
            if item_name in stock:
                stock[item_name] += order["quantity"]
                print(f"📈 Stock updated. {item_name} quantity is now {stock[item_name]}.")
                save_stock(stock, settings)
            else:
                print(f"❌ {item_name} not found in stock.")

            print(f"✅ Payment for inventory order {inventory_id} completed successfully!")
            return

    if not order_found:
        print(f"❌ Inventory order with ID {inventory_id} not found.")


def generate_inventory_reports(inventory):
   
    print("\n" + "="*50)
    print("📄 Detailed Inventory Report".center(50))
    print("="*50)

    if not inventory:
        print("❌ No inventory orders to report.")
        return

    
    print("ID       | Item        | Quantity | Status  | Date                ")
    print("-" * 60)

    for order in inventory:
        
        print(f"{order['inventory_id']:7} | {order['item']:10} | {order['quantity']:8} | {order['status']:7} | {order.get('order_date', 'N/A')}")


def super_user_menu(users, orders, inventory, settings):
    
    while True:
        print("\n" + "="*50)
        print("🔧 Super User Menu".center(50))
        print("="*50)

        print("1. 🆕 Add User")
        print("2. ✔️ Verify New Customers")
        print("3. ✏️ Modify User Details")
        print("4. 🚫 Disable/Reenable User Access")
        print("5. 🔍 Inquiry User System Usage")
        print("6. 📦 Check Customer Order Status")
        print("7. 📊 Reports")
        print("8. 🔒 Logout")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_user(users, settings)
        elif choice == "2":
            verify_menu(users, settings)
        elif choice == "3":
            modify_user_details(users, settings)
        elif choice == "4":
            disable_user_access(users, settings)
        elif choice == "5":
            inquiry_user_system_usage(users)
        elif choice == "6":
            check_customer_order_status(users, orders)
        elif choice == "7":
            generate_admin_reports(users, orders, inventory)
        elif choice == "8":
            print("🔓 Logging out...")
            break
        else:
            print("❌ Invalid choice.")



def admin_menu(users, orders, inventory, settings):
    
    while True:
        print("\n" + "="*40)
        print("🛠️ Admin Menu".center(40))
        print("="*40)

        print("1. ✔️ Verify New Customers")
        print("2. 📦 Check Customer Order Status")
        print("3. 📊 Reports")
        print("4. 🔒 Logout")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            verify_menu(users, settings)
        elif choice == "2":
            check_customer_order_status(users, orders)
        elif choice == "3":
            generate_admin_reports(users, orders, inventory)
        elif choice == "4":
            print("🔓 Logging out...")
            break
        else:
            print("❌ Invalid choice.")




def verify_menu(users, settings):
    
    while True:
        print("\n" + "="*40)
        print("🔍 Verify Menu".center(40))
        print("="*40)

        print("1. ✅ Verify User")
        print("2. ✅ Verify All Users")
        print("3. 🔙 Back")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            verify_users(users, settings)
        elif choice == "2":
            verify_all_users(users, settings)
        elif choice == "3":
            print("🔙 Returning to the previous menu...")
            break
        else:
            print("❌ Invalid choice.")



def customer_menu(users, username, orders, inventory, stock, prices, settings):

    while True:
        
        print("\n" + "="*40)
        print("👤 Customer Menu".center(40))
        print("="*40)

        print("1. 🛒 Purchase Order")
        print("2. 🔧 Request Service/Repair")
        print("3. 📊 Reports")
        print("4. 🔒 Logout")

        choice = input("Enter choice: ").strip()

        
        if choice == "1":
            purchase_order_menu(username, orders, stock, prices, settings)
        elif choice == "2":
            repair_order_menu(username, orders, stock, prices, settings) 
        elif choice == "3":
            generate_customer_reports(username, orders) 
        elif choice == "4":
            print("🔒 Logging out...")
            break 
        else:
            print("❌ Invalid choice.")





def purchase_order_menu(username, orders, stock, prices, settings):
    
    while True:
        print("\n" + "="*40)
        print("🛒 Purchase Order Menu".center(40))
        print("="*40)

        print("1. 📦 Place Purchase Order")
        print("2. ✏️ Modify Order")
        print("3. ❌ Cancel Order")
        print("4. 💳 Make Payment")
        print("5. 📋 Inquiry Order Status")
        print("6. 🔙 Back")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            place_customer_order(username, orders, stock)
        elif choice == "2":
            modify_customer_order(username, orders, settings)
        elif choice == "3":
            cancel_customer_order(username, orders, settings)
        elif choice == "4":
            make_customer_payment(username, orders, stock, prices, settings)
        elif choice == "5":
            inquiry_order_status(username, orders)
        elif choice == "6":
            print("🔙 Returning to previous menu...")
            break
        else:
            print("❌ Invalid choice.")



def repair_order_menu(username, orders, stock, prices, settings):
    
    while True:
        print("\n" + "="*40)
        print("🔧 Repair/Service Order Menu".center(40))
        print("="*40)

        print("1. 🔨 Place Repair/Service Order")
        print("2. ✏️ Modify Order")
        print("3. ❌ Cancel Order")
        print("4. 💳 Make Payment")
        print("5. 📋 Inquiry Order Status")
        print("6. 🔙 Back")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            place_service_repair(username, orders, settings)
        elif choice == "2":
            modify_customer_order(username, orders, settings)
        elif choice == "3":
            cancel_customer_order(username, orders, settings)
        elif choice == "4":
            make_customer_payment(username, orders, stock, prices, settings)
        elif choice == "5":
            inquiry_order_status(username, orders)
        elif choice == "6":
            print("🔙 Returning to previous menu...")
            break
        else:
            print("❌ Invalid choice.")



def inventory_menu(inventory, stock, prices, settings):
    
    while True:
        print("\n" + "="*40)
        print("📦 Inventory Menu".center(40))
        print("="*40)

        print("1. 🛒 Purchase Order")
        print("2. 📊 Stock Check/Adjustment")
        print("3. 📋 Check Purchase Order Status")
        print("4. ✏️ Modify Purchase Order")
        print("5. ❌ Cancel Purchase Order")
        print("6. 💳 Make Payment")
        print("7. 📈 Reports")
        print("8. 🚪 Logout")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            place_inventory_order(inventory, prices, settings)
        elif choice == "2":
            check_stock(stock)
        elif choice == "3":
            check_purchase_order_status(inventory)
        elif choice == "4":
            modify_inventory_order(inventory, prices, settings)
        elif choice == "5":
            cancel_inventory_order(inventory, settings)
        elif choice == "6":
            make_inventory_payment(inventory, stock, prices, settings)
        elif choice == "7":
            generate_inventory_reports(inventory)
        elif choice == "8":
            print("🚪 Logged out successfully.")
            break
        else:
            print("❌ Invalid choice. Please try again.")



def main():

    
    settings = {
    "USERS_FILE": "users.txt",
    "ORDERS_FILE": "orders.txt",
    "INVENTORY_FILE": "inventory.txt",
    "PRICES_FILE": "prices.txt",
    "STOCK_FILE": "stock.txt",
    "STATUS_PENDING": "pending",
    "STATUS_APPROVED": "approved",
    "DEFAULT_SUPER_USER": ("super user", "Super123!", "super user", "approved", "123-456-7890", "N/A"),
    "MIN_PASSWORD_LENGTH": 8,
    }

    
    users = []
    orders = []
    inventory = []
    prices = {}
    stock = {}

    
    users = load_users(settings)
    orders = load_orders(settings)
    inventory = load_inventory(settings)
    prices = load_prices(settings)
    stock = load_stock(settings)
    save_users(users, settings)

    
    while True:
        display_menu()
        choice = input("🔍 Enter your choice: ")

        
        if choice == "1":
            print("\n" + "="*50)
            print("🔑 Register".center(50))
            print("="*50)
            username = input("Enter username: ")
            password = input("Enter password: ")
            register_user(users, username, password, settings)

        
        elif choice == "2":
            print("\n" + "="*50)
            print("🔑 Login".center(50))
            print("="*50)
            username = input("Enter username: ")
            password = input("Enter password: ")
            user = login(users, username, password, settings)
            if user:
                role = user[2]
                
                # Based on the user's role, direct them to the appropriate menu
                if role == "admin":
                    admin_menu(users, orders, inventory, settings)
                elif role == "customer":
                    customer_menu(users, username, orders, inventory, stock, prices, settings)
                elif role == "inventory":
                    inventory_menu(inventory, stock, prices, settings)
                elif role == "super user":
                    super_user_menu(users, orders, inventory, settings)
                else:
                    print("🔒 Unrecognized role. Access denied.")
            else:
                print("❌ Login failed. ")

        
        elif choice == "3":
            print("\n🚪 Exiting the system. Goodbye!")
            save_users(users, settings)
            save_orders(orders, settings)
            save_inventory(inventory, settings)
            save_prices(prices, settings)
            save_stock(stock, settings)
            break  # Exit the while loop

        else:
            print("⚠️  Invalid choice.")


if __name__ == "__main__":
    main()

