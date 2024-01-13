#!/bin/bash

# 获取当前工作目录
current_directory=$(pwd)

# 指定相对路径，可以根据需要修改
# relative_paths=("archive" "logs" "output")
relative_paths=("logs" "output")

suffix=("*mergeTrue*.txt" "*mergeTrue*.csv" "*mergeTrue*.xls")

# 指定目标路径，可以根据需要修改
absolute_paths=()

# 转换相对路径为绝对路径
target_paths=()
if [ ${#absolute_paths[@]} -ne 0 ]; then
    target_paths+=$absolute_paths
fi
for rel_path in "${relative_paths[@]}"; do
    abs_path="${current_directory}/${rel_path}"
    target_paths+=("$abs_path")
done

# 遍历目标路径
for path in "${target_paths[@]}"; do
    # 检查目录是否存在
    if [ -d "$path" ]; then
        # 根据规则列出文件
        files_to_delete=()
        for suf in "${suffix[@]}"; do
            files_to_delete+=($(find "$path" -type f -name "$suf"))
        done

        # 检查是否有文件需要删除
        if [ ${#files_to_delete[@]} -eq 0 ]; then
            echo "在目录 $path 中没有符合规则的文件需要删除。"
        else
            # 列出待删除的文件
            echo "在目录 $path 中找到以下文件需要删除："
            printf "%s\n" "${files_to_delete[@]}"

            # 询问用户是否删除文件
            read -p "是否删除这些文件？ (y/n): " choice
            case "$choice" in
                [Yy]|[Yy][Ee][Ss])
                    # 删除文件
                    rm -f "${files_to_delete[@]}"
                    echo "文件已删除。"
                    ;;
                [Nn]|[Nn][Oo])
                    echo "用户选择不删除文件。"
                    ;;
                *)
                    echo "无效的选择，不删除文件。"
                    ;;
            esac
        fi
    else
        echo "目录 $path 不存在。"
    fi
done