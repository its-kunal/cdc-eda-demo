import json
import logging
from kafka import KafkaConsumer
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CDCConsumer:
    def __init__(self):
        self.bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.group_id = os.getenv('KAFKA_GROUP_ID', 'cdc-consumer-group')
        
        self.consumer = KafkaConsumer(
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            auto_commit_interval_ms=1000
        )
        
        # Subscribe to topics
        topics = [
            os.getenv('KAFKA_TOPIC_PRODUCTS'),
            os.getenv('KAFKA_TOPIC_ORDERS')
        ]
        self.consumer.subscribe(topics)
        logger.info(f"Subscribed to topics: {topics}")
    
    def process_message(self, message: Dict[str, Any]) -> None:
        """Process incoming CDC message"""
        try:
            topic = message.topic
            value = message.value
            
            # Extract operation type
            operation = value.get('__op', 'unknown')
            
            logger.info(f"Topic: {topic} | Operation: {operation}")
            logger.info(f"Data: {json.dumps(value, indent=2)}")
            
            # Route to appropriate handler
            if 'products' in topic:
                self.handle_product_change(operation, value)
            elif 'orders' in topic:
                self.handle_order_change(operation, value)
                
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
    
    def handle_product_change(self, operation: str, data: Dict[str, Any]) -> None:
        """Handle product table changes"""
        product_id = data.get('id')
        
        if operation == 'c':  # Create
            logger.info(f"New product created: {data.get('name')} (ID: {product_id})")
        elif operation == 'u':  # Update
            logger.info(f"Product updated: ID {product_id}")
            # Check for specific field updates
            if 'quantity' in data:
                logger.info(f"Quantity changed to: {data['quantity']}")
        elif operation == 'd':  # Delete
            logger.info(f"Product deleted: ID {product_id}")
    
    def handle_order_change(self, operation: str, data: Dict[str, Any]) -> None:
        """Handle order table changes"""
        order_id = data.get('id')
        
        if operation == 'c':  # Create
            logger.info(f"New order created: {data.get('customer_name')} (ID: {order_id})")
            logger.info(f"Amount: ${data.get('total_amount')}")
        elif operation == 'u':  # Update
            logger.info(f"Order updated: ID {order_id} | Status: {data.get('status')}")
    
    def start(self) -> None:
        """Start consuming messages"""
        logger.info("Starting CDC consumer...")
        try:
            for message in self.consumer:
                self.process_message(message)
        except KeyboardInterrupt:
            logger.info("Shutting down consumer...")
        finally:
            self.consumer.close()


if __name__ == "__main__":
    consumer = CDCConsumer()
    consumer.start()