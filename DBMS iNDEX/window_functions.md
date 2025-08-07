# Window Functions in SQL

## Table of Contents
1. [Introduction](#introduction)
2. [Basic Syntax](#basic-syntax)
3. [Window Function Components](#window-function-components)
4. [Types of Window Functions](#types-of-window-functions)
5. [Ranking Functions](#ranking-functions)
6. [Aggregate Window Functions](#aggregate-window-functions)
7. [Analytic Functions](#analytic-functions)
8. [Practical Examples](#practical-examples)
9. [Performance Considerations](#performance-considerations)
10. [Common Use Cases](#common-use-cases)

---

## Introduction

Window functions perform calculations across a set of table rows that are related to the current row. Unlike aggregate functions that return a single value for a group of rows, window functions return a value for each row while maintaining access to details of individual rows.

### Key Benefits:
- Perform calculations without GROUP BY
- Access both aggregate and detail data simultaneously
- No need for self-joins or subqueries in many cases
- More readable and maintainable code

---

## Basic Syntax

```sql
SELECT 
    column1,
    column2,
    WINDOW_FUNCTION() OVER (
        [PARTITION BY column(s)]
        [ORDER BY column(s)]
        [ROWS/RANGE frame_specification]
    ) AS alias
FROM table_name;
```

### Components Breakdown:
- **WINDOW_FUNCTION()**: The function to apply
- **OVER()**: Defines the window specification
- **PARTITION BY**: Divides rows into groups (optional)
- **ORDER BY**: Orders rows within each partition (optional)
- **Frame**: Defines subset of rows for calculation (optional)

---

## Window Function Components

### 1. PARTITION BY Clause
Divides the result set into partitions. Window function is applied separately to each partition.

```sql
-- Example: Calculate running total by department
SELECT 
    employee_id,
    department_id,
    salary,
    SUM(salary) OVER (PARTITION BY department_id ORDER BY employee_id) as running_total
FROM employees;
```

### 2. ORDER BY Clause
Specifies the order of rows within each partition. Required for some functions like ROW_NUMBER(), RANK().

```sql
-- Example: Rank employees by salary within department
SELECT 
    employee_id,
    department_id,
    salary,
    RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) as salary_rank
FROM employees;
```

### 3. Frame Specification
Defines which rows to include in the calculation relative to the current row.

#### Frame Types:
- **ROWS**: Physical number of rows
- **RANGE**: Logical range of values

#### Frame Bounds:
- `UNBOUNDED PRECEDING`: From start of partition
- `UNBOUNDED FOLLOWING`: To end of partition
- `CURRENT ROW`: Current row only
- `n PRECEDING`: n rows before current
- `n FOLLOWING`: n rows after current

```sql
-- Examples of frame specifications
SELECT 
    date,
    sales,
    -- Moving average of last 3 days including current
    AVG(sales) OVER (ORDER BY date ROWS 2 PRECEDING) as moving_avg_3days,
    
    -- Running total from start
    SUM(sales) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING) as running_total,
    
    -- Centered moving average (1 before, current, 1 after)
    AVG(sales) OVER (ORDER BY date ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) as centered_avg
FROM daily_sales;
```

---

## Types of Window Functions

### 1. Ranking Functions
- `ROW_NUMBER()`: Unique sequential number
- `RANK()`: Rank with gaps for ties
- `DENSE_RANK()`: Rank without gaps
- `NTILE(n)`: Divides into n buckets

### 2. Aggregate Functions
- `SUM()`, `AVG()`, `COUNT()`, `MIN()`, `MAX()`
- `STDDEV()`, `VARIANCE()`

### 3. Analytic Functions
- `LAG()`, `LEAD()`: Access previous/next row
- `FIRST_VALUE()`, `LAST_VALUE()`: First/last value in frame
- `NTH_VALUE()`: nth value in frame
- `PERCENT_RANK()`, `CUME_DIST()`: Statistical functions

---

## Ranking Functions

### ROW_NUMBER()
Assigns unique sequential numbers to rows.

```sql
-- Assign unique numbers to all employees
SELECT 
    employee_id,
    name,
    salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) as row_num
FROM employees;

-- Reset numbering for each department
SELECT 
    employee_id,
    name,
    department_id,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) as dept_row_num
FROM employees;
```

### RANK() and DENSE_RANK()

```sql
-- RANK() leaves gaps for ties
SELECT 
    name,
    salary,
    RANK() OVER (ORDER BY salary DESC) as rank_with_gaps,
    DENSE_RANK() OVER (ORDER BY salary DESC) as rank_no_gaps
FROM employees;

-- Results might look like:
-- name     salary   rank_with_gaps   rank_no_gaps
-- John     5000     1                1
-- Jane     4500     2                2
-- Bob      4500     2                2
-- Alice    4000     4                3  <- Note the difference
```

### NTILE()
Divides rows into approximately equal groups.

```sql
-- Divide employees into salary quartiles
SELECT 
    name,
    salary,
    NTILE(4) OVER (ORDER BY salary) as salary_quartile
FROM employees;

-- Divide into performance buckets by department
SELECT 
    name,
    department_id,
    performance_score,
    NTILE(3) OVER (PARTITION BY department_id ORDER BY performance_score DESC) as performance_bucket
FROM employees;
```

---

## Aggregate Window Functions

### Running Totals and Cumulative Calculations

```sql
-- Running total of sales
SELECT 
    date,
    daily_sales,
    SUM(daily_sales) OVER (ORDER BY date) as running_total,
    AVG(daily_sales) OVER (ORDER BY date) as running_average
FROM sales_data;

-- Monthly running totals (reset each month)
SELECT 
    date,
    daily_sales,
    SUM(daily_sales) OVER (
        PARTITION BY YEAR(date), MONTH(date) 
        ORDER BY date
    ) as monthly_running_total
FROM sales_data;
```

### Moving Averages

```sql
-- 7-day moving average
SELECT 
    date,
    sales,
    AVG(sales) OVER (
        ORDER BY date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as moving_avg_7days
FROM daily_sales;

-- Centered 5-day moving average
SELECT 
    date,
    sales,
    AVG(sales) OVER (
        ORDER BY date 
        ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
    ) as centered_avg_5days
FROM daily_sales;
```

---

## Analytic Functions

### LAG() and LEAD()
Access values from previous or next rows.

```sql
-- Compare current month sales with previous month
SELECT 
    month,
    sales,
    LAG(sales, 1) OVER (ORDER BY month) as previous_month_sales,
    LEAD(sales, 1) OVER (ORDER BY month) as next_month_sales,
    sales - LAG(sales, 1) OVER (ORDER BY month) as month_over_month_change
FROM monthly_sales;

-- Compare with same month last year
SELECT 
    year,
    month,
    sales,
    LAG(sales, 12) OVER (ORDER BY year, month) as same_month_last_year,
    ((sales - LAG(sales, 12) OVER (ORDER BY year, month)) / 
     LAG(sales, 12) OVER (ORDER BY year, month)) * 100 as year_over_year_pct
FROM monthly_sales;
```

### FIRST_VALUE() and LAST_VALUE()

```sql
-- Compare each employee's salary to highest and lowest in department
SELECT 
    name,
    department_id,
    salary,
    FIRST_VALUE(salary) OVER (
        PARTITION BY department_id 
        ORDER BY salary DESC
        ROWS UNBOUNDED PRECEDING
    ) as highest_salary_in_dept,
    LAST_VALUE(salary) OVER (
        PARTITION BY department_id 
        ORDER BY salary DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as lowest_salary_in_dept
FROM employees;
```

### NTH_VALUE()

```sql
-- Get the 2nd highest salary in each department
SELECT 
    name,
    department_id,
    salary,
    NTH_VALUE(salary, 2) OVER (
        PARTITION BY department_id 
        ORDER BY salary DESC
        ROWS UNBOUNDED PRECEDING
    ) as second_highest_salary
FROM employees;
```

---

## Practical Examples

### Example 1: Top N Records per Group

```sql
-- Get top 3 highest paid employees in each department
WITH ranked_employees AS (
    SELECT 
        employee_id,
        name,
        department_id,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) as rn
    FROM employees
)
SELECT employee_id, name, department_id, salary
FROM ranked_employees
WHERE rn <= 3;
```

### Example 2: Running Statistics

```sql
-- Calculate running statistics for stock prices
SELECT 
    date,
    stock_price,
    AVG(stock_price) OVER (ORDER BY date ROWS 19 PRECEDING) as moving_avg_20day,
    MIN(stock_price) OVER (ORDER BY date ROWS 19 PRECEDING) as min_20day,
    MAX(stock_price) OVER (ORDER BY date ROWS 19 PRECEDING) as max_20day,
    STDDEV(stock_price) OVER (ORDER BY date ROWS 19 PRECEDING) as volatility_20day
FROM stock_data
ORDER BY date;
```

### Example 3: Gap and Island Analysis

```sql
-- Find consecutive sequences of days with sales > 1000
WITH daily_status AS (
    SELECT 
        date,
        sales,
        CASE WHEN sales > 1000 THEN 1 ELSE 0 END as high_sales_day,
        ROW_NUMBER() OVER (ORDER BY date) as rn
    FROM daily_sales
),
gap_analysis AS (
    SELECT 
        date,
        sales,
        high_sales_day,
        ROW_NUMBER() OVER (ORDER BY date) - 
        ROW_NUMBER() OVER (PARTITION BY high_sales_day ORDER BY date) as grp
    FROM daily_status
    WHERE high_sales_day = 1
)
SELECT 
    MIN(date) as streak_start,
    MAX(date) as streak_end,
    COUNT(*) as streak_length
FROM gap_analysis
GROUP BY grp
ORDER BY streak_start;
```

### Example 4: Percentage of Total

```sql
-- Calculate each product's contribution to monthly sales
SELECT 
    month,
    product,
    sales,
    SUM(sales) OVER (PARTITION BY month) as total_monthly_sales,
    ROUND(sales * 100.0 / SUM(sales) OVER (PARTITION BY month), 2) as pct_of_monthly_sales
FROM product_sales
ORDER BY month, sales DESC;
```

---

## Performance Considerations

### 1. Indexing
- Create indexes on columns used in PARTITION BY and ORDER BY
- Consider covering indexes for frequently used window function queries

```sql
-- Good index for department-based window functions
CREATE INDEX idx_emp_dept_salary ON employees (department_id, salary DESC);
```

### 2. Frame Specification
- Be specific with frame clauses to avoid unnecessary calculations
- Default frame for aggregate functions with ORDER BY is `RANGE UNBOUNDED PRECEDING`

### 3. Multiple Window Functions
- Define window specifications once and reuse them

```sql
-- Efficient: Define window once
SELECT 
    employee_id,
    salary,
    ROW_NUMBER() OVER win as rn,
    RANK() OVER win as rnk,
    AVG(salary) OVER win as avg_salary
FROM employees
WINDOW win AS (PARTITION BY department_id ORDER BY salary DESC);
```

### 4. Avoid in WHERE Clause
- Window functions cannot be used directly in WHERE clause
- Use CTE or subquery instead

```sql
-- Correct way to filter on window function results
WITH ranked_data AS (
    SELECT 
        employee_id,
        salary,
        ROW_NUMBER() OVER (ORDER BY salary DESC) as rn
    FROM employees
)
SELECT employee_id, salary
FROM ranked_data
WHERE rn <= 10;
```

---

## Common Use Cases

### 1. Business Analytics
- Running totals and moving averages
- Year-over-year comparisons
- Percentile analysis
- Top N analysis

### 2. Data Quality
- Duplicate detection using ROW_NUMBER()
- Gap analysis in sequential data
- Outlier detection using statistical functions

### 3. Reporting
- Ranking and scoring
- Cumulative distributions
- Period-over-period analysis
- Contribution analysis

### 4. Time Series Analysis
- Trend analysis with LAG/LEAD
- Seasonal comparisons
- Moving statistics
- Change point detection

---

## Advanced Tips

### 1. Named Windows
```sql
SELECT 
    employee_id,
    salary,
    ROW_NUMBER() OVER dept_salary_desc as dept_rank,
    AVG(salary) OVER dept_all as dept_avg_salary
FROM employees
WINDOW 
    dept_salary_desc AS (PARTITION BY department_id ORDER BY salary DESC),
    dept_all AS (PARTITION BY department_id);
```

### 2. Conditional Window Functions
```sql
-- Count only high-value sales in running total
SELECT 
    date,
    sales,
    COUNT(CASE WHEN sales > 1000 THEN 1 END) OVER (ORDER BY date) as high_sales_count
FROM daily_sales;
```

### 3. Window Functions with CASE
```sql
-- Different rankings for different categories
SELECT 
    product_name,
    category,
    sales,
    CASE category
        WHEN 'Electronics' THEN RANK() OVER (PARTITION BY category ORDER BY sales DESC)
        WHEN 'Clothing' THEN ROW_NUMBER() OVER (PARTITION BY category ORDER BY sales DESC)
        ELSE NULL
    END as category_rank
FROM products;
```

---

## Interview Questions & Answers

### Q1: What's the difference between ROW_NUMBER(), RANK(), and DENSE_RANK()?
**Answer:** 
- `ROW_NUMBER()`: Always assigns unique sequential numbers (1,2,3,4...)
- `RANK()`: Assigns same rank to ties, skips next ranks (1,2,2,4...)
- `DENSE_RANK()`: Assigns same rank to ties, doesn't skip ranks (1,2,2,3...)

### Q2: How do you find the 2nd highest salary in each department?
**Answer:**
```sql
WITH ranked_salaries AS (
    SELECT 
        employee_id,
        department_id,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) as rn
    FROM employees
)
SELECT employee_id, department_id, salary
FROM ranked_salaries
WHERE rn = 2;
```

### Q3: Explain the default frame for window functions.
**Answer:**
- Without ORDER BY: Frame is entire partition
- With ORDER BY but no frame: `RANGE UNBOUNDED PRECEDING` (from start to current row)
- This can cause unexpected results with LAST_VALUE() - always specify frame explicitly

---

This comprehensive guide covers the essential concepts and practical applications of window functions in SQL. Practice with real datasets to master these powerful analytical tools!