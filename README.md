# good-flavor
This is the backend code for the "good-flavor" project.

# Configure environment
* python 3.8+
* PostgreSQL 14

# Install libraries and dependencies
在项目根目录下
```powershell
pip install -r requirements.txt
```
# Create tables
在项目根目录下
```shell
createdb tb
psql -U postgres -d tb -f "src/sql/1_create_table.sql" 
psql -U postgres -d tb -f "src/sql/2_trigger.sql"
```
# Set the username and password for the database
目录下新建`config.json`:
```json
{
	"username":"postgres",
	"password":"password"
}
```
# Start the server
在项目根目录下
```powershell
uvicorn src.main:app --reload 
```
