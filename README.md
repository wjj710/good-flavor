# good-flavor
此仓库用来存储2022年北邮《Web开发技术》的大作业后端代码。

# 配置环境
* python 3.8+
* PostgreSQL 14

# 安装库
在项目根目录下
```powershell
pip install -r requirements.txt
```
# 创建表
Linux
```shell
createdb tb
psql -U postgres -d tb -f "src/sql/1_create_table.sql" 
psql -U postgres -d tb -f "src/sql/2_index.sql"
psql -U postgres -d tb -f "src/sql/3_trigger.sql" 
```
Windows
```powershell
createdb.exe tb
psql.exe -U postgres -d tb -f "src\sql\1_create_table.sql" 
psql.exe -U postgres -d tb -f "src\sql\2_index.sql" 
psql.exe -U postgres -d tb -f "src\sql\3_trigger.sql" 
```
# 配置数据库
目录下新建`config.json`:
```json
{
	"username":"postgres",
	"password":"password"
}
```
# 启动server
在项目根目录下
```powershell
uvicorn src.main:app --reload 
```
