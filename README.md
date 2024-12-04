# Payroll Management System

## How to run?
- Change user and password in the program.

## Table structure
### Structure - 
- create table emp (emp_id integer PRIMARY KEY, name varchar(50), position varchar(50), salary float, department varchar(50), PF float, DA float, HRA float, medical_leave int, working_days int, date_of_joining datetime, loan_taken float DEFAULT 0, amount_topay float DEFAULT 0, loan_date DATETIME);

`

    +-----------------+-------------+------+-----+---------+-------+
    | Field           | Type        | Null | Key | Default | Extra |
    +-----------------+-------------+------+-----+---------+-------+
    | emp_id          | int         | NO   | PRI | NULL    |       |
    | name            | varchar(50) | YES  |     | NULL    |       |
    | position        | varchar(50) | YES  |     | NULL    |       |
    | salary          | float       | YES  |     | NULL    |       |
    | department      | varchar(50) | YES  |     | NULL    |       |
    | PF              | float       | YES  |     | NULL    |       |
    | DA              | float       | YES  |     | NULL    |       |
    | HRA             | float       | YES  |     | NULL    |       |
    | medical_leave   | int         | YES  |     | 0       |       |
    | working_days    | int         | YES  |     | NULL    |       |
    | date_of_joining | datetime    | YES  |     | NULL    |       |
    | loan_taken      | float       | YES  |     | 0       |       |
    | amount_topay    | float       | YES  |     | 0       |       |
    | loan_date       | datetime    | YES  |     | NULL    |       |
    +-----------------+-------------+------+-----+---------+-------+    
