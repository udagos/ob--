---
up:
  - "[[../moc/n8n|n8n]]"
---

version: '3.8'

volumes:
  db_storage:
  n8n_storage:

services:
  postgres:
    image: postgres:16
    restart: always
    environment:
      - POSTGRES_USER
      - POSTGRES_PASSWORD
      - POSTGRES_DB
      - POSTGRES_NON_ROOT_USER
      - POSTGRES_NON_ROOT_PASSWORD
    volumes:
      - db_storage:/var/lib/postgresql/data
      - ./init-data.sh:/docker-entrypoint-initdb.d/init-data.sh
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -h localhost -U ${POSTGRES_USER} -d ${POSTGRES_DB}']
      interval: 5s
      timeout: 5s
      retries: 10

  n8n:
    image: swr.cn-north-4.myhuaweicloud.com/ddn-k8s/ghcr.io/n8n-io/n8n:1.84.1
    restart: always
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=${POSTGRES_DB}
      - DB_POSTGRESDB_USER=${POSTGRES_NON_ROOT_USER}
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_NON_ROOT_PASSWORD}
    ports:
      - 5678:5678
    links:
      - postgres
    volumes:
      - n8n_storage:/home/node/.n8n
      - E:\docker_n8n:/home/node/Files
      - C:\Users\udago\AppData\Local\Microsoft\Edge\User Data\Profile 1:/home/node/Files/bookmarks
    depends_on:
      postgres:
        condition: service_healthy

```
好的，这是一个 Docker Compose 文件的配置说明，我会用中文为您详细解释。

这个 Docker Compose 文件定义了一个多容器的应用，用于部署 **n8n 自动化平台**，并使用一个独立的 **PostgreSQL 数据库**来持久化存储其数据。

简单来说，它的作用就是自动化地搭建一套自托管的 n8n 服务。在这套服务中，您的工作流、凭证和执行记录都会被安全地保存在一个专用的数据库里，而不是默认的 SQLite 文件中，这样更稳定、更适合生产环境。

---

### 定义的服务 (Services)

该文件设置了两个相互协作的服务（即两个容器）：

#### 1. `postgres` 服务 🐘

- **用途**: 运行一个 PostgreSQL 数据库（版本 16），作为 n8n 的数据后端。
    
- **数据持久化**: 它使用一个名为 `db_storage` 的数据卷 (volume) 来存储数据库文件。这确保了即使容器被删除或重启，您的所有 n8n 数据（如工作流、凭证等）都不会丢失。
    
- **初始化**: 在首次启动时，它会==自动运行您项目目录下的 `init-data.sh` 脚本==。这个脚本通常用来创建 n8n 连接所需的特定数据库和非 root 用户，这是一种很好的安全实践。
    
- **健康检查 (`healthcheck`)**: 这个配置会定期检查数据库是否已准备好接受连接。这对于控制应用的启动顺序至关重要。
    
好的，这两行是 Docker Compose 中的**数据卷挂载 (volume mounts)** 配置，作用是在您的电脑（宿主机）和 Docker 容器之间共享和持久化数据。

---

##### 1. `db_storage:/var/lib/postgresql/data`

这行代码的作用是==设置一个**命名卷 (named volume)**，用来持久化存储您的数据库数据==。

- **`db_storage`**: 这是==由 Docker 管理的数据卷的名称。您可以把它想象成一个由 Docker 在您电脑上创建并管理的专用“数据盘”，它独立于容器本身存在==。
    
- **`/var/lib/postgresql/data`**: 这是 ==PostgreSQL 容器内部默认用来存放所有数据库文件（例如表、索引、用户信息等）的路径==。
    

**它的效果是**: 将容器内部的 PostgreSQL 数据目录链接到 `db_storage` 这个数据卷上。这样做可以确保，**即使您停止、删除或重新创建 PostgreSQL 容器，所有的数据库数据都会被安全地保存在这个数据卷中，不会丢失**。如果没有这一行，容器一旦被删除，里面的所有数据都会消失。

---

##### 2. `./init-data.sh:/docker-entrypoint-initdb.d/init-data.sh`

这行代码的作用是==设置一个**绑定挂载 (bind mount)**，用来在数据库初始化时执行一个自定义脚本==。

- **`./init-data.sh`**: 指的是位于您电脑上、与 `docker-compose.yml` 文件在同一个目录下的 `init-data.sh` 脚本文件。
    
- **`/docker-entrypoint-initdb.d/init-data.sh`**: 这是 PostgreSQL 官方镜像内部的一个**特殊目录**。
    

**它的效果是**: 将您本地的 `init-data.sh` 文件映射到容器内的初始化目录中。==PostgreSQL 容器被设计为**在数据库第一次被创建时，会自动执行**放在这个目录里的所有 `.sh` (脚本文件) 或 `.sql` (SQL文件)。这个过程**只会发生一次**。因此，它通常被用来执行一些初始设置任务，比如：为您的应用程序创建一个专用的数据库用户和密码，或者创建初始的数据表结构==。
#### 2. `n8n` 服务 ⚙️

- **用途**: 这是运行 n8n 自动化平台（版本 1.84.1）的主应用服务。
    
- **数据库连接**: 它的环境变量被配置为连接到 `postgres` 服务。主机名 `postgres` 之所以能生效，是因为 Docker Compose 创建了一个内部网络，服务之间可以通过服务名相互访问。
    
- **外部访问**: 它将容器的 `5678` 端口映射到您电脑（宿主机）的 `5678` 端口。这样，您就可以通过在浏览器中访问 `http://localhost:5678` 来使用 n8n 界面。
    
- **数据持久化**: 它使用 `n8n_storage` 数据卷来保存 n8n 本身的配置文件和加密密钥等。
    
- **本地文件映射**:
    
    - `E:\docker_n8n:/home/node/Files`: 将您 Windows 系统 E 盘的 `docker_n8n` 文件夹映射到 n8n 容器内的 `/home/node/Files` 目录。这使得 n8n 的工作流可以直接读取或写入您电脑上的文件。
        
    - `C:\Users\...`: 将您 Windows C 盘的 Edge 浏览器用户配置文件夹映射到了容器中。这可能是为了让 n8n 读取浏览器的书签或其他数据。**请注意：直接映射这类应用数据文件可能导致文件锁或权限问题，需谨慎使用。**
        
- **启动依赖 (`depends_on`)**: 这是非常关键的配置。它规定 `n8n` 服务**必须等待** `postgres` 服务的健康检查 (`healthcheck`) 状态变为 `healthy` (即数据库完全准备就绪) 之后才能启动。这可以有效防止 n8n 因数据库尚未就绪而启动失败。
    
好的，这三行都是**数据卷挂载 (volume mounts)** 配置，作用是在您的电脑（宿主机）和 n8n 容器之间建立链接，用于持久化数据和允许 n8n 访问您电脑上的本地文件。

---

##### 1. `n8n_storage:/home/node/.n8n`

这一行是==使用**命名卷 (named volume)** 来保存 n8n 的核心数据==。💾

- **`n8n_storage`**: 这是一个由 Docker 自己管理的数据存储空间。它是持久化应用数据的最安全、最推荐的方式。
    
- **`/home/node/.n8n`**: 这是 ==n8n 容器内部的默认工作目录，n8n 会在这里存储它所有最重要的数据，包括你的**工作流 (`workflows`)、凭证 (`credentials`) 和执行日志**等==。
    

**用途**: 这项挂载确保了你所有的 n8n 配置和工作流都能被永久保存。即使你停止或删除了 n8n 容器，这些数据依然安全地存放在 Docker 的数据卷中，当你下次启动容器时会自动加载，数据不会丢失。

---

##### 2. `E:\docker_n8n:/home/node/Files`

这一行是==使用**绑定挂载 (bind mount)** 来将一个本地文件夹共享给 n8n 使用==。📂

- **`E:\docker_n8n`**: 这是指你电脑 E 盘上一个名为 `docker_n8n` 的文件夹。
    
- **`/home/node/Files`**: 这是 n8n 容器内部的一个文件夹。
    

**用途**: 这个设置让你的 n8n 工作流可以直接访问你电脑上的 `docker_n8n` 文件夹。你可以利用这个功能，让工作流去读取本地的 Excel 文件、处理文件夹里的图片，或者将生成的数据报告直接保存到你的电脑上。

---

### 3. `C:\Users\...:/home/node/Files/bookmarks`

这一行是一个更特殊的**绑定挂载**，用于访问浏览器的特定数据。🔖

- **`C:\Users\udago\AppData\Local\Microsoft\Edge\User Data\Profile 1`**: 这是指向你 Windows 系统上某个微软 Edge 浏览器配置文件的完整路径。
    
- **`/home/node/Files/bookmarks`**: 这是容器内部的一个子文件夹。
    

**用途**: 这个挂载的目的是让 n8n 工作流能够访问你 Edge 浏览器的用户数据，很可能是为了读取其中的 `Bookmarks` (书签) 文件。例如，你可以创建一个自动化流程来读取、处理或备份你的浏览器书签。
![](../fujian/Pasted%20image%2020250824114049.png)
---

### 如何使用它

1. **创建 `.env` 文件**: 在与此 `docker-compose.yml` 文件相同的目录下，创建一个名为 `.env` 的文件。这个文件用于存放敏感信息，如数据库密码。文件内容应如下：
    
    代码段
    
    ```
    # .env 文件示例
    
    # PostgreSQL 超级用户信息
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=your_super_strong_password
    
    # n8n 将要使用的数据库信息
    POSTGRES_DB=n8n
    POSTGRES_NON_ROOT_USER=n8n_user
    POSTGRES_NON_ROOT_PASSWORD=another_strong_password_for_n8n
    ```
    
2. **创建 `init-data.sh` 脚本**: 同样在当前目录下，创建 `init-data.sh` 文件。这个脚本用于创建 n8n 专用的数据库用户和授权。
    
    Bash
    
    ```
    #!/bin/bash
    set -e
    
    # 创建一个非 root 用户并授予其对 n8n 数据库的所有权限
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        CREATE USER $POSTGRES_NON_ROOT_USER WITH PASSWORD '$POSTGRES_NON_ROOT_PASSWORD';
        GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_NON_ROOT_USER;
    EOSQL
    ```
    
3. **启动服务**: 打开终端或命令行工具，进入该目录，然后运行以下命令：
    
    Shell
    
    ```
    docker-compose up -d
    ```
    
    `-d` 参数表示在后台运行服务。
    
1. **访问 n8n**: 等待几分钟让服务完全启动后，在您的浏览器中打开 `http://localhost:5678`，即可开始设置和使用 n8n。

# [[init-data. sh]]
 
#  n8n storage 数据卷的内容具体都是什么
 好的，根据您提供的截图，我们来详细解释一下这个 `n8n_storage` 数据卷里的内容具体都是什么。

首先请注意，您在 `docker-compose.yml` 中定义的名字是 `n8n_storage`，而截图中显示为 `withpostgres_n8n_storage`，这是 Docker Compose 的正常行为。它会自动将项目目录名（`withpostgres`）作为前缀加在数据卷名前面。

这个数据卷是您 n8n 应用的核心，它保存了所有让您的 n8n 实例能够个性化运行的关键数据和配置。没有它，n8n 每次重启都会恢复到初始状态。

以下是截图中各个文件和目录的具体作用：

---

### 文件/目录详解

- 📁 **`binaryData`**
    
    - **用途**: 用于存储工作流执行过程中产生的**二进制数据**。例如，当您的工作流下载了一张图片、一个 PDF 文件或处理了任何文件时，这些文件的临时或永久副本会保存在这里。这是处理文件相关流程的关键目录。
        
- 📄 **`config`**
    
    - **用途**: 这是一个简单的**配置文件**，可能包含 n8n 的一些基本用户设置或偏好。
        
- 📄 **`crash.journal`**
    
    - **用途**: **崩溃日志文件**。如果 n8n 应用程序意外崩溃，相关信息会记录在这里，便于排查问题。文件大小为 0 字节表示近期没有发生崩溃。
        
- 📁 **`git`**
    
    - **用途**: 如果您为您的工作流启用了 **Git 版本控制**功能，这个目录就是用来存放本地 Git 仓库的地方。它可以帮助您追踪和管理工作流的每一次变更，实现版本回退等高级功能。
        
- 📄 **`n8nEventLog-*.log`**
    
    - **用途**: n8n 的**事件日志文件**。这些文件记录了应用的运行事件，比如服务的启动、停止、工作流的执行信息等，主要用于日常监控和调试。看到多个文件是因为 n8n 会进行日志轮转（Log Rotation）来防止单个日志文件过大。
        
- 📁 **`nodes`**
    
    - **用途**: 这是非常重要的一个目录，通常用来存放**用户手动安装的社区节点（Community Nodes）**。当您通过 n8n 界面或命令行添加了官方默认节点之外的第三方节点时，这些节点包就会被下载并安装到这里。这个目录的大小（33.8 MB）也说明您可能安装了一些自定义节点。
        
- 📁 **`ssh`**
    
    - **用途**: 用于存放 **SSH 密钥**。当您的 n8n 需要通过 SSH 连接到其他服务时，所需的 SSH 密钥就存放在这里。常见的用例包括：
        
        - 使用 Git 功能连接到私有的 Git 仓库（如 GitLab/GitHub）。
            
        - 使用 "Execute Command" 节点通过 SSH 远程执行服务器命令。
            

---

### 总结

总而言之，这个 `withpostgres_n8n_storage` 数据卷就是您 n8n 实例的**“大脑和记忆”**。它包含了：

- **您的所有工作流和凭证（存储在数据库中，但此目录包含相关配置和密钥）。**
    
- **您安装的自定义节点。**
    
- **用于版本控制和远程连接的配置。**
    
- **运行日志和临时文件。**
    

**备份这个数据卷就等于备份了您所有的工作成果**。当您需要迁移或恢复 n8n 服务时，只需要恢复这个数据卷（以及 `db_storage` 数据库卷）即可。

## 1  数据卷和容器目录
![](../fujian/Pasted%20image%2020250825083810.png)
容器目录
![](../fujian/Pasted%20image%2020250825083937.png)
数据卷
![](../fujian/Pasted%20image%2020250825083837.png)

# db storage 数据卷的内容具体都是什么
好的，这张截图展示的是 `db_storage` 数据卷的内容，也就是 PostgreSQL 数据库的**数据目录 (Data Directory)**。

简单来说，这个 `db_storage` 数据卷就是您的 PostgreSQL 数据库服务器的**“物理硬盘”**，它包含了运行一个完整数据库实例所需的所有文件，从配置文件到用户数据本身，一切都在这里。

同样，您会看到卷名为 `withpostgres_db_storage`，这是 Docker Compose 将项目目录名 `withpostgres` 作为前缀添加的结果。

以下是其中最关键的一些文件和目录的用途说明：

---

### 核心数据目录

- 📁 **`base`**
    
    - **用途**: 这是**最核心**的目录，您的实际数据就存放在这里。里面会为每个数据库（包括 n8n 的库以及系统默认的库）创建一个子目录，而您的表和索引等数据文件就保存在这些子目录中。
        
- 📁 **`global`**
    
    - **用途**: 存放集群范围的全局数据，比如关于数据库和用户（角色）的系统目录表。
        

### 核心配置文件

- 📄 **`postgresql.conf`**
    
    - **用途**: PostgreSQL 的**主配置文件**。几乎所有的服务器运行参数都在这里设置，例如内存分配 (`shared_buffers`)、最大连接数 (`max_connections`)、日志记录行为等。
        
- 📄 **`pg_hba.conf`**
    
    - **用途**: 这是 PostgreSQL 的**主机认证配置文件** (Host-Based Authentication)。它定义了**谁**可以从**哪个 IP 地址**连接到数据库，以及需要使用**何种验证方式**（例如，密码验证）。这是一个至关重要的安全配置文件。
        

### 数据完整性与恢复

- 📁 **`pg_wal`**
    
    - **用途**: 这是**预写式日志** (Write-Ahead Log) 的存放目录。为了保证数据的一致性和可恢复性，任何对数据的更改都会先在这里被记录下来，然后再写入到 `base` 目录的主数据文件中。如果数据库意外崩溃，PostgreSQL 会通过重放 (replay)这些日志来恢复数据，确保数据不会损坏或丢失。这是保证数据安全的关键机制。
        

### 进程与版本信息

- 📄 **`PG_VERSION`**
    
    - **用途**: 一个纯文本文件，里面只记录了 PostgreSQL 的主版本号（例如，`16`）。这用来防止错误地用一个不兼容的 PostgreSQL 程序版本来启动现有数据库。
        
- 📄 **`postmaster.pid`**
    
    - **用途**: 一个**锁文件**，当 PostgreSQL 服务器正在运行时，这个文件就会存在。它记录了主进程的 ID (PID)。它的主要作用是防止同一个数据目录被多个数据库实例同时启动，从而避免数据损坏。当数据库正常关闭时，这个文件会被自动删除。
        

### 其他内部目录

- **其他所有 `pg_*` 开头的目录** (如 `pg_commit_ts`, `pg_multixact`, `pg_stat`, `pg_subtrans` 等)
    
    - **用途**: 这些都是 PostgreSQL 内部用于管理事务、多事务状态、统计信息、通知、复制等功能的目录。普通用户和管理员通常不需要直接与它们交互。
        

---

### 总结

总而言之，这个数据卷就是您的 n8n **数据库本身**。其中包含了配置、运行状态以及最重要的——由 n8n 创建和使用的所有数据（工作流、执行记录、凭证等）。

因此，保证这个数据卷的持久化和安全至关重要。在做备份时，您需要同时备份 `db_storage` 和 `n8n_storage` 才能完整地保护您的整个 n8n 服务。


# 如何查看PostgreSQL的表，及这些表是存储什么数据
非常好的问题！了解数据库的内部结构对于深入使用和维护 n8n非常有帮助。

要查看 PostgreSQL 中的表以及它们存储的数据，分为两个步骤：首先是连接到数据库，其次是执行查询命令。由于您的数据库运行在 Docker 容器中，我们需要通过 Docker 来完成第一步。

---

### 第一步：连接到数据库容器

您需要使用 `docker exec` 命令进入正在运行的 `postgres` 容器，并启动 `psql` 命令行工具。

1. 查找容器的准确名称
    
    在您的电脑终端中运行以下命令，列出所有正在运行的容器：
    
    Bash
    
    ```
    docker ps
    ```
    
    您会看到类似下面的输出。找到 `IMAGE` 为 `postgres:16` 的那一行，并记下它的 `NAMES`。名字通常是 `项目名-服务名-1` 的格式，例如 `withpostgres-postgres-1`。
    
    ```
    CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                    NAMES
    a1b2c3d4e5f6   postgres:16    "docker-entrypoint.s…"   5 days ago      Up 5 days      0.0.0.0:5432->5432/tcp   withpostgres-postgres-1
    ...
    ```
    
2. 进入容器并连接数据库
    
    使用以下命令连接。请将 <容器名> 替换为您上一步找到的名称。这个命令会使用您在 .env 文件中为 n8n 配置的非 root 用户 (POSTGRES_NON_ROOT_USER) 连接到 n8n 的数据库 (POSTGRES_DB)。
    
    Bash
    
    ```
    docker exec -it <容器名> psql -U ${POSTGRES_NON_ROOT_USER} -d ${POSTGRES_DB}
    ```
    
    **举例**，如果您的容器名叫 `withpostgres-postgres-1`，并且您设置的用户是 `n8n_user`，数据库是 `n8n`，那么命令就是：
    
    Bash
    
    ```
    docker exec -it withpostgres-postgres-1 psql -U n8n_user -d n8n
    ```
    
    执行后，系统会提示您输入该用户的密码 (`POSTGRES_NON_ROOT_PASSWORD`)。输入正确后，您会看到 `psql` 的命令提示符，类似 `n8n=>`，表示您已成功连接。
    

---

### 第二步：查看表和数据

成功连接到 `psql` 后，您可以使用以下命令来查看信息。这些命令以反斜杠 `\` 开头。

- 列出所有表
    
    这个命令会列出当前数据库（n8n 库）中所有的表。
    
    SQL
    
    ```
    \dt
    ```
    
- 查看表的详细结构
    
    要查看某个具体表的列、数据类型等详细信息，使用 \d 命令，后面跟表名。
    
    SQL
    
    ```
    \d workflow_entity
    ```
    
- 查看表中的数据（重要！）
    
    您可以使用标准的 SQL 查询语句来查看表中的实际数据。
    
    强烈建议在查询时加上 LIMIT 子句，这样可以只看几行示例数据，避免因数据量过大导致终端卡死。
    
    SQL
    
    ```
    -- 查看 workflow_entity 表的前 5 条记录
    SELECT * FROM workflow_entity LIMIT 5;
    
    -- 查看 execution_entity 表的前 10 条记录
    SELECT * FROM execution_entity LIMIT 10;
    ```
    
    要退出 `psql`，可以输入 `\q` 然后按回车。
    

---

### n8n 数据库中的核心表及其用途

n8n 使用 [TypeORM](https://typeorm.io/) 框架来管理数据库，所以表名都比较规范。以下是您会看到的一些核心表以及它们存储的数据：

| 表名 (`Table Name`)         | 用途说明                                                                                                  |
| ------------------------- | ----------------------------------------------------------------------------------------------------- |
| **`workflow_entity`**     | 存储您创建的**所有工作流 (Workflow)** 的核心信息，包括名称、节点、连接、设置等。这是最重要的表之一。                                            |
| **`execution_entity`**    | 记录**每一次工作流的执行历史**。每当一个工作流运行一次，就会在这里生成一条或多条记录，包含开始时间、结束时间、状态（成功/失败）以及详细的输入输出数据（通常是JSON格式）。这个表可能会变得非常大。 |
| **`credentials_entity`**  | 存储您在 n8n 中创建的**所有凭证 (Credentials)**。**重要**：这些凭证数据是经过加密的，所以您无法在数据库中直接看到原始的密码或 API 密钥。                  |
| **`webhook_entity`**      | 管理通过 Webhook 触发器节点创建的**所有 Webhook 链接**。当 n8n 等待外部信号来触发工作流时，相关信息就存在这里。                                 |
| **`user`**                | 如果您为 n8n 实例启用了**用户管理功能**，这个表会存储所有用户的账户信息（用户名、加密后的密码等）。                                                |
| **`workflow_tag_entity`** | 存储您为工作流设置的**标签 (Tag)**，用于分类和组织工作流。                                                                    |
| **`migrations`**          | 这是 TypeORM 框架用来**管理数据库结构版本**的内部表。它记录了数据库结构的变更历史，请**绝对不要手动修改**它。                                       |

⚠️ 安全警告：

您可以安全地使用 SELECT 命令来查看数据。但是，请绝对不要手动使用 UPDATE, INSERT 或 DELETE 来修改这些表中的数据，除非您完全清楚这样做的后果。直接修改数据库可能会破坏 n8n 应用的数据完整性，导致应用无法正常工作。


##  表项
![](../fujian/Pasted%20image%2020250825102950.png)

您做得非常好！这张截图完美地展示了 n8n 数据库中用来存储所有关系数据的表。这个列表比我们上次讨论的要完整得多，它揭示了 n8n 更多强大的内部功能。

正如我们之前讨论的，这些表共同构成了 n8n 的“记忆”，存储着从工作流定义到每次执行的详细数据的一切。我将根据它们的功能对这些表进行分类解释，包含我们之前提过的和新出现的表：

---

### 表的功能分类详解

#### 工作流与版本管理 (Workflows & Versioning)

- **`workflow_entity`**: **(核心)** 存储您所有工作流的定义（节点、连接、设置）。
    
- **`workflow_history`**: 存储工作流的**历史版本**。每次保存工作流时，旧的版本可能会被记录在这里。
    
- **`workflows_tags`**: 关联工作流和标签的中间表。
    
- **`tag_entity`**: 存储您创建的所有标签 (Tag) 的信息。
    
- **`folder`**: 存储您在 UI 中创建的用于组织工作流的**文件夹**。
    
- **`folder_tag`**: 关联文件夹和标签的中间表。
    
- **`shared_workflow`**: 用于管理被分享的工作流。
    

#### 执行与数据日志 (Executions & Data Logs)

- **`execution_entity`**: **(核心)** 存储每一次工作流执行的主记录（状态、开始/结束时间）。
    
- **`execution_data`**: 存储工作流执行过程中每个节点的详细**输入/输出数据 (JSON)**，通常与 `execution_entity` 关联。这个表可能会非常大。
    
- **`execution_metadata`**: 存储执行的元数据，例如执行模式（手动/生产）。
    
- **`execution_annotations`** & **`execution_annotation_tags`**: 用于存储您可能对某次执行添加的**注释或标签**，便于调试和回顾。
    
- **`processed_data`**: 可能用于存储某些节点处理后的中间或缓存数据。
    

#### 凭证与认证 (Credentials & Authentication)

- **`credentials_entity`**: **(核心)** 存储您所有**加密后**的凭证。
    
- **`shared_credentials`**: 用于管理在用户之间共享的凭证。
    
- **`auth_identity`**, **`auth_provider_sync_history`**, **`invalid_auth_token`**: 这些与用户认证体系相关，特别是当使用 SSO（单点登录）等高级功能时。
    
- **`user_api_keys`**: 存储为用户生成的，用于通过 API 与 n8n 交互的 API 密钥。
    

#### 用户、项目与角色 (Users, Projects & Roles)

- **`user`**: **(核心)** 存储 n8n 的用户账户。
    
- **`role`**: 定义不同的用户**角色**（如管理员、普通用户）及其权限。
    
- **`project`** & **`project_relation`**: 用于支持“项目”功能，允许将工作流、凭证等资源分组隔离。
    

#### 系统、节点与设置 (System, Nodes & Settings)

- **`installed_nodes`** & **`installed_packages`**: 记录您通过社区市场安装的**自定义节点**。
    
- **`migrations`**: **(内部使用)** TypeORM 框架用来管理数据库版本迭代的表，**请勿修改**。
    
- **`settings`**: 存储 n8n 实例的全局设置。
    
- **`variables`**: 存储您创建的，可在多个工作流中使用的**全局变量**。
    
- **`webhook_entity`**: **(核心)** 存储所有 Webhook 触发器的注册信息。
    

#### 统计与分析 (Statistics & Analytics)

- **`analytics_by_period`**, **`analytics_metadata`**, **`analytics_raw`**: 这些表用于 n8n 内置的**分析仪表盘**功能，收集工作流执行次数、成功率、执行时长等统计数据。
    
- **`workflow_statistics`**: 存储关于每个工作流的聚合统计信息。
    

#### 内部测试框架 (Internal Testing Framework)

- **`test_case_execution`**, **`test_definition`**, **`test_metric`**, **`test_run`**: 这些表是 n8n 自身开发和自动化测试使用的，与您的日常使用无关。
    

---

### 总结

这个视图清晰地展示了 n8n 是一个功能非常丰富的平台，它不仅仅是执行工作流，还内置了版本控制、用户权限管理、执行分析、自定义节点管理等多种高级功能。

您现在已经对 n8n 的“骨架”有了非常深入的了解！
![](../fujian/Pasted%20image%2020250825102949.png)
##  `workflow_entity` 这张核心表  

![](../fujian/Pasted%20image%2020250825104246.png)

太棒了！您现在看到的是 `workflow_entity` 这张核心表的“设计图纸”。这个 `\d` 命令的输出结果非常详细，它定义了存储一个工作流所需的所有数据字段以及它们之间的关系。

我们来逐一解析这个输出的各个部分：

---

### 1. 列 (Columns)

这部分定义了表的结构，即一个工作流包含哪些信息：

- **`name`**: 工作流的名称，就是您在 n8n 界面上看到的名字。
    
- **`active`**: 一个布尔值 (`true`/`false`)，标记这个工作流是**激活**状态还是**未激活**状态。
    
- **`nodes`**: **(核心字段)** 一个 `json` 字段，以 JSON 格式存储了工作流中**所有节点**的详细信息（节点类型、位置、参数设置等）。
    
- **`connections`**: **(核心字段)** 同样是 `json` 字段，存储了节点之间**所有连接线**的信息。
    
- **`createdAt` / `updatedAt`**: 时间戳，分别记录了工作流的创建时间和最后一次更新时间。
    
- **`settings`**: 一个 `json` 字段，存储这个工作流的特定设置（例如时区、错误处理工作流等）。
    
- **`staticData`**: 用于存储工作流的静态数据，通常包含 Webhook 的 URL 路径等不应改变的信息。
    
- **`pinData`**: 存储与工作流中被“钉住”的节点相关的数据。
    
- **`versionId`**: 此工作流**特定版本**的唯一 ID。
    
- **`triggerCount`**: 一个计数器，可能用于统计此工作流被触发的次数。
    
- **`id`**: **(主键)** 每个工作流的唯一标识符 (ID)。
    
- **`parentFolderId`**: 此工作流所属文件夹的 ID，用于实现文件夹组织功能。
    

---

### 2. 索引 (Indexes)

索引就像书的目录，能让数据库极快地根据特定列找到数据行，从而大大提高查询性能。

- `"workflow_entity_pkey" PRIMARY KEY, btree (id)`: 这是**主键索引**，确保每个工作流的 `id` 都是唯一的，并且能通过 `id` 进行超快速的查找。
    
- `"IDX_workflow_entity_name"`: 在 `name` 列上建立的索引，用于加速按工作流名称的搜索。
    
- `"pk_workflow_history" UNIQUE, btree (versionId, id)`: 这是一个**唯一约束索引**，它确保了 `versionId` 和 `id` 的组合是唯一的。这意味着对于同一个工作流 (`id`)，每一个版本 (`versionId`)都只能有一条记录，这是实现版本控制的关键。
    

---

### 3. 外键约束 (Foreign-key constraints)

外键是用来建立表与表之间链接的规则，确保数据的完整性和一致性。

- `"fk_workflow_parent_folder" ... REFERENCES folder(id) ON DELETE CASCADE`: 这条规则表示，`workflow_entity` 表中的 `parentFolderId` 必须对应 `folder` 表中一个真实存在的 `id`。
    
    - `ON DELETE CASCADE` 的意思是：如果一个文件夹被删除了，那么这个文件夹里的所有工作流也会被**级联删除**。
        

---

### 4. 被以下表引用 (Referenced by)

这个列表非常重要，它展示了**哪些其他的表依赖于 `workflow_entity` 表**，完美地说明了工作流是 n8n 各种数据的中心。

- **`execution_entity`**: 每一次的**执行记录**都必须关联到一个工作流。
    
- **`webhook_entity`**: 每一个 **Webhook** 都必须属于一个工作流。
    
- **`workflows_tags`**: **标签**通过这个中间表关联到工作流。
    
- ...以及分析、测试、分享等其他功能的数据表都通过 `workflowId` 链接回这张主表。
    

您会注意到很多都带有 `ON DELETE CASCADE`。这意味着如果一个工作流被删除，那么与它相关的所有执行记录、Webhook、统计数据等都会被自动一并删除，以保持数据干净整洁。

### 总结

通过这张“设计图”，我们可以清晰地看到：一个工作流的核心设计（节点和连接）被存储为 JSON，它拥有唯一的 ID，可以被组织在文件夹中，并且是大量其他数据（如执行历史、Webhook 等）的“父级”实体。


## 如何更好的查看表项
当然！在命令行中使用 `SELECT *` 查看数据确实很不方便，尤其是当表里有很多列，或者某些列（比如 JSON 字段）包含大量内容时，输出会非常混乱。

这里为您介绍两种更好的查看表项数据的方法：**优化命令行（`psql`）的显示方式** 和 **使用图形化界面（GUI）工具**。

---

### 方法一：在 `psql` 命令行中优化显示

您无需安装任何新工具，只需几个 `psql` 的内置命令和技巧，就能极大地改善查看体验。

#### 1. 使用“扩展显示”模式 (`\x`)

这是最有用的一个技巧。它会将一行记录的“横向”显示变为“纵向”的键值对格式。

- **开启扩展显示**: 在 `psql` 提示符后，输入 `\x` 然后按回车。
    
    SQL
    
    ```
    n8n=> \x
    Expanded display is on.
    ```
    
- 现在，当您再次查询时，结果会非常清晰：
    
    SQL
    
    ```
    -- 只看一条工作流的数据
    n8n=> SELECT * FROM workflow_entity LIMIT 1;
    ```
    
    **输出效果对比：**
    
    - **关闭 `\x` (默认)**: `id | name | active | nodes | connections ... (所有内容挤在一行)`
        
    - **开启 `\x`**:
        
        ```
        -[ RECORD 1 ]-+-------------------------------------------------
        id            | 1
        name          | My Awesome Workflow
        active        | t
        nodes         | {"nodes":[{"parameters":{...}}],"connections":{...}}
        createdAt     | 2025-08-24 22:40:00.12345-04
        ...           | ...
        ```
        

#### 2. 只选择您关心的列

不要总是用 `*` 查询所有列。只选择您想看的，可以让输出更简洁。

SQL

```
-- 只看工作流的 ID, 名称, 和是否激活
SELECT id, name, active FROM workflow_entity;
```

#### 3. 美化输出 JSON 字段

对于 `nodes`、`connections` 这种 JSON 字段，可以直接在 SQL 查询中使用 `jsonb_pretty()` 函数（如果列是 `jsonb` 类型）或 `json_pretty()`（如果列是 `json` 类型）来格式化输出。

SQL

```
-- 结合以上技巧：开启 \x 并美化输出 nodes 字段
n8n=> \x
n8n=> SELECT id, name, jsonb_pretty(nodes::jsonb) AS formatted_nodes FROM workflow_entity LIMIT 1;
```

`::jsonb` 是一个类型转换，确保 `jsonb_pretty` 函数能正常工作。这样输出的 `formatted_nodes` 字段就会是格式化、带缩进的 JSON，非常易读。

---

### 方法二：使用图形化界面 (GUI) 数据库工具（强烈推荐）

对于日常的数据浏览和查询，使用 GUI 工具是**最方便、最直观**的方式。它们就像是数据库的 Excel，您可以像浏览电子表格一样查看数据。

#### 1. 推荐的 GUI 工具

- **DBeaver**: **（首选推荐）** 功能强大、免费开源、跨平台（Windows/Mac/Linux），支持包括 PostgreSQL 在内的几乎所有数据库。
    
- **pgAdmin**: PostgreSQL 官方的开源管理工具，功能非常全面。
    
- **DataGrip**: 由 JetBrains 公司（开发 IntelliJ IDEA, WebStorm 的公司）出品，功能极其强大，是专业开发者的首选（此为付费软件，但提供试用）。
    

#### 2. 如何连接到 Docker 中的数据库

要让您电脑上的 GUI 工具连接到 Docker 容器里的 PostgreSQL，您需要**将容器的 5432 端口暴露给您的电脑**。

**第一步：修改 `docker-compose.yml` 文件**

在 `docker-compose.yml` 文件的 `postgres` 服务下，添加 `ports` 配置，就像 n8n 服务一样。

YAML

```
services:
  postgres:
    image: postgres:16
    restart: always
    environment:
      # ... (您已有的环境变量)
    volumes:
      # ... (您已有的数据卷)
    ports: # <--- 添加这个 ports 部分
      - "5432:5432" # 将主机的5432端口映射到容器的5432端口
    healthcheck:
      # ... (您已有的健康检查)

  n8n:
    # ... (n8n 服务的其余部分)
```

**第二步：重启 Docker Compose 服务**

修改并保存文件后，在 `docker-compose.yml` 所在的目录打开终端，运行以下命令来应用更改（它只会重建有变化的 `postgres` 服务，您的数据不会丢失）。

Bash

```
docker-compose up -d
```

**第三步：在 GUI 工具中配置连接**

现在您可以打开 DBeaver 或其他 GUI 工具，新建一个 PostgreSQL 连接，然后填入以下信息：

- **Host (主机)**: `localhost` (或 `127.0.0.1`)
    
- **Port (端口)**: `5432`
    
- **Database (数据库)**: 您在 `.env` 文件中定义的 `POSTGRES_DB` (例如: `n8n`)
    
- **User (用户)**: 您定义的 `POSTGRES_NON_ROOT_USER` (例如: `n8n_user`)
    
- **Password (密码)**: 您定义的 `POSTGRES_NON_ROOT_PASSWORD`
    

点击“连接”或“测试连接”，成功后您就可以在图形化界面中随意浏览所有的表和数据了！GUI 工具通常还内置了优秀的 JSON 查看器。