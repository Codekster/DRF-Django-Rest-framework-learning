# MySQL Triggers - Complete Guide

## Table of Contents
1. [Definition](#definition)
2. [Types of Triggers](#types-of-triggers)
3. [Creating Triggers](#creating-triggers)
4. [Trigger Syntax](#trigger-syntax)
5. [Trigger Examples](#trigger-examples)
6. [Use Cases](#use-cases)
7. [Best Practices](#best-practices)
8. [Limitations](#limitations)
9. [Interview Preparation](#interview-preparation)

---

## Definition

A **trigger** in MySQL is a database object that automatically executes in response to specific events on a particular table or view. Triggers are procedural code that are automatically executed in response to certain events on a particular table or view in a database.

### Key Characteristics:
- Triggers are **event-driven**
- They execute **automatically**
- They are associated with specific **tables or views**
- They execute in response to DML operations (INSERT, UPDATE, DELETE)
- They can execute **before** or **after** the triggering event
- They can access and modify database data

### Trigger Terminology:
- **Triggering Statement**: The SQL statement that causes a trigger to execute
- **Trigger Time**: BEFORE or AFTER the triggering statement
- **Trigger Event**: INSERT, UPDATE, or DELETE
- **Trigger Body**: The actions performed when the trigger executes
- **OLD and NEW**: Special references to access column values

---

## Types of Triggers

### Based on Timing:

#### 1. **BEFORE Triggers**
- Execute **before** the triggering statement (INSERT, UPDATE, DELETE)
- Can modify the data being inserted or updated
- Can prevent the operation by signaling an error
- Useful for data validation and preprocessing

#### 2. **AFTER Triggers**
- Execute **after** the triggering statement completes
- Cannot modify the data being inserted or updated
- Cannot prevent the operation (it's already done)
- Useful for logging, auditing, and cascading changes

### Based on Event:

#### 1. **INSERT Triggers**
- Execute when new rows are added to a table
- Can access NEW values (the data being inserted)

#### 2. **UPDATE Triggers**
- Execute when existing rows are modified
- Can access both OLD values (before update) and NEW values (after update)

#### 3. **DELETE Triggers**
- Execute when rows are removed from a table
- Can access OLD values (the data being deleted)

### Total Combinations:
This gives us 6 possible types of triggers:
1. BEFORE INSERT
2. AFTER INSERT
3. BEFORE UPDATE
4. AFTER UPDATE
5. BEFORE DELETE
6. AFTER DELETE

---

## Creating Triggers

### Basic Syntax

```sql
DELIMITER //

CREATE TRIGGER trigger_name
{BEFORE | AFTER} {INSERT | UPDATE | DELETE}
ON table_name
FOR EACH ROW
BEGIN
    -- Trigger body
    -- SQL statements
END //

DELIMITER ;
```

### OLD and NEW References

- **OLD**: Refers to the row before the change (for UPDATE and DELETE)
- **NEW**: Refers to the row after the change (for INSERT and UPDATE)

| Trigger Type | OLD Available | NEW Available |
|--------------|--------------|--------------|
| INSERT       | No           | Yes          |
| UPDATE       | Yes          | Yes          |
| DELETE       | Yes          | No           |

### Dropping a Trigger

```sql
DROP TRIGGER [IF EXISTS] trigger_name;
```

### Showing Triggers

```sql
SHOW TRIGGERS;
SHOW TRIGGERS LIKE 'pattern';
SHOW TRIGGERS FROM database_name;
```

---

## Trigger Syntax

### Full Syntax

```sql
DELIMITER //

CREATE TRIGGER trigger_name
{BEFORE | AFTER} {INSERT | UPDATE | DELETE}
ON table_name
FOR EACH ROW
[trigger_order]
BEGIN
    -- Trigger logic
END //

DELIMITER ;
```

Where:
- **trigger_name**: Unique name for the trigger
- **BEFORE | AFTER**: When the trigger executes
- **INSERT | UPDATE | DELETE**: The triggering event
- **table_name**: The table to which the trigger belongs
- **FOR EACH ROW**: Trigger executes once for each row affected
- **trigger_order** (MySQL 8.0+): FOLLOWS or PRECEDES to define execution order
- **BEGIN...END**: Block containing the trigger logic

### Conditional Logic

```sql
IF condition THEN
    -- Statements
ELSEIF condition THEN
    -- Statements
ELSE
    -- Statements
END IF;
```

### Variables in Triggers

```sql
DECLARE variable_name data_type [DEFAULT default_value];
SET variable_name = value;
```

### Error Handling

```sql
SIGNAL SQLSTATE '45000' 
SET MESSAGE_TEXT = 'Custom error message';
```

---

## Trigger Examples

### Example 1: BEFORE INSERT Trigger (Data Validation)

```sql
-- Create a table for employees
CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    salary DECIMAL(10,2),
    hire_date DATE
);

-- Create a BEFORE INSERT trigger to validate data
DELIMITER //
CREATE TRIGGER before_employee_insert
BEFORE INSERT ON employees
FOR EACH ROW
BEGIN
    -- Validate email format
    IF NEW.email NOT LIKE '%@%.%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid email format';
    END IF;
    
    -- Ensure salary is positive
    IF NEW.salary <= 0 THEN
        SET NEW.salary = 1000.00; -- Default minimum salary
    END IF;
    
    -- Set hire_date to current date if not provided
    IF NEW.hire_date IS NULL THEN
        SET NEW.hire_date = CURDATE();
    END IF;
END //
DELIMITER ;

-- Test the trigger
INSERT INTO employees (first_name, last_name, email, salary) 
VALUES ('John', 'Doe', 'john.doe@company.com', 5000);

-- This will fail due to invalid email
INSERT INTO employees (first_name, last_name, email, salary) 
VALUES ('Jane', 'Smith', 'invalid-email', 4500);

-- This will set default salary and hire date
INSERT INTO employees (first_name, last_name, email, salary) 
VALUES ('Bob', 'Johnson', 'bob.j@company.com', -100);
```

### Example 2: AFTER INSERT Trigger (Audit Log)

```sql
-- Create audit log table
CREATE TABLE employee_audit (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    action_type VARCHAR(10),
    action_date TIMESTAMP,
    action_user VARCHAR(50),
    old_data JSON,
    new_data JSON
);

-- Create AFTER INSERT trigger
DELIMITER //
CREATE TRIGGER after_employee_insert
AFTER INSERT ON employees
FOR EACH ROW
BEGIN
    INSERT INTO employee_audit (
        employee_id, 
        action_type, 
        action_date, 
        action_user,
        old_data,
        new_data
    )
    VALUES (
        NEW.id,
        'INSERT',
        NOW(),
        CURRENT_USER(),
        NULL,
        JSON_OBJECT(
            'first_name', NEW.first_name,
            'last_name', NEW.last_name,
            'email', NEW.email,
            'salary', NEW.salary,
            'hire_date', NEW.hire_date
        )
    );
END //
DELIMITER ;

-- Test the trigger
INSERT INTO employees (first_name, last_name, email, salary) 
VALUES ('Alice', 'Cooper', 'alice@company.com', 6000);

-- Check the audit log
SELECT * FROM employee_audit;
```

### Example 3: BEFORE UPDATE Trigger (Prevent Updates)

```sql
-- Create BEFORE UPDATE trigger
DELIMITER //
CREATE TRIGGER before_employee_update
BEFORE UPDATE ON employees
FOR EACH ROW
BEGIN
    -- Block updates to employee ID
    IF NEW.id != OLD.id THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Employee ID cannot be changed';
    END IF;
    
    -- Validate salary changes
    IF NEW.salary < OLD.salary THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Salary cannot be reduced';
    END IF;
    
    -- Log attempt to change email
    IF NEW.email != OLD.email THEN
        INSERT INTO employee_audit (
            employee_id, action_type, action_date, action_user,
            old_data, new_data
        )
        VALUES (
            OLD.id, 'EMAIL CHANGE', NOW(), CURRENT_USER(),
            JSON_OBJECT('email', OLD.email),
            JSON_OBJECT('email', NEW.email)
        );
    END IF;
END //
DELIMITER ;

-- Test the trigger
UPDATE employees SET salary = 6500 WHERE id = 1; -- This works

UPDATE employees SET salary = 5000 WHERE id = 1; -- This fails
```

### Example 4: AFTER UPDATE Trigger (Sync Related Tables)

```sql
-- Create employee contact table
CREATE TABLE employee_contacts (
    employee_id INT PRIMARY KEY,
    phone VARCHAR(20),
    emergency_contact VARCHAR(100),
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

-- Insert some data
INSERT INTO employee_contacts VALUES (1, '555-1234', 'Sarah Doe');

-- Create AFTER UPDATE trigger
DELIMITER //
CREATE TRIGGER after_employee_update
AFTER UPDATE ON employees
FOR EACH ROW
BEGIN
    -- Update last modified timestamp in contacts
    IF OLD.first_name != NEW.first_name OR OLD.last_name != NEW.last_name THEN
        UPDATE employee_contacts
        SET emergency_contact = CONCAT('Contact ', NEW.first_name, ' ', NEW.last_name)
        WHERE employee_id = NEW.id AND emergency_contact LIKE CONCAT('Contact ', OLD.first_name, '%');
    END IF;
END //
DELIMITER ;

-- Test the trigger
UPDATE employees SET first_name = 'Jonathan', last_name = 'Doe' WHERE id = 1;

-- Check employee_contacts
SELECT * FROM employee_contacts WHERE employee_id = 1;
```

### Example 5: BEFORE DELETE Trigger (Prevent Deletion)

```sql
-- Create BEFORE DELETE trigger
DELIMITER //
CREATE TRIGGER before_employee_delete
BEFORE DELETE ON employees
FOR EACH ROW
BEGIN
    -- Check if employee has contacts
    IF EXISTS (SELECT 1 FROM employee_contacts WHERE employee_id = OLD.id) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot delete employee with contacts. Remove contacts first.';
    END IF;
END //
DELIMITER ;

-- Test the trigger
DELETE FROM employees WHERE id = 1; -- This fails

-- Delete contacts first, then employee
DELETE FROM employee_contacts WHERE employee_id = 1;
DELETE FROM employees WHERE id = 1; -- This works
```

### Example 6: AFTER DELETE Trigger (Cascading Delete)

```sql
-- Create AFTER DELETE trigger
DELIMITER //
CREATE TRIGGER after_employee_delete
AFTER DELETE ON employees
FOR EACH ROW
BEGIN
    -- Log deletion in audit table
    INSERT INTO employee_audit (
        employee_id, 
        action_type, 
        action_date, 
        action_user,
        old_data,
        new_data
    )
    VALUES (
        OLD.id,
        'DELETE',
        NOW(),
        CURRENT_USER(),
        JSON_OBJECT(
            'first_name', OLD.first_name,
            'last_name', OLD.last_name,
            'email', OLD.email,
            'salary', OLD.salary
        ),
        NULL
    );
END //
DELIMITER ;

-- Test the trigger
INSERT INTO employees (first_name, last_name, email, salary) 
VALUES ('Test', 'User', 'test@example.com', 3000);

SET @last_id = LAST_INSERT_ID();

DELETE FROM employees WHERE id = @last_id;

-- Check the audit log
SELECT * FROM employee_audit WHERE action_type = 'DELETE';
```

---

## Use Cases

### 1. **Data Validation and Integrity**
- Enforce complex business rules beyond simple constraints
- Format data consistently (e.g., capitalize names, standardize phone numbers)
- Perform cross-field validations
- Ensure referential integrity beyond foreign keys

### 2. **Auditing and Logging**
- Track all changes to sensitive data
- Record who made changes and when
- Maintain history of data changes
- Create comprehensive audit trails

### 3. **Automated Calculations**
- Calculate derived fields automatically
- Maintain running totals or averages
- Update timestamps and version numbers
- Compute complex values based on multiple fields

### 4. **Synchronizing Data**
- Keep redundant data in sync across tables
- Propagate changes to related tables
- Implement custom cascading updates
- Maintain denormalized data for reporting

### 5. **Security Enforcement**
- Prevent unauthorized modifications
- Implement time-based restrictions
- Add additional security checks
- Enforce complex access rules

### 6. **Notification Systems**
- Record events for notification processing
- Queue messages for external systems
- Log activities for later processing
- Implement event-driven architectures

### 7. **Business Workflow**
- Implement state transitions
- Enforce process sequences
- Automate next steps in business processes
- Track progress through multi-step procedures

---

## Best Practices

### 1. **Keep Triggers Simple**
- Focus on one task per trigger
- Avoid complex logic when possible
- Use stored procedures for complex operations

### 2. **Document Thoroughly**
- Comment trigger code extensively
- Maintain documentation of all triggers
- Explain business rules implemented

### 3. **Error Handling**
- Implement proper error handling
- Use descriptive error messages
- Log errors for troubleshooting

### 4. **Performance Considerations**
- Minimize database operations in triggers
- Avoid recursive trigger chains
- Be cautious with triggers on frequently updated tables

### 5. **Testing**
- Test all possible scenarios
- Verify both positive and negative cases
- Test with bulk operations

### 6. **Naming Conventions**
- Use descriptive names
- Include trigger timing and event in name
- Follow consistent naming standards

---

## Limitations

### 1. **No Access to Session Variables**
- Triggers cannot access session variables like `@variables`

### 2. **Limited Transaction Control**
- Cannot use COMMIT or ROLLBACK within triggers

### 3. **No Dynamic SQL**
- Cannot use PREPARE statements

### 4. **Recursion Limits**
- Limited recursive trigger execution

### 5. **No Multiple Triggers of Same Type**
- In MySQL before 8.0, only one trigger of each type per table
- MySQL 8.0+ allows multiple triggers with ordering

### 6. **No Triggers on Views**
- Triggers can only be defined on tables

### 7. **No Returns or Parameters**
- Triggers cannot return values or accept parameters

---

## Interview Preparation

### Common Interview Questions

#### Q1: What is a trigger in MySQL?
**Answer:** A trigger is a database object that automatically executes when a specified event (INSERT, UPDATE, DELETE) occurs on a particular table. Triggers can execute before or after these events and can perform actions like validating data, updating related tables, or logging changes.

#### Q2: What are the different types of triggers in MySQL?
**Answer:** MySQL supports six types of triggers:
1. BEFORE INSERT
2. AFTER INSERT
3. BEFORE UPDATE
4. AFTER UPDATE
5. BEFORE DELETE
6. AFTER DELETE

#### Q3: What is the difference between BEFORE and AFTER triggers?
**Answer:**
- **BEFORE triggers** execute before the actual DML operation and can modify the data being inserted or updated. They can also prevent the operation by raising errors.
- **AFTER triggers** execute after the DML operation completes and cannot modify the data being affected by the triggering statement. They are useful for logging or updating related tables.

#### Q4: How can you access the data that triggered the trigger?
**Answer:** MySQL provides special references:
- **OLD**: Contains the row data before the change (available in UPDATE and DELETE triggers)
- **NEW**: Contains the row data after the change (available in INSERT and UPDATE triggers)

#### Q5: Can a trigger call itself recursively?
**Answer:** Yes, triggers can be recursive, but MySQL limits recursion to prevent infinite loops. The maximum recursion depth is controlled by the `max_sp_recursion_depth` system variable.

#### Q6: What happens if a trigger raises an error?
**Answer:** If a trigger raises an error (using SIGNAL), the entire transaction is rolled back, including the triggering statement. This means the original data modification that triggered the trigger will not take place.

#### Q7: Can you have multiple triggers of the same type on a table?
**Answer:** In MySQL 8.0 and later, yes. You can have multiple triggers of the same type (e.g., multiple BEFORE INSERT triggers) on a table. You can control their order using the FOLLOWS and PRECEDES clauses. In MySQL 5.7 and earlier, only one trigger of each type was allowed per table.

#### Q8: What are the limitations of MySQL triggers?
**Answer:** Some key limitations include:
- Cannot use COMMIT or ROLLBACK statements
- Cannot use dynamic SQL (PREPARE statements)
- Cannot access session variables
- Cannot return values
- Cannot create temporary tables with the same name twice
- Cannot use statements that explicitly or implicitly begin/end transactions

#### Q9: How do you debug triggers in MySQL?
**Answer:** Debugging triggers can be done by:
- Creating logging tables to record trigger execution
- Using user-defined variables to track execution flow
- Implementing error handling with detailed messages
- Using the general query log for tracking execution
- Testing triggers with different data scenarios

#### Q10: What is the difference between triggers and stored procedures?
**Answer:**
| Triggers | Stored Procedures |
|----------|-------------------|
| Execute automatically on events | Execute when explicitly called |
| No parameters | Can accept parameters |
| Associated with tables | Not associated with specific tables |
| Cannot be called directly | Can be called directly |
| No return values | Can return values |
| Used for data integrity/consistency | Used for business logic/operations |

#### Q11: How would you implement an audit log using triggers?
**Answer:** I'd create an audit table with columns for the primary key, action type (INSERT/UPDATE/DELETE), timestamp, user, and old/new values. Then I'd create AFTER triggers for each action type that would insert the relevant data into the audit table. For example:

```sql
CREATE TRIGGER after_table_update
AFTER UPDATE ON main_table
FOR EACH ROW
INSERT INTO audit_log 
VALUES (NULL, NEW.id, 'UPDATE', NOW(), CURRENT_USER(), 
        JSON_OBJECT('old', OLD.column, 'new', NEW.column));
```

#### Q12: How can triggers impact performance?
**Answer:** Triggers can impact performance by:
- Adding overhead to DML operations
- Creating cascading effects if multiple tables have triggers
- Causing contention on frequently accessed tables
- Performing expensive operations on every row change
- Creating deep recursion chains
- Adding complexity to transaction processing

### Practical Interview Scenarios

#### Scenario 1: Implement a trigger to enforce business hours
**Problem:** Create a trigger that prevents updates to the `orders` table outside of business hours (9 AM to 5 PM, Monday to Friday).

**Solution:**
```sql
DELIMITER //
CREATE TRIGGER enforce_business_hours
BEFORE UPDATE ON orders
FOR EACH ROW
BEGIN
    DECLARE current_day INT;
    DECLARE current_hour INT;
    
    SET current_day = DAYOFWEEK(NOW()); -- 1=Sunday, 2=Monday, ..., 7=Saturday
    SET current_hour = HOUR(NOW());
    
    IF (current_day = 1 OR current_day = 7 OR 
        current_hour < 9 OR current_hour >= 17) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Updates are only allowed during business hours (9 AM - 5 PM, Mon-Fri)';
    END IF;
END //
DELIMITER ;
```

#### Scenario 2: Create a system for maintaining aggregate totals
**Problem:** Create triggers to maintain a running total of order amounts by customer.

**Solution:**
```sql
-- First create necessary tables
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    amount DECIMAL(10,2),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE customer_totals (
    customer_id INT PRIMARY KEY,
    total_orders INT DEFAULT 0,
    total_amount DECIMAL(12,2) DEFAULT 0.00
);

-- Create triggers
DELIMITER //

-- After insert trigger
CREATE TRIGGER update_customer_totals_insert
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    INSERT INTO customer_totals (customer_id, total_orders, total_amount)
    VALUES (NEW.customer_id, 1, NEW.amount)
    ON DUPLICATE KEY UPDATE
        total_orders = total_orders + 1,
        total_amount = total_amount + NEW.amount;
END //

-- After update trigger
CREATE TRIGGER update_customer_totals_update
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
    IF OLD.customer_id = NEW.customer_id THEN
        -- Same customer, just update amount
        UPDATE customer_totals
        SET total_amount = total_amount - OLD.amount + NEW.amount
        WHERE customer_id = NEW.customer_id;
    ELSE
        -- Customer changed, update both records
        UPDATE customer_totals
        SET total_orders = total_orders - 1,
            total_amount = total_amount - OLD.amount
        WHERE customer_id = OLD.customer_id;
        
        INSERT INTO customer_totals (customer_id, total_orders, total_amount)
        VALUES (NEW.customer_id, 1, NEW.amount)
        ON DUPLICATE KEY UPDATE
            total_orders = total_orders + 1,
            total_amount = total_amount + NEW.amount;
    END IF;
END //

-- After delete trigger
CREATE TRIGGER update_customer_totals_delete
AFTER DELETE ON orders
FOR EACH ROW
BEGIN
    UPDATE customer_totals
    SET total_orders = total_orders - 1,
        total_amount = total_amount - OLD.amount
    WHERE customer_id = OLD.customer_id;
    
    -- Optional: Remove customer if no more orders
    DELETE FROM customer_totals 
    WHERE customer_id = OLD.customer_id AND total_orders = 0;
END //

DELIMITER ;
```

#### Scenario 3: Implement data validation trigger
**Problem:** Create a trigger to validate that product prices are never reduced by more than 25% in a single update.

**Solution:**
```sql
DELIMITER //
CREATE TRIGGER validate_price_change
BEFORE UPDATE ON products
FOR EACH ROW
BEGIN
    DECLARE max_reduction DECIMAL(10,2);
    
    IF NEW.price < OLD.price THEN
        SET max_reduction = OLD.price * 0.75; -- 25% reduction limit
        
        IF NEW.price < max_reduction THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Price cannot be reduced by more than 25% in a single update';
        END IF;
    END IF;
END //
DELIMITER ;
```

### Key Points to Remember for Interviews

1. **Know the types of triggers** (BEFORE/AFTER and INSERT/UPDATE/DELETE)
2. **Understand the OLD and NEW references** and when they're available
3. **Be aware of trigger limitations** in MySQL
4. **Have examples ready** for common use cases
5. **Know best practices** for performance and maintainability
6. **Understand the relationship** between triggers and transactions
7. **Be able to explain** when to use triggers versus other database objects
8. **Mention security implications** of using triggers
9. **Know how to debug and troubleshoot** trigger issues
10. **Describe how to prevent recursive trigger loops**

---

*This guide covers MySQL triggers from basic concepts to advanced usage and interview preparation. Practice these examples to master trigger development.*
