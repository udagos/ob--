---
up:
  - "[[docker]]"
---


```
volumes:
  mysql_data:
services:
  gemini-balance:
    image: ghcr.io/snailyp/gemini-balance:latest
    container_name: gemini-balance
    restart: unless-stopped
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      mysql:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "python -c \"import requests; exit(0) if requests.get('http://localhost:8000/health').status_code == 200 else exit(1)\""]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
  mysql:
    image: mysql:8
    container_name: gemini-balance-mysql
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: your_root_password
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    # ports:
    #   - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "127.0.0.1"]
      interval: 10s # 每隔10秒检查一次
      timeout: 5s   # 每次检查的超时时间为5秒
      retries: 3    # 重试3次失败后标记为 unhealthy
      start_period: 30s # 容器启动后等待30秒再开始第一次健康检查
```

好的，这是一个 `docker-compose.yml` 文件。它是一个用来定义和运行多容器 Docker 应用程序的配置文件。这个文件定义了两个服务（`gemini-balance` 和 `mysql`）以及一个用于数据持久化的卷（volume）。

下面是对这个配置文件的详细中文解释：

### 顶层的 `volumes`

YAML

```
volumes:
  mysql_data:
```

- **`volumes`**: 这个顶层关键字用来定义可以被此文件中各个服务使用的“命名卷”。
    
- **`mysql_data`**: 这里创建了一个名为 `mysql_data` 的命名卷。使用命名卷是 Docker 中持久化数据的首选方式。Docker 会在主机（你的电脑）上管理这个卷的存储位置。即使删除了容器，这个卷也不会被删除，从而确保你的 MySQL 数据是安全的。
    

### `services` (服务)

这个部分定义了组成你的应用程序的各个独立的容器。

#### 1. `gemini-balance` 服务

这个服务看起来是你的主应用程序。

YAML

```
services:
  gemini-balance:
    image: ghcr.io/snailyp/gemini-balance:latest
    container_name: gemini-balance
    restart: unless-stopped
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      mysql:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "python -c \"import requests; exit(0) if requests.get('http://localhost:8000/health').status_code == 200 else exit(1)\""]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
```

- **`image: ghcr.io/snailyp/gemini-balance:latest`**: 指定了这个服务（容器）要使用的 Docker 镜像。它会从 GitHub 容器镜像仓库 (ghcr.io) 拉取 `snailyp/gemini-balance` 镜像的 `latest` (最新) 版本。
    
- **`container_name: gemini-balance`**: 为这个容器设置一个自定义的名称，方便识别和管理。
    
- **`restart: unless-stopped`**: 这是一个重启策略。表示除非是你手动停止了容器，否则无论容器因何种原因停止，Docker 都会自动重启它。
    
- **`ports: - "8000:8000"`**: 将主机（你的电脑）的 8000 端口映射到容器的 8000 端口。这样，你就可以通过访问你电脑上的 `http://localhost:8000` 来访问容器内运行的应用程序。
    
- **`env_file: - .env`**: 告诉 Docker Compose 从与 `docker-compose.yml` 文件位于同一目录下的 `.env` 文件中加载环境变量。这是一种管理敏感信息（如 API 密钥或数据库凭证）的好方法。
    
- **`depends_on`**: 定义了此服务对其他服务的依赖关系。
    
    - **`mysql: condition: service_healthy`**: 这表示 `gemini-balance` 服务需要等待 `mysql` 服务不仅是启动了，而且是处于“健康”状态（基于 `mysql` 自己的 `healthcheck` 检查结果）之后，才会启动自己。这确保了应用程序在尝试连接数据库之前，数据库已经完全准备好了。
        
- **`healthcheck`**: 这部分定义了一个命令，用来检查容器是否处于健康状态。
    
    - **`test`**: 要运行的检查命令。这里使用了一段简短的 Python 脚本，向容器内的 `http://localhost:8000/health` 地址发送一个 HTTP GET 请求。如果返回的状态码是 200，脚本就以状态码 0 退出（表示健康）；否则以 1 退出（表示不健康）。
        
    - **`interval: 30s`**: 每隔 30 秒运行一次健康检查。
        
    - **`timeout: 5s`**: 每次检查必须在 5 秒内完成，否则视为失败。
        
    - **`retries: 3`**: 如果一次检查失败，Docker 会再重试 3 次。如果连续失败，容器就会被标记为“不健康”(unhealthy)。
        
    - **`start_period: 10s`**: 容器启动后，等待 10 秒再开始第一次健康检查。这给了应用程序一些初始化和启动的时间。
        

#### 2. `mysql` 服务

这个服务用来运行一个 MySQL 数据库。

YAML

```
  mysql:
    image: mysql:8
    container_name: gemini-balance-mysql
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: your_root_password
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    # ports:
    #   - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "127.0.0.1"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 30s
```

- **`image: mysql:8`**: 使用官方的 `mysql` 镜像，版本为 8。
    
- **`container_name: gemini-balance-mysql`**: 为 MySQL 容器设置一个自定义名称。
    
- **`restart: unless-stopped`**: 与 `gemini-balance` 服务使用相同的重启策略。
    
- **`environment`**: 在 MySQL 容器内部设置环境变量，这些变量会在数据库第一次启动时用来进行初始化配置。
    
    - **`MYSQL_ROOT_PASSWORD: your_root_password`**: **(注意)** 设置 MySQL 的 root 用户密码。你应该把 `"your_root_password"` 改成一个强密码。
        
    - **`MYSQL_DATABASE: ${MYSQL_DATABASE}`**: 创建一个新数据库，数据库的名称从 `.env` 文件中的 `MYSQL_DATABASE` 变量获取。
        
    - **`MYSQL_USER: ${MYSQL_USER}`**: 创建一个新用户，用户名从 `.env` 文件中的 `MYSQL_USER` 变量获取。
        
    - **`MYSQL_PASSWORD: ${MYSQL_PASSWORD}`**: 为上面创建的新用户设置密码，密码从 `.env` 文件中的 `MYSQL_PASSWORD` 变量获取。
        
- **`ports` (被注释掉了)**: `ports: - "3306:3306"` 这一部分被注释掉了（前面有 `#` 号）。这是一个很好的安全实践，意味着数据库的 3306 端口不会暴露到你的主机上。`gemini-balance` 服务仍然可以连接到它，因为它们在同一个 Docker 内部网络中。
    
- **`volumes: - mysql_data:/var/lib/mysql`**: 将前面定义的命名卷 `mysql_data` 挂载到容器内的 `/var/lib/mysql` 目录。这是 MySQL 存储其所有数据文件的地方。这样做可以确保即使 `mysql` 容器被删除和重建，你的所有数据库数据也都会被保留下来。
    ![](../fujian/Pasted%20image%2020250824114105.png)
- **`healthcheck`**: 定义了 Docker 如何检查 MySQL 服务是否正常运行。
    
    - **`test: ["CMD", "mysqladmin", "ping", "-h", "127.0.0.1"]`**: 这个命令使用 `mysqladmin` 工具来 ping 本地的 MySQL 服务。如果服务有响应，命令就会成功。
        
    - **`interval: 10s`**: 每 10 秒检查一次。
        
    - **`timeout: 5s`**: 检查超时时间为 5 秒。
        
    - **`retries: 3`**: 失败后重试 3 次。
        
    - **`start_period: 30s`**: 容器启动后等待 30 秒再开始第一次健康检查，给 MySQL 足够的时间来初始化。
        

### 总结

总而言之，这个 `docker-compose.yml` 文件定义了一个双层架构的应用：

1. 一个名为 `gemini-balance` 的后端应用程序。
    
2. 一个该应用程序所依赖的 MySQL 数据库。
    

这个配置非常健壮，它包含了为数据库做数据持久化、为两个服务设置健康检查以确保它们正常运行，以及设置了依赖条件来保证应用程序总是在数据库完全就绪后才启动。像数据库凭证这样的配置细节也被很好地外部化到了 `.env` 文件中，提高了安全性和可配置性。