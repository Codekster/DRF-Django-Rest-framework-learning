# MySQL Stored Procedures - Complete Guide

## Table of Contents
1. [Basic Introduction](#basic-introduction)
2. [What is a Stored Procedure?](#what-is-a-stored-procedure)
3. [Why Use Stored Procedures?](#why-use-stored-procedures)
4. [Basic Syntax](#basic-syntax)
5. [Parameters](#parameters)
6. [Variables](#variables)
7. [Control Flow](#control-flow)
8. [Examples](#examples)
9. [Advanced Features](#advanced-features)
10. [Best Practices](#best-practices)
11. [Interview Preparation](#interview-preparation)

---

## Basic Introduction

A **Stored Procedure** in MySQL is a prepared SQL code that you can save and reuse. It's a collection of SQL statements that can be executed as a single unit. Think of it as a function in programming languages but for database operations.

### Key Points:
- Stored procedures are precompiled and stored in the database
- They can accept parameters and return results
- They improve performance and security
- They allow complex business logic to be centralized in the database

---

## What is a Stored Procedure?

A stored procedure is a group of SQL statements that form a logical unit and perform a particular task. They are stored in the MySQL database and can be invoked by triggers, other stored procedures, or applications.

### Characteristics:
- **Precompiled**: Parsed and optimized when created
- **Reusable**: Can be called multiple times
- **Parameterized**: Can accept input and output parameters
- **Secure**: Helps prevent SQL injection
- **Centralized**: Business logic stored in database

---

## Why Use Stored Procedures?

### 1. **Performance**
- Precompiled and cached
- Reduced network traffic
- Faster execution for complex operations

### 2. **Security**
- Prevents SQL injection attacks
- Controlled data access
- User permissions can be granted on procedures

### 3. **Code Reusability**
- Write once, use multiple times
- Consistent business logic
- Easier maintenance

### 4. **Reduced Network Traffic**
- Single call executes multiple statements
- Only results are sent over network
- Efficient for complex operations

### 5. **Centralized Business Logic**
- Database enforces business rules
- Consistent across all applications
- Easier to modify logic

### 6. **Transaction Control**
- Built-in transaction management
- Better error handling
- Atomicity of operations

---

## Basic Syntax

### Creating a Stored Procedure

```sql
DELIMITER //

CREATE PROCEDURE procedure_name (
    [IN | OUT | INOUT] parameter_name data_type,
    ...
)
BEGIN
    -- SQL statements
    -- Business logic
END //

DELIMITER ;
```

### Calling a Stored Procedure

```sql
CALL procedure_name(parameter1, parameter2, ...);
```

### Dropping a Stored Procedure

```sql
DROP PROCEDURE IF EXISTS procedure_name;
```

### Showing Stored Procedures

```sql
SHOW PROCEDURE STATUS;
SHOW PROCEDURE STATUS WHERE Db = 'database_name';
SHOW CREATE PROCEDURE procedure_name;
```

---

## Parameters

### Parameter Types

#### 1. **IN Parameters** (Default)
- Input parameters
- Values passed to the procedure
- Cannot be modified within procedure

#### 2. **OUT Parameters**
- Output parameters
- Used to return values from procedure
- Initial value is ignored

#### 3. **INOUT Parameters**
- Both input and output
- Can be modified within procedure
- Initial value is used

### Parameter Examples

```sql
-- IN Parameter Example
DELIMITER //
CREATE PROCEDURE GetEmployeeById(IN emp_id INT)
BEGIN
    SELECT * FROM employees WHERE employee_id = emp_id;
END //
DELIMITER ;

-- OUT Parameter Example
DELIMITER //
CREATE PROCEDURE GetEmployeeCount(OUT emp_count INT)
BEGIN
    SELECT COUNT(*) INTO emp_count FROM employees;
END //
DELIMITER ;

-- INOUT Parameter Example
DELIMITER //
CREATE PROCEDURE DoubleValue(INOUT value INT)
BEGIN
    SET value = value * 2;
END //
DELIMITER ;
```

---

## Variables

### Declaring Variables

```sql
DECLARE variable_name data_type [DEFAULT value];
```

### Variable Examples

```sql
DELIMITER //
CREATE PROCEDURE VariableExample()
BEGIN
    -- Declare variables
    DECLARE emp_count INT DEFAULT 0;
    DECLARE avg_salary DECIMAL(10,2);
    DECLARE dept_name VARCHAR(50);
    
    -- Use variables
    SELECT COUNT(*) INTO emp_count FROM employees;
    SELECT AVG(salary) INTO avg_salary FROM employees;
    
    SELECT emp_count, avg_salary;
END //
DELIMITER ;
```

---

## Control Flow

### 1. **IF-THEN-ELSE**

```sql
IF condition THEN
    statements;
ELSEIF condition THEN
    statements;
ELSE
    statements;
END IF;
```

### 2. **CASE Statement**

```sql
CASE case_value
    WHEN when_value THEN statements;
    WHEN when_value THEN statements;
    ELSE statements;
END CASE;
```

### 3. **WHILE Loop**

```sql
WHILE condition DO
    statements;
END WHILE;
```

### 4. **REPEAT Loop**

```sql
REPEAT
    statements;
UNTIL condition
END REPEAT;
```

### 5. **FOR Loop** (MySQL 8.0+)

```sql
FOR counter IN start_value..end_value DO
    statements;
END FOR;
```

---

## Examples

### Example 1: Simple Stored Procedure

```sql
-- Create a simple procedure to get employee details
DELIMITER //
CREATE PROCEDURE GetEmployeeDetails(IN emp_id INT)
BEGIN
    SELECT 
        employee_id,
        first_name,
        last_name,
        department,
        salary
    FROM employees 
    WHERE employee_id = emp_id;
END //
DELIMITER ;

-- Call the procedure
CALL GetEmployeeDetails(101);
```

### Example 2: Procedure with Multiple Parameters

```sql
-- Create procedure to add new employee
DELIMITER //
CREATE PROCEDURE AddEmployee(
    IN p_first_name VARCHAR(50),
    IN p_last_name VARCHAR(50),
    IN p_department VARCHAR(50),
    IN p_salary DECIMAL(10,2),
    OUT p_employee_id INT
)
BEGIN
    INSERT INTO employees (first_name, last_name, department, salary)
    VALUES (p_first_name, p_last_name, p_department, p_salary);
    
    SET p_employee_id = LAST_INSERT_ID();
END //
DELIMITER ;

-- Call the procedure
CALL AddEmployee('John', 'Doe', 'IT', 75000, @new_emp_id);
SELECT @new_emp_id;
```

### Example 3: Procedure with Control Flow

```sql
-- Procedure to calculate bonus based on performance
DELIMITER //
CREATE PROCEDURE CalculateBonus(
    IN emp_id INT,
    IN performance_rating INT,
    OUT bonus_amount DECIMAL(10,2)
)
BEGIN
    DECLARE current_salary DECIMAL(10,2);
    
    -- Get current salary
    SELECT salary INTO current_salary 
    FROM employees 
    WHERE employee_id = emp_id;
    
    -- Calculate bonus based on rating
    IF performance_rating >= 9 THEN
        SET bonus_amount = current_salary * 0.20;  -- 20% bonus
    ELSEIF performance_rating >= 7 THEN
        SET bonus_amount = current_salary * 0.15;  -- 15% bonus
    ELSEIF performance_rating >= 5 THEN
        SET bonus_amount = current_salary * 0.10;  -- 10% bonus
    ELSE
        SET bonus_amount = 0;  -- No bonus
    END IF;
END //
DELIMITER ;

-- Call the procedure
CALL CalculateBonus(101, 8, @bonus);
SELECT @bonus;
```

### Example 4: Procedure with Loop

```sql
-- Procedure to update salaries for all employees in a department
DELIMITER //
CREATE PROCEDURE UpdateDepartmentSalaries(
    IN dept_name VARCHAR(50),
    IN percentage_increase DECIMAL(5,2)
)
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE emp_id INT;
    DECLARE current_salary DECIMAL(10,2);
    
    -- Cursor to iterate through employees
    DECLARE emp_cursor CURSOR FOR 
        SELECT employee_id, salary 
        FROM employees 
        WHERE department = dept_name;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN emp_cursor;
    
    read_loop: LOOP
        FETCH emp_cursor INTO emp_id, current_salary;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- Update salary
        UPDATE employees 
        SET salary = salary * (1 + percentage_increase/100)
        WHERE employee_id = emp_id;
    END LOOP;
    
    CLOSE emp_cursor;
END //
DELIMITER ;

-- Call the procedure
CALL UpdateDepartmentSalaries('IT', 10.0);  -- 10% increase
```

### Example 5: Error Handling

```sql
-- Procedure with error handling
DELIMITER //
CREATE PROCEDURE SafeAddEmployee(
    IN p_first_name VARCHAR(50),
    IN p_last_name VARCHAR(50),
    IN p_email VARCHAR(100),
    IN p_department VARCHAR(50),
    OUT p_result VARCHAR(100)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_result = 'Error: Employee could not be added';
    END;
    
    START TRANSACTION;
    
    -- Check if email already exists
    IF EXISTS (SELECT 1 FROM employees WHERE email = p_email) THEN
        SET p_result = 'Error: Email already exists';
        ROLLBACK;
    ELSE
        INSERT INTO employees (first_name, last_name, email, department)
        VALUES (p_first_name, p_last_name, p_email, p_department);
        
        COMMIT;
        SET p_result = 'Success: Employee added successfully';
    END IF;
END //
DELIMITER ;

-- Call the procedure
CALL SafeAddEmployee('Jane', 'Smith', 'jane.smith@company.com', 'HR', @result);
SELECT @result;
```

---

## Advanced Features

### 1. **Cursors**

```sql
DELIMITER //
CREATE PROCEDURE ProcessEmployees()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE emp_name VARCHAR(100);
    DECLARE emp_salary DECIMAL(10,2);
    
    DECLARE emp_cursor CURSOR FOR 
        SELECT CONCAT(first_name, ' ', last_name), salary 
        FROM employees;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN emp_cursor;
    
    read_loop: LOOP
        FETCH emp_cursor INTO emp_name, emp_salary;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- Process each employee
        SELECT emp_name, emp_salary;
    END LOOP;
    
    CLOSE emp_cursor;
END //
DELIMITER ;
```

### 2. **Exception Handling**

```sql
DELIMITER //
CREATE PROCEDURE HandleErrors()
BEGIN
    DECLARE CONTINUE HANDLER FOR SQLWARNING
    BEGIN
        SELECT 'Warning occurred' AS message;
    END;
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SELECT 'Error occurred' AS message;
        ROLLBACK;
    END;
    
    START TRANSACTION;
    
    -- Your SQL operations here
    
    COMMIT;
END //
DELIMITER ;
```

### 3. **Dynamic SQL**

```sql
DELIMITER //
CREATE PROCEDURE DynamicQuery(IN table_name VARCHAR(64))
BEGIN
    SET @sql = CONCAT('SELECT COUNT(*) FROM ', table_name);
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;
```

---

## Best Practices

### 1. **Naming Conventions**
- Use descriptive names
- Prefix with `sp_` or `proc_`
- Use consistent naming style

### 2. **Parameter Handling**
- Always specify parameter direction (IN, OUT, INOUT)
- Validate input parameters
- Use meaningful parameter names

### 3. **Error Handling**
- Always include error handling
- Use transactions for data modifications
- Provide meaningful error messages

### 4. **Performance**
- Avoid cursors when possible (use set-based operations)
- Use appropriate indexes
- Keep procedures simple and focused

### 5. **Security**
- Validate all inputs
- Use parameterized queries
- Grant minimal required permissions

### 6. **Documentation**
- Comment complex logic
- Document parameters and return values
- Include examples of usage

---

## Interview Preparation

### Common Interview Questions

#### Q1: What is a Stored Procedure?
**Answer:** A stored procedure is a precompiled collection of SQL statements stored in the database that can be executed as a single unit. It can accept parameters, perform complex operations, and return results.

#### Q2: What are the advantages of Stored Procedures?
**Answer:**
- **Performance**: Precompiled and cached
- **Security**: Prevents SQL injection
- **Reusability**: Write once, use multiple times
- **Reduced Network Traffic**: Single call for multiple operations
- **Centralized Logic**: Business rules in database

#### Q3: What are the types of parameters in MySQL stored procedures?
**Answer:**
- **IN**: Input parameters (default)
- **OUT**: Output parameters for returning values
- **INOUT**: Both input and output parameters

#### Q4: How do you handle errors in stored procedures?
**Answer:**
```sql
DECLARE EXIT HANDLER FOR SQLEXCEPTION
BEGIN
    ROLLBACK;
    SELECT 'Error occurred' AS message;
END;
```

#### Q5: What is the difference between Stored Procedure and Function?
**Answer:**
| Stored Procedure | Function |
|------------------|----------|
| Can have 0 or more return values | Must return exactly one value |
| Can use OUT parameters | Cannot use OUT parameters |
| Can call functions | Cannot call procedures |
| Can contain transactions | Cannot contain transactions |
| Called with CALL statement | Called in SELECT statements |

#### Q6: How do you create a cursor in MySQL?
**Answer:**
```sql
DECLARE cursor_name CURSOR FOR select_statement;
OPEN cursor_name;
FETCH cursor_name INTO variables;
CLOSE cursor_name;
```

#### Q7: What is DELIMITER in MySQL stored procedures?
**Answer:** DELIMITER changes the statement delimiter from semicolon (;) to another character (usually //) so that the procedure definition can contain semicolons without ending the CREATE PROCEDURE statement prematurely.

#### Q8: Can stored procedures be recursive in MySQL?
**Answer:** Yes, MySQL supports recursive stored procedures, but you need to set the `max_sp_recursion_depth` system variable to control the maximum recursion depth.

#### Q9: How do you debug stored procedures in MySQL?
**Answer:**
- Use SELECT statements to output intermediate values
- Use temporary tables to store debug information
- Use MySQL Workbench debugger (if available)
- Add logging to tables for debugging

#### Q10: What are the limitations of MySQL stored procedures?
**Answer:**
- Limited debugging capabilities
- Database-specific (not portable)
- Can make application logic harder to version control
- May create performance bottlenecks if overused
- Limited error handling compared to application code

### Practice Scenarios

#### Scenario 1: E-commerce Order Processing
Create procedures for:
- Adding new orders
- Calculating order totals
- Processing payments
- Updating inventory

#### Scenario 2: Employee Management System
Create procedures for:
- Employee CRUD operations
- Salary calculations
- Department transfers
- Performance evaluations

#### Scenario 3: Banking System
Create procedures for:
- Account transactions
- Balance inquiries
- Interest calculations
- Loan processing

### Key Points for Interviews

1. **Understand the basic syntax and parameter types**
2. **Know error handling techniques**
3. **Be familiar with control flow statements**
4. **Understand performance implications**
5. **Know when to use procedures vs functions**
6. **Be aware of security benefits**

---

## Common Commands Reference

```sql
-- Create procedure
CREATE PROCEDURE name() BEGIN ... END;

-- Call procedure
CALL procedure_name(params);

-- Drop procedure
DROP PROCEDURE procedure_name;

-- Show procedures
SHOW PROCEDURE STATUS;
SHOW CREATE PROCEDURE procedure_name;

-- Show procedure code
SELECT ROUTINE_DEFINITION 
FROM INFORMATION_SCHEMA.ROUTINES 
WHERE ROUTINE_NAME = 'procedure_name';
```

---

*This guide covers MySQL stored procedures from basic concepts to advanced features. Practice with real scenarios to master stored procedure development.*
