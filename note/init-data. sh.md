
```
#!/bin/bash
set -e;
  
  
if [ -n "${POSTGRES_NON_ROOT_USER:-}" ] && [ -n "${POSTGRES_NON_ROOT_PASSWORD:-}" ]; then
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        CREATE USER ${POSTGRES_NON_ROOT_USER} WITH PASSWORD '${POSTGRES_NON_ROOT_PASSWORD}';
        GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_NON_ROOT_USER};
        GRANT CREATE ON SCHEMA public TO ${POSTGRES_NON_ROOT_USER};
    EOSQL
else
    echo "SETUP INFO: No Environment variables given!"
fi
```

好的，这是一个对 `init-data.sh` 脚本的详细中文解释。

这个脚本是一个数据库初始化脚本，它的核心作用是**为 n8n 应用创建一个专用的、非 root 的数据库用户，并授予其必要的权限**。这是一种非常好的安全实践，避免了让应用程序直接使用拥有最高权限的 `postgres` 超级用户连接数据库。

---

### 脚本逐行解析

1. **`#!/bin/bash`**
    
    - 这是一个 "shebang"，它告诉系统这个脚本需要使用 Bash shell 来执行。
        
2. **`set -e;`**
    
    - 这是一个安全设置。它表示如果在执行过程中有任何命令失败（返回非零退出码），整个脚本将立即停止执行。这可以防止因某个命令意外失败而导致后续的错误操作。
        
3. **`if [ -n "${POSTGRES_NON_ROOT_USER:-}" ] && [ -n "${POSTGRES_NON_ROOT_PASSWORD:-}" ]; then`**
    
    - 这是一个条件判断语句。
        
    - 它检查 `POSTGRES_NON_ROOT_USER` 和 `POSTGRES_NON_ROOT_PASSWORD` 这两个环境变量**是否都存在并且值不为空**。
        
    - 只有当这两个变量都设置了，`if` 后面的代码块才会被执行。
        
4. **`psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL`**
    
    - 如果条件满足，这行命令会启动 PostgreSQL 的命令行工具 `psql` 来执行一段 SQL 代码。
        
    - `-v ON_ERROR_STOP=1`: 确保在执行 SQL 时，一旦遇到错误就立即停止。
        
    - `--username "$POSTGRES_USER"`: 使用环境变量中定义的超级用户（通常是 `postgres`）来连接数据库。
        
    - `--dbname "$POSTGRES_DB"`: 连接到环境变量中指定的数据库（例如 `n8n`）。
        
    - `<<-EOSQL`: 这是一个 "here document"，它允许你将 `EOSQL` 标记之间的多行文本作为输入传递给 `psql` 命令。
        
5. **SQL 命令块**
    
    - **`CREATE USER ${POSTGRES_NON_ROOT_USER} WITH PASSWORD '${POSTGRES_NON_ROOT_PASSWORD}';`**
        
        - 创建一个新的数据库用户，用户名和密码来自于环境变量。
            
    - **`GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_NON_ROOT_USER};`**
        
        - 将指定数据库的所有权限授予这个新创建的用户。
            
    - **`GRANT CREATE ON SCHEMA public TO ${POSTGRES_NON_ROOT_USER};`**
        
        - 额外授予新用户在 `public` 模式（schema）下创建对象（如数据表）的权限。对于 n8n 这样的应用来说，这个权限是必需的，否则它可能无法正常创建自己的数据表。
            
6. **`else ... fi`**
    
    - 如果最开始的 `if` 条件不满足（即缺少用户名或密码的环境变量），脚本会执行 `else` 部分的代码。
        
    - **`echo "SETUP INFO: No Environment variables given!"`**: 它会打印一条提示信息到日志中，告知用户没有提供必要的环境变量，然后脚本就结束了，不会执行任何数据库操作。
        

---

### 总结

当 PostgreSQL 容器第一次启动时，它会自动运行这个脚本。脚本会检查你是否在 `.env` 文件或 `docker-compose.yml` 中定义了 `POSTGRES_NON_ROOT_USER` 和 `POSTGRES_NON_ROOT_PASSWORD`。如果定义了，它就会为你安全地创建好 n8n 需要的数据库用户和权限。如果没定义，它就什么也不做。