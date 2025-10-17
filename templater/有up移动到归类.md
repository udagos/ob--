<%*
// --- 用户配置区 ---

  

// 1. 目标文件夹名称

// 当笔记满足条件时，将会被移动到这个文件夹。

const destinationFolder = "已归类卡";

  

// 2. 触发移动的元数据属性名

// 脚本会检查笔记的元数据中是否存在这个键（key）。

const triggerProperty = "up";

  

// --- 脚本核心代码 ---

  

/**

 * 检查单个文件并根据其元数据移动它。

 * 这是被事件监听器调用的核心函数。

 * @param {TFile} file - The file to check.

 * @returns {Promise<void>}

 */

async function checkAndMoveFile(file) {

    // 确保我们只处理 Markdown 文件

    if (!file || file.extension !== 'md') {

        return;

    }

  

    try {

        const frontmatter = app.metadataCache.getFileCache(file)?.frontmatter;

        const currentFolder = file.parent.path;

  

        // 条件：元数据存在、包含触发属性、且当前不在目标文件夹内

        if (frontmatter && triggerProperty in frontmatter && currentFolder !== destinationFolder) {

            // 确保目标文件夹存在

            const destinationExists = app.vault.getAbstractFileByPath(destinationFolder);

            if (!destinationExists) {

                await app.vault.createFolder(destinationFolder);

                new Notice(`已创建文件夹: ${destinationFolder}`);

            }

  

            const newPath = `${destinationFolder}/${file.name}`;

            await app.fileManager.renameFile(file, newPath);

            new Notice(`文件 "${file.name}" 已自动归档。`);

        }

    } catch (error) {

        console.error(`自动归档文件 ${file.path} 时出错:`, error);

        new Notice(`自动归档文件 "${file.name}" 时出错。`);

    }

}

  

// --- 脚本启动与事件监听 ---

  

// 1. 注册一个事件监听器，当任何文件的元数据发生变化时触发

// 这使得脚本能够自动响应你对 frontmatter 的修改

app.metadataCache.on('changed', checkAndMoveFile);

  

// 2. 提示用户脚本已成功加载并正在运行

new Notice("自动归档脚本已启动，将实时监控文件元数据变化。");
%>