import psycopg2
import time
import random
from decimal import Decimal
import os
from dotenv import load_dotenv

load_dotenv()


class DataGenerator:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        self.cursor = self.conn.cursor()
    
    def update_random_product_quantity(self):
        """Simulate inventory update"""
        product_id = random.randint(1, 5)
        new_quantity = random.randint(0, 300)
        
        self.cursor.execute(
            "UPDATE inventory.products SET quantity = %s WHERE id = %s",
            (new_quantity, product_id)
        )
        self.conn.commit()
        print(f"Updated product {product_id} quantity to {new_quantity}")
    
    def create_random_order(self):
        """Simulate new order"""
        product_id = random.randint(1, 5)
        quantity = random.randint(1, 10)
        
        # Get product price
        self.cursor.execute(
            "SELECT price FROM inventory.products WHERE id = %s",
            (product_id,)
        )
        price = self.cursor.fetchone()[0]
        total = Decimal(price) * quantity
        
        customers = ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown']
        customer = random.choice(customers)
        
        self.cursor.execute(
            """INSERT INTO inventory.orders 
               (product_id, customer_name, quantity, total_amount, status)
               VALUES (%s, %s, %s, %s, %s)""",
            (product_id, customer, quantity, total, 'pending')
        )
        self.conn.commit()
        print(f"Created order for {customer}: {quantity} items, ${total}")
    
    def update_order_status(self):
        """Simulate order status update"""
        self.cursor.execute("SELECT id FROM inventory.orders ORDER BY RANDOM() LIMIT 1")
        result = self.cursor.fetchone()
        
        if result:
            order_id = result[0]
            statuses = ['processing', 'shipped', 'delivered']
            new_status = random.choice(statuses)
            
            self.cursor.execute(
                "UPDATE inventory.orders SET status = %s WHERE id = %s",
                (new_status, order_id)
            )
            self.conn.commit()
            print(f"Updated order {order_id} status to {new_status}")
    
    def run(self):
        """Run random operations"""
        print("Starting data generator...")
        try:
            while True:
                operation = random.choice(['update_product', 'create_order', 'update_order'])
                
                if operation == 'update_product':
                    self.update_random_product_quantity()
                elif operation == 'create_order':
                    self.create_random_order()
                elif operation == 'update_order':
                    self.update_order_status()
                
                time.sleep(random.uniform(2, 5))
        except KeyboardInterrupt:
            print("\nStopping data generator...")
        finally:
            self.cursor.close()
            self.conn.close()


if __name__ == "__main__":
    generator = DataGenerator()
    generator.run()