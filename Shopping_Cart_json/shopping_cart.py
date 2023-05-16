import json
import jsonschema

# product list file validation
def product_list_validation(data_file):
    #read the product details json file
    try:
        with open(data_file,'r') as data_file:
            data = json.load(data_file)
          
    except ValueError as e:
        print("Error in reading the file", e)
        exit()
    #read json schema file
    try:
        with open("C:\\Python_PyCharm\\Training\\Shopping_Cart_json\\product_list_schema.json",'r') as schema_file:
            schema = json.load(schema_file)
            
    except ValueError as e:
        print("Error in reading the file", e)
        exit()
    try:
        jsonschema.validate(data, schema)
        print("JSON data is valid")
    except jsonschema.exceptions.ValidationError as e:
        print("Json validation error", e)        

#Validate customer data file
def customer_data_validation(data_file):
    #read the product details json file
    try:
        with open(data_file,'r') as data_file:
            data = json.load(data_file)
          
    except ValueError as e:
        print("Error in reading the file", e)
        exit()
    #read json schema file
    try:
        with open("C:\\Python_PyCharm\\Training\\Shopping_Cart_json\\customer_data_schema.json",'r') as schema_file:
            schema = json.load(schema_file)
            
    except ValueError as e:
        print("Error in reading the file", e)
        exit()
    try:
        jsonschema.validate(data, schema)
        print("JSON data is valid")
    except jsonschema.exceptions.ValidationError as e:
        print("Json validation error", e)    

#read the customer data json file
def read_customer_details_data():
    try:
        with open("C:\\Python_PyCharm\\Training\\Shopping_Cart_json\\customer_data.json",'r') as data_file:
            data = json.load(data_file)
            return data
    except ValueError as e:
        print("Error in reading the file", e)
        exit()



class shopping_cart:

    shopping_cart_items = []
    
    def __init__(self, product_list_file, cust_data_file):
        self.product_list_file = product_list_file
        self.cust_data_file = cust_data_file 
        product_list_validation(self.product_list_file)
        customer_data_validation( self.cust_data_file )
    

    #Add items to cart
    def add_items_to_cart(self, add_items):
        self.shopping_cart_items.append(add_items)
        #print(self.shopping_cart_items) 
        new_item = 0
        item_added = 0
        exist_cust_item =0
        with open(self.product_list_file, 'r+') as f_cart_data: 
            read_data = json.load(f_cart_data)
            for item_cart in read_data["customer_cart"]:
                for add in add_items:
                    if item_added == 1:
                        break
                    if item_cart["customer_member_id"]  == add_items["customer_member_id"]:
                        new_item = 1
                                                
                        for key,value in item_cart.items():
                            
                            for add_key, add_value in add_items.items():
                                
                                if key == "Items" and add_key == "Items":
                                    
                                    for add_fruit in add_value:
                                        for exist_product in value:
                                            
                                            if exist_product["product_name"] == add_fruit["product_name"] and exist_cust_item == 1:
                                                exist_product["Quantity"] += add_fruit["Quantity"]
                                                print("Quantity",exist_product["Quantity"])
                                                item_added = 1
                                                f_cart_data.truncate(0)
                                                f_cart_data.seek(0)
                                                json.dump(read_data, f_cart_data, indent=4 )
                                            else:
                                                if not any(exist_product["product_name"] == add_fruit["product_name"] for exist_product in value ):
                                                    value.append(add_fruit)
                                                    add_value.remove(add_fruit)
                                                    print(value, add_value)
                                                    exist_cust_item = 1
                                                    f_cart_data.truncate(0)
                                                    f_cart_data.seek(0)
                                                    json.dump(read_data, f_cart_data, indent=4 )
                                                    break
                                                break
                                                                
                    else:
                        break

            if new_item == 0:  
                read_data["customer_cart"].append(add_items)
                f_cart_data.seek(0)
                json.dump(read_data, f_cart_data, indent=4 )


    def remove_items_from_cart(self, remove_items):
        update = 0
        
        with open(self.product_list_file, 'r+') as f_cart_data:
            cart_data = json.load(f_cart_data)
            
            for item_cart in cart_data["customer_cart"]: 
                for remove in remove_items:
                    
                    if update == 1:
                        break
                    if item_cart["customer_member_id"] == remove_items["customer_member_id"]:
                        for key,value in item_cart.items():
                           
                            for remove_key, remove_value in remove_items.items():
                                
                                if key == "Items" and remove_key == "Items":
                                    for fruit in value:
                                        for remove_fruit in remove_value:
                                            if fruit["product_name"] == remove_fruit["product_name"]:

                                                fruit["Quantity"] = fruit["Quantity"] - remove_fruit["Quantity"]
                                                if fruit["Quantity"] <= 0:
                                                    fruit["Quantity"] = 0
                                                print("Quantity",fruit["Quantity"])
                                                update = 1
                 
            f_cart_data.truncate(0)
            f_cart_data.seek(0)
            update_data = json.dump(cart_data, f_cart_data,indent=4)
                                    
       
    def show_items_cart(self, cust_ID):
        with open(self.product_list_file, 'r') as f_cart_data:
            cart_data = json.load(f_cart_data)
            print("Items in the cart for customer: ",cust_ID)
            for item_cart in cart_data["customer_cart"]:
                if item_cart["customer_member_id"]  == cust_ID:
                    for key,value in item_cart.items():
                        if key == "Items":
                            for fruit in value:
                                print("Product :", fruit["product_name"])
                                print("Quantity :",fruit["Quantity"])
                                    

    def get_total_price(self, cust_ID):
        total_price = 0
        with open(self.product_list_file, 'r') as f_cart_data:
            cart_data = json.load(f_cart_data)

            for item_cart in cart_data["customer_cart"]:
                for item in cart_data["products"]:
                    
                    if item_cart["customer_member_id"]  == cust_ID:  
                        for key,value in item_cart.items():
                            if key == "Items":
                                for fruit in value:
                                    if fruit["product_name"] == item["product_name"]:
                                        """print("Product", fruit["product_name"])
                                        print("Quantity",fruit["Quantity"])
                                        print("unit_price",item["unit_price"])"""
                                        total_price += item["unit_price"] * fruit["Quantity"] 

            print(f"Total price for {cust_ID} is :",total_price)

           

f_product_list = "C:\\Python_PyCharm\\Training\\Shopping_Cart_json\\product_list.json"
f_customer_data = "C:\\Python_PyCharm\\Training\\Shopping_Cart_json\\customer_data.json"
customer_1 = shopping_cart(f_product_list, f_customer_data)

customer_1.add_items_to_cart({"customer_member_id": 1011,"Items":[{"product_name":"Apple", "Quantity": 2}, {"product_name":"Orange", "Quantity": 2}]})
customer_1.add_items_to_cart({"customer_member_id": 1021,"Items":[{"product_name":"Apple", "Quantity": 4}, {"product_name":"Notebook", "Quantity": 2}]})
customer_1.add_items_to_cart({"customer_member_id": 1013,"Items":[{"product_name":"Bread", "Quantity": 1}, {"product_name":"Cereal", "Quantity": 2}, {"product_name":"Jam", "Quantity": 5}]})
customer_1.add_items_to_cart({"customer_member_id": 1011,"Items":[{"product_name":"Bread", "Quantity": 2}]})


print("**********TOTAL PRICE BEORE***************")
customer_1.get_total_price(1011)
customer_1.get_total_price(1021)
customer_1.get_total_price(1013)
print("********SHOW ITEMS***************")
customer_1.show_items_cart(1021)
customer_1.show_items_cart(1011)
customer_1.show_items_cart(1013)
customer_1.remove_items_from_cart({"customer_member_id": 1011,"Items":[{"product_name":"Apple", "Quantity": 1}]})
customer_1.remove_items_from_cart({"customer_member_id": 1013,"Items":[{"product_name":"Jam", "Quantity": 1}]})
print("**********Total price after remove an item:********")
customer_1.get_total_price(1011)
customer_1.get_total_price(1013)

