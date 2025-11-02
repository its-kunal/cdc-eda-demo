# Change Data Capture with Event Driven Architecture Demo - Apache Kafka | Debezium | Postgres

## Prerequisites

### System Requirements
- Docker & Docker Compose (20.10+)
- Python 3.8+
- 8GB RAM minimum
- 20GB disk space

### Knowledge Prerequisites
- Basic SQL
- Understanding of event streaming concepts
- Python fundamentals
- Docker basics

---

## Step-by-Step Implementation

### Step 1: Start Infrastructure

```bash
# Clone or create project directory
git clone its-kunal/cdc-eda-demo && cd cdc-eda-demo

# Start all services
docker-compose up -d

# Verify all containers are running
docker-compose ps

# Check logs
docker-compose logs -f
```

### Step 2: Register Debezium Connector

```bash
# Wait for Kafka Connect to be ready (check http://localhost:8083)
curl http://localhost:8083/connectors

# Register the connector
curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d @debezium-connector.json

# Verify connector status
curl http://localhost:8083/connectors/inventory-connector/status
```

### Step 3: Verify Kafka Topics

```bash
# List topics (should see cdc.inventory.products and cdc.inventory.orders)
docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092

# View messages in products topic
docker exec -it kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic cdc.inventory.products \
  --from-beginning \
  --max-messages 5
```

### Step 4: Setup Python Consumer

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Testing

### Test 1: Manual Database Changes

```bash
# Connect to PostgreSQL
docker exec -it postgres psql -U postgres -d sourcedb

# Run some updates
UPDATE inventory.products SET quantity = 1000 WHERE id = 1;
INSERT INTO inventory.orders (product_id, customer_name, quantity, total_amount) 
VALUES (1, 'Test Customer', 5, 149.95);
```

### Test 2: Run Consumer

```bash
# Terminal 1: Start consumer
python consumer.py

# Terminal 2: Start data generator
python producer.py
```

### Test 3: Monitor with Kafka UI

Visit http://localhost:8080 to see:
- Topics and message counts
- Consumer groups and lag
- Connector status

---

## Troubleshooting

### Connector Not Starting

```bash
# Check connector logs
docker logs connect

# Reset connector
curl -X DELETE http://localhost:8083/connectors/inventory-connector
# Then re-register
```

### No Messages in Topics

```bash
# Verify WAL level
docker exec postgres psql -U postgres -c "SHOW wal_level;"

# Check publication
docker exec postgres psql -U postgres -d sourcedb -c "\dRp+"
```

### Consumer Not Receiving Messages

```python
# Check consumer group status
from kafka import KafkaConsumer
consumer = KafkaConsumer(bootstrap_servers='localhost:9092')
print(consumer.topics())
```

---

## Contributing

Contributions are welcome! 🤗

If you'd like to improve this demo, add new features, or fix bugs, feel free to fork the repository and submit a pull request.  
Please ensure your code is well-documented and follows best practices.
