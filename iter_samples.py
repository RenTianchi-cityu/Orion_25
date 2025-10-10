import os

# ******** 請修改此處的路徑為您的三級目錄實際路徑 ********
TARGET_DIR = "/path/to/your/Level3/directory" 
# 範例：TARGET_DIR = "C:/Users/YourName/Documents/ProjectData"
# 範例：TARGET_DIR = "/home/user/data/project/level3"
# **********************************************************


def rename_revision_folders(target_path):
    """
    掃描目標目錄，將成對的 (base, base_revision) 文件夾重命名為 (base_backup, base)。
    """
    
    if not os.path.isdir(target_path):
        print(f"錯誤：指定的路徑 '{target_path}' 不是一個有效的目錄。")
        return

    print(f"--- 開始掃描目錄：{target_path} ---")
    
    # 1. 獲取目標目錄下的所有文件夾和文件
    all_items = os.listdir(target_path)
    
    # 2. 篩選出所有以 '_revision' 結尾的文件夾
    revision_folders = [
        item for item in all_items 
        if item.endswith("_revision") and os.path.isdir(os.path.join(target_path, item))
    ]
    
    if not revision_folders:
        print("未找到任何以 '_revision' 結尾的文件夾。")
        return

    for rev_folder_name in revision_folders:
        
        # 3. 提取基礎名稱 (e.g., 從 'front_revision' 提取 'front')
        base_name = rev_folder_name.replace("_revision", "")
        
        # 構建完整路徑
        base_path = os.path.join(target_path, base_name)
        rev_path = os.path.join(target_path, rev_folder_name)
        backup_path = os.path.join(target_path, f"{base_name}_backup")

        # 4. 檢查對應的基礎文件夾是否存在
        if os.path.isdir(base_path):
            print("-" * 30)
            print(f"發現一組匹配：原始='{base_name}'，修訂版='{rev_folder_name}'")
            
            try:
                # 步驟 A: 將原始文件夾重命名為 _backup
                # 'front' -> 'front_backup'
                os.rename(base_path, backup_path)
                print(f"  成功: '{base_name}' 重命名為 '{os.path.basename(backup_path)}'")
                
                # 步驟 B: 將 _revision 文件夾重命名為原始名稱
                # 'front_revision' -> 'front'
                os.rename(rev_path, base_path)
                print(f"  成功: '{rev_folder_name}' 重命名為 '{base_name}'")

            except OSError as e:
                print(f"  **錯誤: 在重命名過程中發生錯誤: {e}**")
                print("  請檢查文件夾權限或是否有其他程序正在使用這些文件。")
                
        else:
            print(f"--- 警告: 找到修訂版文件夾 '{rev_folder_name}'，但未找到對應的原始文件夾 '{base_name}'。跳過。")

    print(f"--- 處理完成。 ---")

# 執行函數
# rename_revision_folders(TARGET_DIR)