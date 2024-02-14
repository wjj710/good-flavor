# good-flavor
This is the backend code for the "good-flavor" project.

## Introduction
The system has two types of users: normal user and administrator. 

A normal user can post requests for delicious food or respond to others’ requests by recommending a restaurant or cooking the food himself. If his request has received other people’s reply, he can either accept or refuse it. If he accepts it, the system will charge him and the other one some agency fee.

An administrator can check some statistical information about the users, requests and agency fee. For example, he can query the amount of agency fee and the number of transaction orders in a certain region during a certain period of time.

## Usage

### Configure environment
* WSL 2
* python 3.8+
* PostgreSQL 14

### Install libraries and dependencies
Under the project root directory<br>
Execute:
```powershell
pip install -r requirements.txt
```
### Create tables
Under the project root directory<br>
Execute:
```shell
sudo -u postgres psql
CREATE DATABASE tb;
\c tb
\i src/sql/1_create_table.sql 
\i src/sql/2_trigger.sql
```
### Set the username and password for the database
Under the project root directory<br>
Create `config.json`:
```json
{
	"username":"postgres",
	"password":"password"
}
```
If there are some problems with password authentication, see [this](https://hassanannajjar.medium.com/how-to-fix-error-password-authentication-failed-for-the-user-in-postgresql-896e1fd880dc).
### Start the server
Under the project root directory<br>
Execute:
```powershell
uvicorn src.main:app --reload 
```

