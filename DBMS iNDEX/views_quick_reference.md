# Database Views - Quick Reference

## What is a View?
A **View** is a virtual table based on an SQL query. It doesn't store data physically but shows data from underlying tables dynamically.

## Why Use Views?
- **Security**: Hide sensitive columns
- **Simplicity**: Simplify complex queries
- **Reusability**: Reuse common queries
- **Abstraction**: Present data in different formats

## Basic Syntax

### Create View
```sql
CREATE VIEW view_name AS
SELECT columns FROM table WHERE condition;
```

### Drop View
```sql
DROP VIEW view_name;
```

### Query View
```sql
SELECT * FROM view_name;
```

## Quick Examples

### 1. Simple View
```sql
CREATE VIEW active_employees AS
SELECT name, department FROM employees 
WHERE status = 'active';
```

### 2. Join View
```sql
CREATE VIEW customer_orders AS
SELECT c.name, o.order_date, o.amount
FROM customers c JOIN orders o ON c.id = o.customer_id;
```

### 3. Aggregate View
```sql
CREATE VIEW dept_summary AS
SELECT department, COUNT(*) as emp_count, AVG(salary) as avg_salary
FROM employees GROUP BY department;
```

## Key Points
- Views are virtual, not physical tables
- Data is generated when queried
- Can be based on one or multiple tables
- Not all views are updatable
- Can impact performance if complex

## Interview Essentials

**Q: View vs Table?**
- Table: Physical storage, faster access
- View: Virtual, no storage, dynamic data

**Q: Can you update through views?**
- Yes, but limited conditions:
  - Single table based
  - Must include primary key
  - No aggregates/GROUP BY

**Q: Types of Views?**
- Regular View: Virtual, no storage
- Materialized View: Physical storage, periodic refresh

## When to Use
✅ **Use When:**
- Complex joins needed frequently
- Need to hide sensitive data
- Want to standardize data access
- Creating reports

❌ **Avoid When:**
- Simple single table queries
- Performance is critical
- Frequently changing base tables

## Common Commands
```sql
-- Show all views
SHOW FULL TABLES WHERE Table_type = 'VIEW';

-- View definition
SHOW CREATE VIEW view_name;

-- Replace existing view
CREATE OR REPLACE VIEW view_name AS SELECT...;
```

---
*Quick reference for database views - covers essentials for development and interviews*
