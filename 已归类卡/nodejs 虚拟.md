---
up:
  - "[[../moc/软件工程]]"
---



Node与Py不同，npm install默认直接在你的工程文件夹的node_modules里下载安装依赖，不会影响到全局，可以理解为默认就在一个虚拟环境中


[nodeJS](https://zhida.zhihu.com/search?content_id=371743447&content_type=Answer&match_order=1&q=nodeJS&zhida_source=entity)本身就是一个程序，每个依赖库都装在工程里，何来需要虚拟环境之说。若你真的还需要满足自己的伪需求，可以你复制一份nodeJS，到其他位置直接执行就可以了，要切换版本就下载不同的nodeJS版本或者使用 [npx](https://zhida.zhihu.com/search?content_id=371743447&content_type=Answer&match_order=1&q=npx&zhida_source=entity) n 命令切换即可。

  
### JavaScript 的虚拟环境

是的，JavaScript 生态系统也有类似的概念，主要通过 **Node.js 版本管理器** 和 **项目本地依赖** 来实现。

#### 1. Node.js 版本管理 (类似 `conda` 管理 Python 版本)

由于不同的项目可能需要不同版本的 Node.js，开发者通常会使用版本管理器来在它们之间轻松切换。

- **`nvm` (Node Version Manager)**: 这是最流行的 Node.js 版本管理器（主要用于 macOS/Linux）。
    - `nvm install 18`: 安装 Node.js v18。
    - `nvm use 16`: 在当前终端会话中切换到 Node.js v16。
    - `.nvmrc` 文件: 可以在项目根目录创建一个 `.nvmrc` 文件，写入版本号（如 `18.17.0`）。这样，当进入该目录时，可以运行 `nvm use` 来自动切换到项目指定的版本。
- **`nvm-windows`**, **`volta`**, **`fnm`**: 这些是其他流行的版本管理器，提供了跨平台支持或更快的性能。

#### 2. 项目本地依赖 (类似 `venv` 管理包)

JavaScript/Node.js 通过 `npm` (Node Package Manager) 或 `yarn` / `pnpm` 来管理项目依赖，其核心机制就是**本地化安装**。

- **`package.json`**: 这个文件定义了项目的所有元数据，包括其依赖项（在 `dependencies` 和 `devDependencies` 字段中）。
- **`node_modules` 目录**: 当你运行 `npm install` 时，`npm` 会读取 `package.json`，下载所有指定的包，并将它们安装到项目根目录下的 `node_modules` 文件夹中。
- **隔离机制**: 当你在项目中运行脚本或启动应用时（例如 `npm start`），Node.js 会自动在当前目录的 `node_modules` 文件夹中查找所需的模块。它不会去全局环境中查找，从而实现了项目间的包隔离。

**总结类比**

| Python 概念             | JavaScript 等价概念                          |
| --------------------- | ---------------------------------------- |
| **`venv`** (包隔离)      | **`node_modules` 目录** + `package.json`   |
| **`conda`** (环境/版本隔离) | **`nvm`** (或 `volta` 等) + `node_modules` |

因此，一个典型的 JavaScript 项目通过在其根目录中拥有自己的 `node_modules` 文件夹来获得与 Python `venv` 相同的包隔离效果，并通过使用 `nvm` 等工具来获得与 `conda` 类似的版本管理能力。
