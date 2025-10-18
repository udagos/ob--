<%*
// --- 用户配置区 ---

  

// 1. 包含 up 属性的笔记，移动到此文件夹

const destinationFolder = "已归类卡";

  

// 2. 被链接的、且不含 up 属性的笔记 (MOC)，移动到此文件夹

const mocFolder = "moc";

  

// 3. 触发移动的元数据属性名

const triggerProperty = "up";

  

// --- 脚本核心代码 ---

  

/**

 * 移动文件的辅助函数，包含检查和创建文件夹的逻辑

 * @param {TFile} file - 要移动的文件

 * @param {string} folderPath - 目标文件夹路径

 */

async function moveFileToFolder(file, folderPath) {

    // 如果文件不存在或已在目标文件夹，则不执行任何操作

    if (!file || file.parent.path === folderPath) {

        return;

    }

  

    try {

        // 确保目标文件夹存在

        const folderExists = app.vault.getAbstractFileByPath(folderPath);

        if (!folderExists) {

            await app.vault.createFolder(folderPath);

            new Notice(`已创建文件夹: ${folderPath}`);

        }

  

        const newPath = `${folderPath}/${file.name}`;

        await app.fileManager.renameFile(file, newPath);

        new Notice(`文件 "${file.name}" 已移动到 ${folderPath}`);

  

    } catch (error) {

        console.error(`移动文件 ${file.path} 到 ${folderPath} 时出错:`, error);

        new Notice(`移动文件 "${file.name}" 时出错。`);

    }

}

  
  

/**

 * 检查单个文件并根据其元数据和链接的笔记来移动它。

 * @param {TFile} file - The file that was changed.

 * @returns {Promise<void>}

 */

async function checkAndMoveFile(file) {

    // 确保我们只处理 Markdown 文件

    if (!file || file.extension !== 'md') {

        return;

    }

  

    const frontmatter = app.metadataCache.getFileCache(file)?.frontmatter;

  

    // 条件1: 检查元数据是否存在，以及是否包含 'up' 属性

    if (!frontmatter || !(triggerProperty in frontmatter)) {

        return;

    }

    // 阶段一: 收集所有需要操作的信息

    let fileToMoveToMoc = null;

  

    let upLinkText = frontmatter[triggerProperty];

    if (Array.isArray(upLinkText)) {

        upLinkText = upLinkText[0];

    }

  

    // 修正后的逻辑：从wikilink中提取文件名

    let linkContent = null;

    if (typeof upLinkText === 'string') {

        const match = upLinkText.trim().match(/^\[\[([^|\]]+)/);

        if (match) {

            linkContent = match[1];

        }

    }

  

    if (linkContent) {

        const parentFile = app.metadataCache.getFirstLinkpathDest(linkContent, file.path);

  

        if (parentFile) {

            const parentFrontmatter = app.metadataCache.getFileCache(parentFile)?.frontmatter;

            if (!parentFrontmatter || !(triggerProperty in parentFrontmatter)) {

                fileToMoveToMoc = parentFile;

            }

        } else {

             new Notice(`警告: 链接的笔记 "${linkContent}" 不存在。`);

        }

        // 阶段二: 按顺序执行移动 (只有在是有效的wikilink时才移动)

        await moveFileToFolder(file, destinationFolder);

        if (fileToMoveToMoc) {

            await moveFileToFolder(fileToMoveToMoc, mocFolder);

        }

    }

}

  

// --- 防抖与事件监听 ---

  

// 用于存储每个文件路径的计时器

const debounceTimers = new Map();

  

/**

 * 防抖函数，确保 checkAndMoveFile 不会过于频繁地执行

 * @param {TFile} file - The file that was changed.

 */

function debouncedCheckAndMove(file) {

    // 如果该文件已有计时器，则清除它

    if (debounceTimers.has(file.path)) {

        clearTimeout(debounceTimers.get(file.path));

    }

  

    // 设置一个新的计时器

    const timer = setTimeout(() => {

        checkAndMoveFile(file);

        // 操作完成后，从 Map 中移除计时器

        debounceTimers.delete(file.path);

    }, 300); // 设置 300 毫秒的延迟

  

    // 将新的计时器存入 Map

    debounceTimers.set(file.path, timer);

}

  
  

// --- 脚本启动 ---

  

// 注册事件监听器，使用防抖函数来处理元数据变化

app.metadataCache.on('changed', debouncedCheckAndMove);

  

// 提示用户脚本已成功加载并正在运行

new Notice("智能归档脚本已启动（已修正链接解析）。");
%>