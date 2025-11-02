-- Create database schema
CREATE SCHEMA IF NOT EXISTS inventory;

-- Create products table
CREATE TABLE inventory.products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create orders table
CREATE TABLE inventory.orders (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES inventory.products(id),
    customer_name VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO inventory.products (name, description, price, quantity, category) VALUES
    ('Laptop', 'High-performance laptop', 1299.99, 50, 'Electronics'),
    ('Mouse', 'Wireless mouse', 29.99, 200, 'Accessories'),
    ('Keyboard', 'Mechanical keyboard', 89.99, 150, 'Accessories'),
    ('Monitor', '27-inch 4K monitor', 399.99, 75, 'Electronics'),
    ('Headphones', 'Noise-canceling headphones', 249.99, 100, 'Audio');

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add trigger to products table
CREATE TRIGGER update_products_updated_at BEFORE UPDATE
    ON inventory.products FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Grant necessary privileges
ALTER TABLE inventory.products REPLICA IDENTITY FULL;
ALTER TABLE inventory.orders REPLICA IDENTITY FULL;