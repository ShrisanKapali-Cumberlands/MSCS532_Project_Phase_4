# MSCS 532 Alorithms and Data Structure

## Shrisan Kapali

## Student Id : 005032249

### Project phase 4 - Inventory Management System

To run the program, on the terminal run the following command

```
py Project_Phase_4.py
```

## Final report

The inventory management system is coded in Python and utilizes various data structures, including dictionaries, lists, tuples, stacks, priority queues, and heaps. It addresses these data structures in performing CRUD operations on inventory categories and products.

Functions such as updating a product or category, updating the price, increasing and decreasing product quantity, and searching a product or category using the name and price range are also implemented.

LRU cache and manual memoization using dictionaries have been implemented to improve the search performance when the application is scaled to handle large data sets.

Additionally, the project includes test cases that validate the effectiveness of the chosen data structures.

## Code Walkthough

Classes implemented - Inventory, Category, Product

Initially class category has been initalized, with functions to update its fields.
Class product has been intialized with functions to update its field, increase/decrease quantity

Class inventory contains dictionary of categories and products. While adding new category and products, the id is checked such that the value is note overwritten. In case the same id is used, Value Error exception is thrown.

As we implemented LRU caching, everytime a new record is added/updated, the LRU cache is cleared.

Search functionality to search category using name using no cache, LRU cache, and custom memoized searched using dictionary has been implemented.

Search functionality for product using product name, category name and ID has been implemented usign no cache, LRU cache, and memoized cache.

Everytime a product price is updated, the new price is also stored in Product.price_history field as tuple with date and new price

## Test Cases

Adding new Category - 20000 new categories have been added using a for loop. In the event the same id is passed, the application will throw ValueError.

Adding Products - 100000 new products have been added. In the event the same id is passed, the application will throw ValueError.

To test the functionality of update, update function test cases have been written. Using a known id, we update category status. We print the sucessful result by printing the result using the search category by name method we implemented. Previous value and new value have been printed in the terminal.

Test cases to test the update functionality of product and to verify search functionality of products using name, category name, and ID has been implemented. The updated results are printed on the terminal which verifies correctness of the implemented methods.

Price history can be printed. If no price history is there, it prints empty.

## Stress testing

100 test were conducted for each search functionality. For each test run, a random category and product name, random price was generated. The results of the search for no-cache, LRU cache, and custom memoized cache was graphed.
