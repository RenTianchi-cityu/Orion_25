import os
import shutil

base_dir = 'data/bench2drive/v1'  # 你的camera文件夹路径

# 定义用于存储版本文件夹路径的字典
originals = {}
revisions = {}

# 获取所有项目（场景）文件夹，它们现在是顶层文件夹
project_folders = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
print(f"Found {len(project_folders)} projects/scenes in total: {project_folders}")

# 遍历每个项目文件夹
for project_name in project_folders:
    camera_dir_parent = os.path.join(base_dir, project_name, 'camera')
    
    # 检查是否存在 camera 文件夹
    if not os.path.exists(camera_dir_parent):
        continue

    # 遍历 camera 文件夹下的所有内容（可能是 front_original, back_revision 等）
    version_folders = os.listdir(camera_dir_parent)
    
    for version_folder in version_folders:
        full_version_path = os.path.join(camera_dir_parent, version_folder)
        
        # 确保它是一个目录
        if not os.path.isdir(full_version_path):
            continue

        # 提取 'original' 或 'revision' 之前的部分（例如 'front' 或 'back'）
        # 假设版本后缀仍然是 '_original' 或 '_revision' (9个字符)
        if version_folder.endswith('_original'):
            camera_name = version_folder[:-9] 
            # 独特的合并组键： 'scene001/front'
            key = f"{project_name}/{camera_name}" 
            originals[key] = full_version_path
        
        elif version_folder.endswith('_revision'):
            camera_name = version_folder[:-9]
            # 独特的合并组键： 'scene001/front'
            key = f"{project_name}/{camera_name}" 
            revisions[key] = full_version_path

print(f"Found {len(originals)} original groups and {len(revisions)} revision groups.")

# 找到有配对的组
groups = set(originals.keys()) & set(revisions.keys())

for group in groups:
    # group 的格式现在是 'project_name/camera_name'
    project_name, camera_name = group.split('/')
    
    orig_dir = originals[group]
    rev_dir = revisions[group]
    
    # 新的合并目录路径：data/bench2drive/v1/scene001/front
    # 将版本文件夹的内容合并到以 camera_name 命名的新文件夹中
    new_dir = os.path.join(base_dir, project_name, camera_name)
    os.makedirs(new_dir, exist_ok=True)

    # 获取所有文件名
    try:
        orig_files = set(os.listdir(orig_dir))
        rev_files = set(os.listdir(rev_dir))
    except FileNotFoundError as e:
        print(f"Error accessing files for group '{group}': {e}. Skipping.")
        continue


    print(f"Processing group '{group}': {len(orig_files)} original files, {len(rev_files)} revision files.")
    all_files = sorted(orig_files | rev_files)  # 按名字排序

    for fname in all_files:
        # Revision 优先逻辑不变
        src = os.path.join(rev_dir, fname) if fname in rev_files else os.path.join(orig_dir, fname)
        dst = os.path.join(new_dir, fname)
        
        # 检查源文件是否存在（以防集合操作后，文件被删除）
        if not os.path.exists(src):
             print(f"Warning: Source file {src} not found. Skipping {fname}.")
             continue
             
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
        # 如果目标文件已存在则跳过

print("合成完成！")