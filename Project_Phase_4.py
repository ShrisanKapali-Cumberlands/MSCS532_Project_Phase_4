## *************************************************************** ##
## MSCS 532 - Algorithms and Data Structures
## Project Phase 4
## Inventory Management System
## Shrisan kapali - 005032249
## *************************************************************** ##

import random
import time

## Dyanamic Inventory Management System
## This program will allow end users to perform CRUD operations on products and categories
from datetime import datetime
from functools import lru_cache

import matplotlib.pyplot as plt


# Defining the class Category
# A category has unique id assigned to it
# A category has a name and the status can be active or inactive i.e, true or false
class Category:
    # Constructor to initialize a category class object
    def __init__(self, cagetory_id: int, name: str, status: bool = True):
        self.category_id = cagetory_id
        self.name = name
        self.status = status

    # Perform update on a category
    # Only perform update on the passed in value
    def update(self, name: str = None, status: bool = None):
        if name:
            self.name = name
        if status is not None:
            self.status = status

    # Printing the category when print command is used
    # Print layout Example "Category 1, Name Grocery, Current Status Active"
    def __repr__(self):
        return f"Category ({self.category_id}), Name {self.name}, Current Status {'Active' if self.status else 'Inactive'}"


# Defining class Product
# A product has id, name, description, quantity and belongs to the category
class Product:
    # Constructor to initialize the product class
    def __init__(
        self,
        product_id: int,
        name: str,
        price: float,
        description: str,
        category: Category,
        quantity: int,
    ):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.quantity = quantity
        self.price_history = [(datetime.now(), price)]  # a list of price history

    # A function to update product information
    def update(
        self,
        name: str = None,
        price: float = None,
        description: str = None,
        category: Category = None,
        quantity: int = None,
    ):
        if name:
            self.name = name
        # Only if the passed in price is not equal to old price
        if price is not None and price != self.price:
            self.price = price
            # Append the new price in the price history list
            self.price_history.append((datetime.now(), price))
        if description:
            self.description = description
        if category:
            self.category = category
        if quantity is not None and quantity != self.quantity:
            self.quantity = quantity

    # A function to increase quantity
    def increaseQuantity(self, increaseBy: int):
        self.quantity += increaseBy

    # A function to decrease quantity
    def decreaseQuantity(self, increaseBy: int):
        self.quantity -= increaseBy

    # A function to print the product class
    def __repr__(self):
        return f"Product Id: {self.product_id}, Product Price: {self.price}, Product Name: {self.name}, Description: {self.description}, Quantity: {self.quantity}, Category:{self.category.name}"


# Finally as we now have product and category class, create Inventory class
class Inventory:

    # Intialize inventory class with empty categories and product dictionary
    def __init__(self):
        self.categories = {}
        self.products = {}
        # Implementing manual caching
        self.memoized_search = {}

    ## ******************************************** ##
    # Inventory Category Management
    ## ******************************************** ##
    # Functions to add and update category and products
    # Each id needs to be unique so
    def is_category_id_unique(self, category_id: int) -> bool:
        return category_id not in self.categories

    # Also check if product id is unique
    def is_product_id_unique(self, product_id: int) -> bool:
        return product_id not in self.products

    # Add new category
    def add_new_category(self, category_id: int, name: str, status: bool = True):
        # First check if the category id is unique
        if not self.is_category_id_unique(category_id):
            raise ValueError("Category Id must be unique. This id already exists")

        # Add the category using category_id as key
        self.categories[category_id] = Category(category_id, name, status)
        # Clear manual cache on each new addition
        self.clear_cache()

    # Update Category name or status
    def update_category(self, cagetory_id: int, name: str = None, status: bool = None):
        # If passed in category id is not present, return error
        if cagetory_id not in self.categories:
            raise ValueError(
                "Unable to find the category for this passed in cateogry id"
            )

        # Use category update method to update the category details
        self.categories[cagetory_id].update(name, status)
        # Clear manual cache on each update
        self.clear_cache()

    # Delete existing category
    def delete_category(self, cagetory_id: int):
        # If passed in category id is not present, return error
        if cagetory_id not in self.categories:
            raise ValueError(
                "Unable to find the category for this passed in cateogry id"
            )

        del self.categories[cagetory_id]
        # Clear manual cache on each update
        self.clear_cache()

    # Adding lru automatic caching as well
    # A function to search category by name
    @lru_cache(maxsize=20000)
    def search_category_by_name(self, name: str):
        return [
            category
            for category in self.categories.values()
            if name.lower() in category.name.lower()
        ]

    # Without cache
    def search_category_by_name_no_cache(self, name: str):
        return [
            category
            for category in self.categories.values()
            if name.lower() in category.name.lower()
        ]

    # Manual caching
    def search_category_by_name_memo(self, name: str):
        # if the name is already in cache, return from cache
        if name in self.memoized_search:
            return self.memoized_search[name]
        result = [
            category
            for category in self.categories.values()
            if name.lower() in category.name.lower()
        ]
        # Add this result to cache for faster retrieval
        self.memoized_search[name] = result
        return result

    ## ******************************************** ##
    # Inventory Product Management
    ## ******************************************** ##

    # Add in a new product
    def add_product(
        self,
        product_id: int,
        name: str,
        price: float,
        description: str,
        category_id: int,
        quantity: int,
    ):
        # First check if the product id is unique
        if not self.is_product_id_unique(product_id):
            raise ValueError("Product with the same id already exists.")

        # Now check if the category id exists
        if category_id not in self.categories:
            raise ValueError("Passed in category id is invalid")

        # Extract the category
        category = self.categories[category_id]

        # Finally add in the product
        self.products[product_id] = Product(
            product_id, name, price, description, category, quantity
        )
        # Clear manual cache on each new addition
        self.clear_cache()

    # Update the existing product details
    def update_product(
        self,
        product_id: int,
        name: str = None,
        price: float = None,
        description: str = None,
        category_id: int = None,
        quantity: int = None,
    ):
        if product_id not in self.products:
            raise ValueError("Unable to find product using the passed in id")

        # Get existing product
        product = self.products[product_id]

        # Check if category changed, if changed get the new category
        # If new category id exists, get the category by id or use existing
        category = (
            self.categories.get(category_id, product.category)
            if category_id
            else product.category
        )

        # Finally call in product update function to update the values
        product.update(name, price, description, category, quantity)
        # Clear manual cache on each new update
        self.clear_cache()

    # Increase product quantity by quantity
    def increase_product_quantity(self, product_id: int, quantity: int):
        if product_id not in self.products:
            raise ValueError("Unable to find the product using passed in id")

        self.products[product_id].increaseQuantity(quantity)
        # Clear manual cache on each new update
        self.clear_cache()

    # Decrease product quantity by quantity
    def decrease_product_quantity(self, product_id: int, quantity: int):
        if product_id not in self.products:
            raise ValueError("Unable to find the product using passed in id")

        self.products[product_id].decreaseQuantity(quantity)
        # Clear manual cache on each new update
        self.clear_cache()

    # View product price history
    @lru_cache(maxsize=20000)  # Adding the cache
    def get_product_price_history(self, product_id: int):
        if product_id not in self.products:
            raise ValueError("Unable to find the product using passed in id")

        return self.products[product_id].price_history

    # Search product by name
    def search_product_by_name_no_cache(self, name: str):
        return [
            product
            for product in self.products.values()
            if name.lower() in product.name.lower()
        ]

    @lru_cache(maxsize=20000)  # Adding the cache
    def search_product_by_name(self, name: str):
        return [
            product
            for product in self.products.values()
            if name.lower() in product.name.lower()
        ]

    # Manual cache memory search
    def search_product_by_name_memo(self, name: str):
        # If this name is present in the memory, return with the value
        if name in self.memoized_search:
            return self.memoized_search[name]
        result = [
            product
            for product in self.products.values()
            if name.lower() in product.name.lower()
        ]
        # Store this value to cache
        self.memoized_search[name] = result
        return result

    # Search product by price range
    def search_product_by_price_range_no_cache(
        self, min_price: float, max_price: float
    ):
        return [
            product
            for product in self.products.values()
            if min_price <= product.price <= max_price
        ]

    @lru_cache(maxsize=20000)  # Adding the cache
    def search_product_by_price_range(self, min_price: float, max_price: float):
        return [
            product
            for product in self.products.values()
            if min_price <= product.price <= max_price
        ]

    # Manual cache memory search
    def search_product_by_price_range_memo(self, min_price: float, max_price: float):
        # Setup a unique key with min and max price
        key = f"{min_price}-{max_price}"
        # If this key is present, return value from memory
        if key in self.memoized_search:
            return self.memoized_search[key]
        # Add this result to cache
        result = [
            product
            for product in self.products.values()
            if min_price <= product.price <= max_price
        ]
        self.memoized_search[key] = result
        return result

    # Search product by category id
    def search_product_by_category_id_no_cache(self, category_id: int):
        return [
            product
            for product in self.products.values()
            if product.category.category_id == category_id
        ]

    @lru_cache(maxsize=20000)  # Adding the cache
    def search_product_by_category_id(self, category_id: int):
        return [
            product
            for product in self.products.values()
            if product.category.category_id == category_id
        ]

    # Manual memoization
    def search_product_by_category_id_memo(self, category_id: int):
        # Setup a unique key with category id
        key = f"category-{category_id}"
        if key in self.memoized_search:
            return self.memoized_search[key]

        result = [
            product
            for product in self.products.values()
            if product.category.category_id == category_id
        ]
        self.memoized_search[key] = result
        return result

    # Search product by category name
    def search_product_by_category_name_no_cache(self, name: str):
        return [
            product
            for product in self.products.values()
            if name.lower() in product.category.name.lower()
        ]

    @lru_cache(maxsize=20000)  # Adding the cache
    def search_product_by_category_name(self, name: str):
        return [
            product
            for product in self.products.values()
            if name.lower() in product.category.name.lower()
        ]

    # Manual
    def search_product_by_category_name_memo(self, name: str):
        # Setup a unique key with category name
        key = f"product-category-{name}"
        if key in self.memoized_search:
            return self.memoized_search[key]
        result = [
            product
            for product in self.products.values()
            if name.lower() in product.category.name.lower()
        ]
        self.memoized_search[key] = result
        return result

    # A method to clear all cache
    def clear_cache(self):
        # Clearing all the manual cache
        self.memoized_search.clear()
        # Clearing all the automatic cache
        self.search_category_by_name.cache_clear()
        self.search_product_by_category_id.cache_clear()
        self.search_product_by_category_name.cache_clear()
        self.search_product_by_name.cache_clear()
        self.search_product_by_price_range.cache_clear()

    # Finally a product to print the inventory class
    def __repr__(self):
        return f"Inventory Details \nCategories:{list(self.categories.values())}, \n\nProducts:{list(self.products.values())})"


## ****************************** ##
## Comprehensive Test Case
## ****************************** ##
## Initializing the inventory
inventory = Inventory()
print("******************************")
print("*** Initializing Inventory ***")
print("******************************")

## Add in the product categories
start = time.time()
for i in range(0, 20000):
    inventory.add_new_category(i, f"Category-{i}")
end = time.time()
print("\n******************************")
print("Adding new category")
print("******************************")
print("20000 new categories are added")
print(f"Execution time - {end-start} seconds")
print("Current inventory category size", len(inventory.categories))
print("******************************")


# Adding in products
start = time.time()
for i in range(0, 100000):
    inventory.add_product(
        i,
        f"Product-{i}",
        random.uniform(1, 200),
        "Simple Description",
        random.randint(1, 10000),
        random.randint(1, 1000),
    )
end = time.time()
print("\n******************************")
print("Adding new products")
print("******************************")
print("100000 new products are added")
print(f"Execution time - {end-start} seconds")
print("Current inventory products size", len(inventory.products))
print("******************************")


# Beginning stress testing
# Storing the execution time for each search
# Creating a test case method to conduct the test
searchTimes = {
    "categoryName": [],
    "productName": [],
    "priceRange": [],
    "productByCategegoryName": [],
    "productByCategegoryId": [],
}
automaticCacheSearchTimes = {
    "categoryName": [],
    "productName": [],
    "priceRange": [],
    "productByCategegoryName": [],
    "productByCategegoryId": [],
}
manualCacheSearchTimes = {
    "categoryName": [],
    "productName": [],
    "priceRange": [],
    "productByCategegoryName": [],
    "productByCategegoryId": [],
}

# For general conduct 100 tests
for _ in range(100):
    # First search criterias
    search_category_name = f"Category-{random.randint(1,10000)}"
    search_product_name = f"Product-{random.randint(1,10000)}"
    search_min_price = random.uniform(1, 200)
    search_max_price = random.uniform(1, 200)
    search_category_id = random.randint(1, 10000)

    # Measuring the time for each search functionality
    # *******************************
    # Searching category by name
    # *******************************
    start = time.time()
    inventory.search_category_by_name_no_cache(search_category_name)
    end = time.time()
    searchTimes["categoryName"].append(end - start)
    # print(search_category_name)
    # print(inventory.search_category_by_name_no_cache(search_category_name))
    # Automatic cache
    start = time.time()
    inventory.search_category_by_name(search_category_name)
    end = time.time()
    automaticCacheSearchTimes["categoryName"].append(end - start)
    # print(search_category_name)
    # print(inventory.search_category_by_name(search_category_name))
    # Manual Cache
    start = time.time()
    inventory.search_category_by_name_memo(search_category_name)
    end = time.time()
    manualCacheSearchTimes["categoryName"].append(end - start)
    # print(search_category_name)
    # print(inventory.search_category_by_name_memo(search_category_name))

    # *******************************
    # Searching product by name
    # *******************************
    start = time.time()
    inventory.search_product_by_name_no_cache(search_product_name)
    end = time.time()
    searchTimes["productName"].append(end - start)
    # Automatic cache
    start = time.time()
    inventory.search_product_by_name(search_product_name)
    end = time.time()
    automaticCacheSearchTimes["productName"].append(end - start)
    # Manual Cache
    start = time.time()
    inventory.search_product_by_name_memo(search_product_name)
    end = time.time()
    manualCacheSearchTimes["productName"].append(end - start)

    # *******************************
    # Searching product by price range
    # *******************************
    start = time.time()
    inventory.search_product_by_price_range_no_cache(search_min_price, search_max_price)
    end = time.time()
    searchTimes["priceRange"].append(end - start)
    # Automatic cache
    start = time.time()
    inventory.search_product_by_price_range(search_min_price, search_max_price)
    end = time.time()
    automaticCacheSearchTimes["priceRange"].append(end - start)
    # Manual Cache
    start = time.time()
    inventory.search_product_by_price_range_memo(search_min_price, search_max_price)
    end = time.time()
    manualCacheSearchTimes["priceRange"].append(end - start)

    # *******************************
    # Searching prodcut by category id
    # *******************************
    start = time.time()
    inventory.search_product_by_category_id_no_cache(search_category_id)
    end = time.time()
    searchTimes["productByCategegoryId"].append(end - start)
    # Automatic cache
    start = time.time()
    inventory.search_product_by_category_id(search_category_id)
    end = time.time()
    automaticCacheSearchTimes["productByCategegoryId"].append(end - start)
    # Manual Cache
    start = time.time()
    inventory.search_product_by_category_id_memo(search_category_id)
    end = time.time()
    manualCacheSearchTimes["productByCategegoryId"].append(end - start)

    # *******************************
    # Searching prodcut by category name
    # *******************************
    start = time.time()
    inventory.search_product_by_category_name_no_cache(search_category_name)
    end = time.time()
    searchTimes["productByCategegoryName"].append(end - start)
    # Automatic cache
    start = time.time()
    inventory.search_product_by_category_name(search_category_name)
    end = time.time()
    automaticCacheSearchTimes["productByCategegoryName"].append(end - start)
    # Manual Cache
    start = time.time()
    inventory.search_product_by_category_name_memo(search_category_name)
    end = time.time()
    manualCacheSearchTimes["productByCategegoryName"].append(end - start)

# Now plotting the graph to view the change
# **************************************
# Plotting search for category name
# **************************************
plt.figure(figsize=(12, 6))
plt.plot(
    searchTimes["categoryName"],
    label="Regular Search by Category Name",
    linestyle="--",
    marker="o",
)
plt.plot(
    automaticCacheSearchTimes["categoryName"],
    label="LRU Search by Category Name",
    linestyle="--",
    marker="*",
)
plt.plot(
    manualCacheSearchTimes["categoryName"],
    label="Memoized Search by Category Name",
    linestyle="-",
    marker=".",
)


plt.xlabel("Test Number")
plt.ylabel("Time (seconds)")
plt.title("Category Search - Reguar vs LRU Cache vs. Manual Memoization Performance")
plt.legend()
plt.grid(True)
plt.show()


# **************************************
# Plotting search for product name
# **************************************
plt.figure(figsize=(12, 6))
plt.plot(
    searchTimes["productName"],
    label="Regular Search by Product Name",
    linestyle="--",
    marker="o",
)
plt.plot(
    automaticCacheSearchTimes["productName"],
    label="LRU Search by Product Name",
    linestyle="--",
    marker="*",
)
plt.plot(
    manualCacheSearchTimes["productName"],
    label="Memoized Search by Product Name",
    linestyle="-",
    marker=".",
)


plt.xlabel("Test Number")
plt.ylabel("Time (seconds)")
plt.title("Product Search - Reguar vs LRU Cache vs. Manual Memoization Performance")
plt.legend()
plt.grid(True)
plt.show()

# **************************************
# Plotting search for price range
# **************************************
plt.figure(figsize=(12, 6))
plt.plot(
    searchTimes["priceRange"],
    label="Regular Search by price range",
    linestyle="--",
    marker="o",
)
plt.plot(
    automaticCacheSearchTimes["priceRange"],
    label="LRU Search by price range",
    linestyle="--",
    marker="*",
)
plt.plot(
    manualCacheSearchTimes["priceRange"],
    label="Memoized Search by price range",
    linestyle="-",
    marker=".",
)


plt.xlabel("Test Number")
plt.ylabel("Time (seconds)")
plt.title("Price Range Search - Reguar vs LRU Cache vs. Manual Memoization Performance")
plt.legend()
plt.grid(True)
plt.show()

# **************************************
# Plotting search for product using category name
# **************************************
plt.figure(figsize=(12, 6))
plt.plot(
    searchTimes["productByCategegoryName"],
    label="Product Search by category name",
    linestyle="--",
    marker="o",
)
plt.plot(
    automaticCacheSearchTimes["productByCategegoryName"],
    label="Product LRU Search by category name",
    linestyle="--",
    marker="*",
)
plt.plot(
    manualCacheSearchTimes["productByCategegoryName"],
    label="Product Memoized Search by category name",
    linestyle="-",
    marker=".",
)


plt.xlabel("Test Number")
plt.ylabel("Time (seconds)")
plt.title(
    "Product Search by category name - Reguar vs LRU Cache vs. Manual Memoization Performance"
)
plt.legend()
plt.grid(True)
plt.show()

# **************************************
# Plotting search for product using category Id
# **************************************
plt.figure(figsize=(12, 6))
plt.plot(
    searchTimes["productByCategegoryId"],
    label="Product Search by category Id",
    linestyle="--",
    marker="o",
)
plt.plot(
    automaticCacheSearchTimes["productByCategegoryId"],
    label="Product LRU Search by category Id",
    linestyle="--",
    marker="*",
)
plt.plot(
    manualCacheSearchTimes["productByCategegoryId"],
    label="Product Memoized Search by category Id",
    linestyle="-",
    marker=".",
)


plt.xlabel("Test Number")
plt.ylabel("Time (seconds)")
plt.title(
    "Product Search by category Id - Reguar vs LRU Cache vs. Manual Memoization Performance"
)
plt.legend()
plt.grid(True)
plt.show()
