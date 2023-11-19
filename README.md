# good-flavor
This is the backend code for the "good-flavor" project.

# Configure environment
* python 3.8+
* PostgreSQL 14

# Install libraries and dependencies
Under the project root directory<br>
Execute:
```powershell
pip install -r requirements.txt
```
# Create tables
Under the project root directory<br>
Execute:
```shell
createdb tb
psql -U postgres -d tb -f "src/sql/1_create_table.sql" 
psql -U postgres -d tb -f "src/sql/2_trigger.sql"
```
# Set the username and password for the database
Under the project root directory<br>
Create `config.json`:
```json
{
	"username":"postgres",
	"password":"password"
}
```
# Start the server
Under the project root directory<br>
Execute:
```powershell
uvicorn src.main:app --reload 
```
# Details of this project
https://docs.google.com/document/d/11coszMhuLH1KRHeZetHJNaN1YgMVt9RwFA5YJ9y6ftA/edit#heading=h.vgvh8m3hxy71
