import datetime
import hashlib
import math
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from google.cloud import datastore

datastore_client = datastore.Client()
app = Flask(__name__, static_url_path='/static')
app.secret_key = os.urandom(24)

# DATASTORE FUNCTIONS
def store_user(username, email, password_hash, reputation=0, role="User"):
    entity = datastore.Entity(key=datastore_client.key("User"))
    entity.update({
        "username": username,
        "email": email,
        "password_hash": password_hash,
        "reputation": reputation,
        "role": role,
        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc)
    })
    datastore_client.put(entity)
    return entity.key.id


def store_item(name, tags, brand):
    entity = datastore.Entity(key=datastore_client.key("Item"))
    entity.update({
        "name": name,
        "tags": tags,
        "brand": brand,
        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc)
    })
    datastore_client.put(entity)
    return entity.key.id


def store_store_info(name, location):
    entity = datastore.Entity(key=datastore_client.key("Store"))
    entity.update({
        "name": name,
        "location": location,
        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc)
    })
    datastore_client.put(entity)
    return entity.key.id



def store_price(item_id, store_id, price, user_id, sale_status):
    entity = datastore.Entity(key=datastore_client.key("Price"))
    entity.update({
        "item_id": item_id,
        "store_id": store_id,
        "price": price,
        "user_id": user_id,
        "sale_status": sale_status,
        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc)
    })
    datastore_client.put(entity)
    return entity.key.id


def store_shoppinglist(user_id, items):
    entity = datastore.Entity(key=datastore_client.key("ShoppingList"))
    entity.update({
        "user_id": user_id,
        "items": items,
        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc)
    })
    datastore_client.put(entity)
    return entity.key.id_or_name


def store_activitylog(user_id, activity_type, details):
    entity = datastore.Entity(key=datastore_client.key("ActivityLog"))
    entity.update({
        "user_id": user_id,
        "activity_type": activity_type,
        "details": details,
        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc)
    })
    datastore_client.put(entity)
    return entity.key.id


def store_tag(name):
    entity = datastore.Entity(key=datastore_client.key("Tag"))
    entity.update({
        "name": name,
        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc)
    })
    datastore_client.put(entity)
    return entity.key.id


def store_comment(user_id, item_id, comment, rating):
    entity = datastore.Entity(key=datastore_client.key("Comment"))
    entity.update({
        "user_id": user_id,
        "item_id": item_id,
        "comment": comment,
        "rating": rating,
        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc)
    })
    datastore_client.put(entity)
    return entity.key.id


# USER FUNCTIONS
def get_user_by_id(user_id):
    key = datastore_client.key("User", user_id)
    user = datastore_client.get(key)
    if user:
        user["id"] = user.key.id
        return user
    return None


def get_user_by_email(email):
    query = datastore_client.query(kind="User")
    query.add_filter("email", "=", email)
    result = list(query.fetch())
    if result:
        user = result[0]
        user["id"] = user.key.id
        return user
    return None


def update_user_info(user_id, updated_data):
    key = datastore_client.key("User", user_id)
    user = datastore_client.get(key)
    if user:
        for k, value in updated_data.items():
            user[k] = value
        datastore_client.put(user)
        return user
    return None


def delete_user(user_id):
    key = datastore_client.key("User", user_id)
    user = datastore_client.get(key)
    if user:
        datastore_client.delete(user.key)
        return True
    return False


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# REPUTATION & RANKING FUNCTIONS
def update_user_reputation(user_id, points):
    user = get_user_by_id(user_id)
    if user:
        user["reputation"] += points
        datastore_client.put(user)
        return user
    return None


def get_user_rankings():
    query = datastore_client.query(kind="User")
    query.order = ["-reputation"]
    result = list(query.fetch())
    rankings = [{"username": user["username"], "reputation": user["reputation"]} for user in result]
    return rankings

# ITEM FUNCTIONS
def get_item_by_id(item_id):
    key = datastore_client.key("Item", int(item_id))
    item = datastore_client.get(key)
    if item:
        return item
    return None

def get_item_by_name(name):
    query = datastore_client.query(kind="Item")
    query.add_filter("name", "=", name)
    result = list(query.fetch())
    if result:
        item = result[0]
        item["id"] = item.key.id
        return item
    return None


def update_item_info(item_id, updated_data):
    key = datastore_client.key("Item", item_id)
    item = datastore_client.get(key)
    if item:
        for k, value in updated_data.items():
            item[k] = value
        datastore_client.put(item)
        return item
    return None


def delete_item(item_id):
    key = datastore_client.key("Item", item_id)
    item = datastore_client.get(key)
    if item:
        datastore_client.delete(item.key)
        return True
    return False


# STORE FUNCTIONS
def get_store_by_id(store_id):
    key = datastore_client.key("Store", store_id)
    store = datastore_client.get(key)
    if store:
        store["id"] = store.key.id
        return store
    return None


def get_store_by_name(name):
    query = datastore_client.query(kind="Store")
    query.add_filter("name", "=", name)
    result = list(query.fetch())
    if result:
        store = result[0]
        store["id"] = store.key.id
        return store
    return None


def update_store_info(store_id, updated_data):
    key = datastore_client.key("Store", store_id)
    store = datastore_client.get(key)
    if store:
        for k, value in updated_data.items():
            if k in ["name", "location"]:
                store[k] = value
        datastore_client.put(store)
        return store
    return None



def delete_store(store_id):
    key = datastore_client.key("Store", store_id)
    store = datastore_client.get(key)
    if store:
        datastore_client.delete(store.key)
        return True
    return False


# SHOPPING LIST FUNCTIONS
def get_shoppinglist_by_user(user_id):
    query = datastore_client.query(kind="ShoppingList")
    query.add_filter("user_id", "=", user_id)
    result = list(query.fetch())
    if result:
        shopping_list = result[0]
        shopping_list["id"] = shopping_list.key.id
        return shopping_list
    return None


def update_shoppinglist(user_id, updated_items):
    shopping_list = get_shoppinglist_by_user(user_id)
    if shopping_list:
        shopping_list = shopping_list[0]
        shopping_list["items"] = updated_items
        datastore_client.put(shopping_list)
        return shopping_list
    return None


def delete_shoppinglist(user_id):
    shopping_list = get_shoppinglist_by_user(user_id)
    if shopping_list:
        datastore_client.delete(shopping_list[0].key)
        return True
    return False

def shoppinglist_remove_item(user_id, item):
    shopping_list = get_shoppinglist_by_user(user_id)
    if shopping_list:
        shopping_list = shopping_list[0]
        if "items" in shopping_list and item in shopping_list["items"]:
            shopping_list["items"].remove(item)
            datastore_client.put(shopping_list)
            return shopping_list
    return None


# PRICE FUNCTIONS
def get_prices_by_item(item_id):
    query = datastore_client.query(kind="Price")
    query.add_filter("item_id", "=", item_id)
    results = list(query.fetch())
    return results


def get_price_comparison(shopping_list):
    comparison = {}
    for item in shopping_list:
        prices = get_prices_by_item(item)
        if prices:
            best_price = min(prices, key=lambda x: x["price"])
            comparison[item] = {
                "store_id": best_price["store_id"],
                "price": best_price["price"],
                "sale_status": best_price["sale_status"],
                "timestamp": best_price["timestamp"]
            }
        else:
            comparison[item] = None
    return comparison


# ACTIVITY LOG FUNCTIONS
def get_activitylog_by_id(log_id):
    key = datastore_client.key("ActivityLog", log_id)
    log = datastore_client.get(key)
    if log:
        log["id"] = log.key.id
        return log
    return None


def get_activitylog_by_user(user_id):
    query = datastore_client.query(kind="ActivityLog")
    query.add_filter("user_id", "=", user_id)
    result = list(query.fetch())
    return result


def update_activitylog_info(log_id, updated_data):
    key = datastore_client.key("ActivityLog", log_id)
    log = datastore_client.get(key)
    if log:
        for k, value in updated_data.items():
            log[k] = value
        datastore_client.put(log)
        return log
    return None


def delete_activitylog(log_id):
    key = datastore_client.key("ActivityLog", log_id)
    log = datastore_client.get(key)
    if log:
        datastore_client.delete(log.key)
        return True
    return False


# TAG FUNCTIONS:
def get_tag_by_id(tag_id):
    key = datastore_client.key("Tag", tag_id)
    tag = datastore_client.get(key)
    if tag:
        tag["id"] = tag.key.id
        return tag
    return None


def get_tag_by_name(name):
    query = datastore_client.query(kind="Tag")
    query.add_filter("name", "=", name)
    result = list(query.fetch())
    if result:
        tag = result[0]
        tag["id"] = tag.key.id
        return tag
    return None


def update_tag_info(tag_id, updated_data):
    key = datastore_client.key("Tag", tag_id)
    tag = datastore_client.get(key)
    if tag:
        for k, value in updated_data.items():
            tag[k] = value
        datastore_client.put(tag)
        return tag
    return None


def delete_tag(tag_id):
    key = datastore_client.key("Tag", tag_id)
    tag = datastore_client.get(key)
    if tag:
        datastore_client.delete(tag.key)
        return True
    return False


def assign_tag_to_item(item_id, tag_id):
    item = get_item_by_id(item_id)
    if item:
        if "tags" not in item:
            item["tags"] = []
        item["tags"].append(tag_id)
        datastore_client.put(item)
        return item
    return None


def assign_tag_to_brand(brand_name, tag_id):
    query = datastore_client.query(kind="Item")
    query.add_filter("brand", "=", brand_name)
    items = list(query.fetch())
    for item in items:
        if "tags" not in item:
            item["tags"] = []
        item["tags"].append(tag_id)
        datastore_client.put(item)
    return items if items else None


# COMMENT FUNCTIONS
def get_comments_by_item(item_id):
    query = datastore_client.query(kind="Comment")
    query.add_filter("item_id", "=", item_id)
    result = list(query.fetch())
    return result


def update_comment_info(comment_id, updated_data):
    key = datastore_client.key("Comment", comment_id)
    comment = datastore_client.get(key)
    if comment:
        for k, value in updated_data.items():
            comment[k] = value
        datastore_client.put(comment)
        return comment
    return None


def delete_comment(comment_id):
    key = datastore_client.key("Comment", comment_id)
    comment = datastore_client.get(key)
    if comment:
        datastore_client.delete(comment.key)
        return True
    return False


# STORE COMPARISON FUNCTIONS
def distance_calculation(lat1, lon1, lat2, lon2):
    radius = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    equation = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(equation), math.sqrt(1 - equation))
    distance = radius * c
    return distance


def get_nearby_stores(user_location, radius=25):
    user_lat, user_lon = user_location
    query = datastore_client.query(kind="Store")
    stores = list(query.fetch())
    nearby_stores = []

    for store in stores:
        store_lat = store["latitude"]
        store_lon = store["longitude"]
        distance = distance_calculation(user_lat, user_lon, store_lat, store_lon)
        if distance <= radius:
            nearby_stores.append(store)

    return nearby_stores


def calculate_best_store(shopping_list, user_location):
    stores = get_nearby_stores(user_location)
    store_totals = {}
    for store in stores:
        store_id = store.key.id
        total_cost = 0
        valid_store = True
        for item_id in shopping_list:
            prices = get_prices_by_item(item_id)
            if not prices:
                valid_store = False
                break
            best_price = min(
                prices,
                key=lambda x: (x['price'], x['sale_status'], -x['timestamp'].timestamp())
            )
            total_cost += best_price['price']
        if valid_store:
            store_totals[store_id] = total_cost
    if not store_totals:
        return None
    best_store_id = min(store_totals, key=store_totals.get)
    best_store = datastore_client.get(datastore_client.key("Store", best_store_id))
    return best_store


# API ENDPOINTS #

# HTML ENDPOINTS
@app.route("/")
def index():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template("index.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/create_user")
def create_user_page():
    return render_template("create_user.html")

@app.route("/create_item")
def create_item_page():
    return render_template("create_item.html")

@app.route("/create_store")
def create_store_page():
    return render_template("create_store.html")

@app.route("/create_shoppinglist")
def create_shoppinglist_page():
    return render_template("create_shoppinglist.html")

@app.route("/recommendation")
def recommendation_page():
    return render_template("recommendation.html")

@app.route('/stores')
def render_stores_page():
    return render_template('stores.html')

@app.route("/shopping_list")
def shopping_list_page():
    return render_template("shopping_list.html")

@app.route("/scan")
def scan_page():
    return render_template("scan.html")

@app.route("/activity")
def activity_page():
    return render_template("activity.html")

@app.route("/user")
def user_page():
    return render_template("user.html")


# USER MANAGEMENT ENDPOINTS
@app.route("/create_user", methods=["POST"])
def create_user_post():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "User")
    reputation = data.get("reputation", 0)
    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    existing_user = get_user_by_email(email)
    if existing_user:
        return jsonify({"error": "User with this email already exists"}), 400

    password_hash = hash_password(password)
    user_id = store_user(username, email, password_hash, reputation=reputation, role=role)
    return jsonify({"message": "User created successfully", "user_id": user_id}), 201

@app.route("/users/<int:user_id>", methods=["GET"])
def read_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        user_info = {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "reputation": user["reputation"],
            "role": user["role"],
            "timestamp": user["timestamp"].isoformat()
        }
        return jsonify(user_info), 200
    return jsonify({"error": "User not found"}), 404


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user_endpoint(user_id):
    if delete_user(user_id):
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"error": "User not found"}), 404


# AUTHENTICATION AND AUTHORIZATION ENDPOINTS
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    user = get_user_by_email(email)
    if user and user["password_hash"] == hash_password(password):
        session['user_id'] = user['id']
        return jsonify({"message": "Login successful"}), 200

    return jsonify({"error": "Invalid email or password"}), 401

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for('login_page'))



# REPUTATION & RANKING ENDPOINTS
@app.route("/users/<int:user_id>/reputation", methods=["PUT"])
def update_reputation(user_id):
    data = request.json
    points = data.get("points")
    if points is None:
        return jsonify({"error": "Missing points"}), 400

    updated_user = update_user_reputation(user_id, points)
    if updated_user:
        return jsonify({"message": "User reputation updated successfully"}), 200
    return jsonify({"error": "User not found"}), 404


@app.route("/users/rankings", methods=["GET"])
def user_rankings():
    rankings = get_user_rankings()
    return jsonify(rankings), 200


@app.route("/users/<int:user_id>/badges", methods=["GET"])
def user_badges(user_id):
    badges = get_user_badges(user_id)
    if badges is not None:
        return jsonify({"badges": badges}), 200
    return jsonify({"error": "User not found"}), 404


# ITEM MANAGEMENT ENDPOINTS
@app.route("/items", methods=["POST"])
def create_item():
    data = request.json
    name = data.get("name")
    tags = data.get("tags", [])
    brand = data.get("brand", "")
    if not name:
        return jsonify({"error": "Missing required fields"}), 400

    existing_item = get_item_by_name(name)
    if existing_item:
        return jsonify({"error": "Item with this name already exists"}), 400

    item_id = store_item(name, tags, brand)
    return jsonify({"message": "Item created successfully", "item_id": item_id}), 201


@app.route("/items/<int:item_id>", methods=["GET"])
def read_item(item_id):
    item = get_item_by_id(item_id)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404


@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.json
    updated_item = update_item_info(item_id, data)
    if updated_item:
        return jsonify({"message": "Item updated successfully"}), 200
    return jsonify({"error": "Item not found"}), 404


@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item_endpoint(item_id):
    if delete_item(item_id):
        return jsonify({"message": "Item deleted successfully"}), 200
    return jsonify({"error": "Item not found"}), 404


# STORE MANAGEMENT ENDPOINTS
@app.route('/api/stores', methods=['POST'])
def create_store():
    data = request.json
    name = data.get("name")
    location = data.get("location")
    if not name or not location:
        return jsonify({"error": "Missing required fields"}), 400

    existing_store = get_store_by_name(name)
    if existing_store:
        return jsonify({"error": "Store with this name already exists"}), 400

    store_id = store_store_info(name, location)
    return jsonify({"message": "Store created successfully", "store_id": store_id}), 201


@app.route("/stores/<int:store_id>", methods=["GET"])
def read_store(store_id):
    store = get_store_by_id(store_id)
    if store:
        return jsonify(store), 200
    return jsonify({"error": "Store not found"}), 404


@app.route("/stores/<int:store_id>", methods=["PUT"])
def update_store(store_id):
    data = request.json
    updated_store = update_store_info(store_id, data)
    if updated_store:
        return jsonify({"message": "Store updated successfully"}), 200
    return jsonify({"error": "Store not found"}), 404


@app.route("/stores/<int:store_id>", methods=["DELETE"])
def delete_store_endpoint(store_id):
    if delete_store(store_id):
        return jsonify({"message": "Store deleted successfully"}), 200
    return jsonify({"error": "Store not found"}), 404


# SHOPPING LIST MANAGEMENT ENDPOINTS
@app.route("/shoppinglist", methods=["POST"])
def create_shoppinglist():
    data = request.json
    user_id = data.get("user_id")
    items = data.get("items", [])
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    shopping_list_id = store_shoppinglist(user_id, items)
    return jsonify({"message": "Shopping list created successfully", "shopping_list_id": shopping_list_id}), 201


@app.route("/shoppinglist/<int:shopping_list_id>", methods=["GET"])
def read_shoppinglist(shopping_list_id):
    shopping_list = datastore_client.get(datastore_client.key("ShoppingList", shopping_list_id))
    if shopping_list:
        shopping_list_info = {
            "user_id": shopping_list["user_id"],
            "items": shopping_list.get("items", []),
            "timestamp": shopping_list["timestamp"].isoformat()
        }
        return jsonify(shopping_list_info), 200
    return jsonify({"error": "Shopping list not found"}), 404


@app.route("/shoppinglist/<int:shopping_list_id>", methods=["PUT"])
def update_shoppinglist_endpoint(shopping_list_id):
    data = request.json
    updated_items = data.get("items")
    if not updated_items:
        return jsonify({"error": "Missing items"}), 400
    shopping_list = datastore_client.get(datastore_client.key("ShoppingList", shopping_list_id))
    if shopping_list:
        shopping_list["items"] = updated_items
        datastore_client.put(shopping_list)
        return jsonify({"message": "Shopping list updated successfully"}), 200
    return jsonify({"error": "Shopping list not found"}), 404


@app.route("/shoppinglist/<int:shopping_list_id>", methods=["DELETE"])
def delete_shoppinglist_endpoint(shopping_list_id):
    key = datastore_client.key("ShoppingList", shopping_list_id)
    shopping_list = datastore_client.get(key)
    if shopping_list:
        datastore_client.delete(key)
        return jsonify({"message": "Shopping list deleted successfully"}), 200
    return jsonify({"error": "Shopping list not found"}), 404


@app.route("/api/shoppinglist", methods=["POST"])
def add_item_to_shoppinglist():
    data = request.json
    user_id = data.get("user_id")
    item_id = data.get("item_id")

    app.logger.info(f"Received add item request: user_id={user_id}, item_id={item_id}")

    if not user_id or not item_id:
        return jsonify({"error": "Missing user_id or item_id"}), 400

    query = datastore_client.query(kind="ShoppingList")
    query.add_filter("user_id", "=", int(user_id))
    result = list(query.fetch())

    if result:
        shopping_list = result[0]
        app.logger.info(f"Shopping list found for user {user_id}: {shopping_list}")
        if "items" not in shopping_list:
            shopping_list["items"] = []
        if int(item_id) not in shopping_list["items"]:
            shopping_list["items"].append(int(item_id))
            datastore_client.put(shopping_list)
            app.logger.info(f"Item {item_id} added to shopping list.")
            return jsonify({"message": "Item added to shopping list"}), 200
        else:
            return jsonify({"error": "Item already in shopping list"}), 400
    else:
        new_shopping_list = datastore.Entity(key=datastore_client.key("ShoppingList"))
        new_shopping_list.update({
            "user_id": int(user_id),
            "items": [int(item_id)],
            "timestamp": datetime.datetime.now(tz=datetime.timezone.utc)
        })
        datastore_client.put(new_shopping_list)
        app.logger.info(f"New shopping list created for user {user_id} with item {item_id}.")
        return jsonify({"message": "Item added to new shopping list"}), 200


# PRICE MANAGEMENT ENDPOINTS
@app.route("/prices", methods=["POST"])
def update_price():
    data = request.json
    item_id = data.get("item_id")
    store_id = data.get("store_id")
    price = data.get("price")
    user_id = data.get("user_id")
    sale_status = data.get("sale_status", False)
    if not item_id or not store_id or not price or not user_id:
        return jsonify({"error": "Missing required fields"}), 400
    price_id = store_price(item_id, store_id, price, user_id, sale_status)
    return jsonify({"message": "Price updated successfully", "price_id": price_id}), 201


@app.route("/prices/<item_id>", methods=["GET"])
def check_prices(item_id):
    prices = get_prices_by_item(item_id)
    if prices:
        return jsonify(prices), 200
    return jsonify({"error": "No prices found for this item"}), 404


@app.route("/prices/compare", methods=["POST"])
def compare_prices():
    data = request.json
    shopping_list = data.get("shopping_list")
    if not shopping_list:
        return jsonify({"error": "Missing shopping list"}), 400
    comparison = get_price_comparison(shopping_list)
    return jsonify(comparison), 200


# ACTIVITY LOG MANAGEMENT ENDPOINTS
@app.route("/activitylogs", methods=["POST"])
def create_activitylog():
    data = request.json
    user_id = data.get("user_id")
    activity_type = data.get("activity_type")
    details = data.get("details")
    if not user_id or not activity_type or not details:
        return jsonify({"error": "Missing required fields"}), 400

    log_id = store_activitylog(user_id, activity_type, details)
    return jsonify({"message": "Activity log created successfully", "log_id": log_id}), 201


@app.route("/activitylogs/<int:log_id>", methods=["GET"])
def read_activitylog(log_id):
    log = get_activitylog_by_id(log_id)
    if log:
        return jsonify(log), 200
    return jsonify({"error": "Activity log not found"}), 404


@app.route("/activitylogs/user/<int:user_id>", methods=["GET"])
def read_activitylog_by_user(user_id):
    logs = get_activitylog_by_user(user_id)
    if logs:
        return jsonify(logs), 200
    return jsonify({"error": "No activity logs found for this user"}), 404


@app.route("/activitylogs/<int:log_id>", methods=["PUT"])
def update_activitylog(log_id):
    data = request.json
    updated_log = update_activitylog_info(log_id, data)
    if updated_log:
        return jsonify({"message": "Activity log updated successfully"}), 200
    return jsonify({"error": "Activity log not found"}), 404


@app.route("/activitylogs/<int:log_id>", methods=["DELETE"])
def delete_activitylog_endpoint(log_id):
    if delete_activitylog(log_id):
        return jsonify({"message": "Activity log deleted successfully"}), 200
    return jsonify({"error": "Activity log not found"}), 404


# TAG MANAGEMENT ENDPOINTS
@app.route("/tags", methods=["POST"])
def create_tag():
    data = request.json
    name = data.get("name")
    if not name:
        return jsonify({"error": "Missing required fields"}), 400

    existing_tag = get_tag_by_name(name)
    if existing_tag:
        return jsonify({"error": "Tag with this name already exists"}), 400

    tag_id = store_tag(name)
    return jsonify({"message": "Tag created successfully", "tag_id": tag_id}), 201


@app.route("/tags/<int:tag_id>", methods=["GET"])
def read_tag(tag_id):
    tag = get_tag_by_id(tag_id)
    if tag:
        return jsonify(tag), 200
    return jsonify({"error": "Tag not found"}), 404


@app.route("/tags/<int:tag_id>", methods=["PUT"])
def update_tag(tag_id):
    data = request.json
    updated_tag = update_tag_info(tag_id, data)
    if updated_tag:
        return jsonify({"message": "Tag updated successfully"}), 200
    return jsonify({"error": "Tag not found"}), 404


@app.route("/tags/<int:tag_id>", methods=["DELETE"])
def delete_tag_endpoint(tag_id):
    if delete_tag(tag_id):
        return jsonify({"message": "Tag deleted successfully"}), 200
    return jsonify({"error": "Tag not found"}), 404


# ASSIGN TAGS TO ITEMS AND BRANDS
@app.route("/items/<int:item_id>/tags", methods=["POST"])
def assign_tag_to_item_endpoint(item_id):
    data = request.json
    tag_id = data.get("tag_id")
    if not tag_id:
        return jsonify({"error": "Missing tag_id"}), 400

    updated_item = assign_tag_to_item(item_id, tag_id)
    if updated_item:
        return jsonify({"message": "Tag assigned to item successfully"}), 200
    return jsonify({"error": "Item not found"}), 404


@app.route("/brands/<string:brand_name>/tags", methods=["POST"])
def assign_tag_to_brand_endpoint(brand_name):
    data = request.json
    tag_id = data.get("tag_id")
    if not tag_id:
        return jsonify({"error": "Missing tag_id"}), 400

    updated_items = assign_tag_to_brand(brand_name, tag_id)
    if updated_items:
        return jsonify({"message": "Tag assigned to brand successfully"}), 200
    return jsonify({"error": "Brand not found"}), 404


# COMMENT MANAGEMENT ENDPOINTS:
@app.route("/comments", methods=["POST"])
def create_comment():
    data = request.json
    user_id = data.get("user_id")
    item_id = data.get("item_id")
    comment = data.get("comment")
    rating = data.get("rating")
    if not user_id or not item_id or not comment or rating is None:
        return jsonify({"error": "Missing required fields"}), 400

    comment_id = store_comment(user_id, item_id, comment, rating)
    return jsonify({"message": "Comment created successfully", "comment_id": comment_id}), 201


@app.route("/comments/<int:item_id>", methods=["GET"])
def read_comments(item_id):
    comments = get_comments_by_item(item_id)
    if comments:
        return jsonify(comments), 200
    return jsonify({"error": "No comments found for this item"}), 404


@app.route("/comments/<int:comment_id>", methods=["PUT"])
def update_comment(comment_id):
    data = request.json
    updated_comment = update_comment_info(comment_id, data)
    if updated_comment:
        return jsonify({"message": "Comment updated successfully"}), 200
    return jsonify({"error": "Comment not found"}), 404


@app.route("/comments/<int:comment_id>", methods=["DELETE"])
def delete_comment_endpoint(comment_id):
    if delete_comment(comment_id):
        return jsonify({"message": "Comment deleted successfully"}), 200
    return jsonify({"error": "Comment not found"}), 404


# PRICE & STORE COMPARISON ENDPONTS
@app.route("/recommend_store", methods=["POST"])
def recommend_store():
    data = request.json
    shopping_list = data.get("shopping_list")
    user_location = data.get("user_location")
    if not shopping_list or not user_location:
        return jsonify({"error": "Missing required fields"}), 400
    best_store = calculate_best_store(shopping_list, user_location)
    if not best_store:
        return jsonify({"error": "No suitable stores found"}), 404
    store_info = {
        "id": best_store.key.id,
        "name": best_store["name"],
        "location": best_store["location"],
        "timestamp": best_store["timestamp"].isoformat()
    }
    return jsonify(store_info), 200

# STORE LOCATION ENDPOINT
@app.route("/stores_nearby")
def stores_nearby():
    radius = float(request.args.get('radius'))
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))
    user_location = (latitude, longitude)

    stores = get_nearby_stores(user_location, radius)
    return jsonify(stores)

# DATASTORE FETCHING ENDPOINTS
@app.route("/api/stores", methods=["GET"])
def get_stores():
    query = datastore_client.query(kind="Store")
    stores = list(query.fetch())
    store_list = []
    for store in stores:
        store_data = {
            "id": store.key.id,  
            "name": store["name"],
            "location": store["location"]
        }
        store_list.append(store_data)
    return jsonify(store_list)


@app.route("/api/store/<int:store_id>/items", methods=["GET"])
def get_items_by_store(store_id):
    query = datastore_client.query(kind="Price")
    query.add_filter("store_id", "=", store_id)
    prices = list(query.fetch())
    item_ids = {price["item_id"] for price in prices}
    items = []
    for item_id in item_ids:
        item = get_item_by_id(item_id)
        if item:
            item_info = item.copy()
            item_price_info = next(price for price in prices if price["item_id"] == item_id)
            item_info["price"] = item_price_info["price"]
            item_info["sale_status"] = item_price_info["sale_status"]
            items.append(item_info)
    
    return jsonify(items)

@app.route("/api/item/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = get_item_by_id(item_id)
    if item:
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

@app.route("/api/current_user", methods=["GET"])
def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return jsonify({"user_id": user_id})
    return jsonify({"error": "User not logged in"}), 401

@app.route("/api/shoppinglist", methods=["POST"])
def create_or_update_shoppinglist():
    data = request.json
    user_id = data.get("user_id")
    item_id = data.get("item_id")
    
    if not user_id or not item_id:
        return jsonify({"error": "Missing user_id or item_id"}), 400
    
    shopping_list = get_shoppinglist_by_user(user_id)
    
    if shopping_list:
        shopping_list = shopping_list
        if "items" not in shopping_list:
            shopping_list["items"] = []
        shopping_list["items"].append(item_id)
        datastore_client.put(shopping_list)
    else:
        shopping_list_id = store_shoppinglist(user_id, [item_id])
    
    return jsonify({"message": "Shopping list updated successfully"}), 200

@app.route("/api/shoppinglist/<int:user_id>", methods=["GET"])
def get_shoppinglist(user_id):
    query = datastore_client.query(kind="ShoppingList")
    query.add_filter("user_id", "=", user_id)
    result = list(query.fetch())
    if result:
        shopping_list = result[0]
        items = []
        for item_id in shopping_list["items"]:
            item = get_item_by_id(item_id)
            if item:
                price_info = get_price_info_by_item_id(item_id)  
                item_data = {
                    "id": item.key.id,
                    "name": item["name"],
                    "brand": item["brand"],
                    "price": price_info["price"] if price_info else "N/A",
                    "sale_status": price_info["sale_status"] if price_info else "N/A"
                }
                items.append(item_data)
            else:
                app.logger.info(f"Item with ID {item_id} not found in datastore.")
        return jsonify(items), 200
    return jsonify({"error": "Shopping list not found"}), 404


def get_price_info_by_item_id(item_id):
    app.logger.info(f"Fetching price info for item_id: {item_id}")
    query = datastore_client.query(kind="Price")
    query.add_filter("item_id", "=", int(item_id))
    result = list(query.fetch())
    if result:
        app.logger.info(f"Price info found for item_id {item_id}: {result[0]}")
        return result[0]
    else:
        app.logger.info(f"No price info found for item_id {item_id}")
    
    return None


@app.route("/api/shoppinglist/<int:user_id>/remove/<item_id>", methods=["DELETE"])
def remove_item_from_shoppinglist(user_id, item_id):
    query = datastore_client.query(kind="ShoppingList")
    query.add_filter("user_id", "=", int(user_id))
    result = list(query.fetch())
    if result:
        shopping_list = result[0]
        app.logger.info(f"Shopping list found: {shopping_list}")
        
        if "items" in shopping_list and item_id in shopping_list["items"]:
            shopping_list["items"].remove(item_id)
            datastore_client.put(shopping_list)
            return jsonify({"message": "Item removed from shopping list"}), 200
    return jsonify({"error": "Item or shopping list not found"}), 404

# ITEM SCANNING ENDPOINTS AND FUNCTIONS:
@app.route("/api/scan", methods=["POST"])
def scan_item():
    data = request.json
    barcode = data.get("barcode")
    price = data.get("price")
    sale_status = data.get("sale_status")
    tags = data.get("tags")
    user_id = data.get("user_id")

    if not barcode or not price or user_id is None:
        return jsonify({"error": "Missing required fields"}), 400
    item = get_item_by_barcode(barcode)
    if item:
        item_id = item.key.id
    else:
        item_id = store_item_info(barcode, tags, "")
    
    store_price_info(item_id, user_id, price, sale_status)
    for tag in tags:
        store_tag_info(tag)
        assign_tag_to_item(item_id, tag)

    return jsonify({"message": "Item scanned and stored successfully"}), 201

def get_item_by_barcode(barcode):
    query = datastore_client.query(kind="Item")
    query.add_filter("barcode", "=", barcode)
    result = list(query.fetch())
    if result:
        return result[0]
    return None

def store_item_info(barcode, tags, brand):
    entity = datastore.Entity(key=datastore_client.key("Item"))
    entity.update({
        "barcode": barcode,
        "tags": tags,
        "brand": brand,
        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc)
    })
    datastore_client.put(entity)
    return entity.key.id

def store_price_info(item_id, user_id, price, sale_status):
    entity = datastore.Entity(key=datastore_client.key("Price"))
    entity.update({
        "item_id": item_id,
        "user_id": user_id,
        "price": price,
        "sale_status": sale_status,
        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc)
    })
    datastore_client.put(entity)
    return entity.key.id

def store_tag_info(name):
    entity = datastore.Entity(key=datastore_client.key("Tag"))
    entity.update({
        "name": name,
        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc)
    })
    datastore_client.put(entity)
    return entity.key.id

def assign_tag_to_item(item_id, tag_name):
    item = get_item_by_id(item_id)
    if item:
        if "tags" not in item:
            item["tags"] = []
        item["tags"].append(tag_name)
        datastore_client.put(item)
        return item
    return None 

# USER PAGE ENDPOINTS:
def get_user_badges(user_id):
    user = get_user_by_id(user_id)
    if user:
        reputation = user["reputation"]
        if reputation >= 5000:
            return "Master Shopper"
        elif reputation >= 1000:
            return "Gold Shopper"
        elif reputation >= 500:
            return "Silver Shopper"
        elif reputation >= 100:
            return "Bronze Shopper"
        else:
            return "None"
    return None

@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        badge = get_user_badges(user_id)
        user_info = {
            "email": user["email"],
            "reputation": user["reputation"],
            "badge": badge
        }
        return jsonify(user_info), 200
    return jsonify({"error": "User not found"}), 404

@app.route("/api/activitylogs/user/<int:user_id>", methods=["GET"])
def get_activity_logs(user_id):
    logs = get_activitylog_by_user(user_id)
    if logs:
        activities = [{"details": log["details"]} for log in logs]
        return jsonify({"activities": activities}), 200
    return jsonify({"error": "No activity logs found for this user"}), 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
