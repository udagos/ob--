import os
import shutil

def move_files_to_root(target_directory):
    """
    将指定目录下所有子文件夹中的文件移动到该(target_directory)目录下。

    :param target_directory: 要处理的目标根目录
    """
    
    # 确保目标目录是一个绝对路径，以便比较
    target_directory = os.path.abspath(target_directory)
    print(f"正在处理目录: {target_directory}\n")

    # 使用 os.walk 遍历目录树
    # topdown=False 意味着我们先访问子目录，再访问父目录
    # 这允许我们在处理完文件后安全地删除空目录
    for dirpath, dirnames, filenames in os.walk(target_directory, topdown=False):
        
        # 跳过根目录本身，我们只关心子目录
        if os.path.abspath(dirpath) == target_directory:
            continue

        print(f"--- 正在扫描子目录: {dirpath} ---")

        # 遍历当前子目录中的所有文件
        for filename in filenames:
            # 构造原始文件的完整路径
            source_file = os.path.join(dirpath, filename)
            
            # 构造目标路径（即根目录）
            dest_file = os.path.join(target_directory, filename)
            
            # --- 处理文件名冲突 ---
            # 如果文件在根目录中已存在，则重命名
            if os.path.exists(dest_file):
                # 分离文件名和扩展名
                base, ext = os.path.splitext(filename)
                counter = 1
                
                # 循环查找一个不存在的新文件名
                while True:
                    new_filename = f"{base}_{counter}{ext}"
                    new_dest_file = os.path.join(target_directory, new_filename)
                    if not os.path.exists(new_dest_file):
                        dest_file = new_dest_file
                        break
                    counter += 1
                print(f"  [注意] 文件名冲突: '{filename}' 将被重命名为 '{new_filename}'")

            # --- 移动文件 ---
            try:
                shutil.move(source_file, dest_file)
                print(f"  [成功] 已移动: {source_file} -> {dest_file}")
            except Exception as e:
                print(f"  [错误] 移动 '{source_file}' 时出错: {e}")

        # --- 尝试删除空的子目录 ---
        # 在移动所有文件后，尝试删除该目录
        try:
            # 检查目录是否真的为空
            if not os.listdir(dirpath):
                os.rmdir(dirpath)
                print(f"--- 已删除空目录: {dirpath} ---\n")
            else:
                print(f"--- 目录非空，未删除: {dirpath} (可能包含其他空文件夹) ---\n")
        except OSError as e:
            print(f"  [错误] 删除目录 '{dirpath}' 时出错: {e} (可能非空)\n")

# --- 主程序 ---
if __name__ == "__main__":
    # ------------------------------------------------------------------
    # !! 重要 !!
    # 请将下面的 '.' 替换为您要处理的目录的实际路径。
    # '.' 代表脚本所在的当前目录。
    # 示例:
    #   Windows: r"C:\Users\YourUser\Documents\MyFolder"
    #   Linux/Mac: "/home/YourUser/Documents/MyFolder"
    # ------------------------------------------------------------------
    
    PATH_TO_PROCESS = r'F:\新建文件夹\obin' 
    
    # 运行主函数
    try:
        if not os.path.isdir(PATH_TO_PROCESS):
            print(f"错误: 路径 '{PATH_TO_PROCESS}' 不是一个有效的目录。")
        else:
            move_files_to_root(PATH_TO_PROCESS)
            print("\n所有文件处理完毕。")
    except Exception as e:
        print(f"发生意外错误: {e}")

