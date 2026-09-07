import json
import os
from datetime import datetime
FILE_NAME = "notes.json"


def load_notes():
    """从文件读取笔记，如果文件不存在就返回空列表"""
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("\n notes.json 文件损坏，已重置为空笔记库")
            return[]
    else:
        return []


def save_notes(notes):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)


def get_new_id(notes):
    """生成不重复ID：取现有最大ID+1，无笔记返回1"""
    if not notes:
        return 1
    max_id = max(n["id"] for n in notes)
    return max_id + 1


def export_note_to_txt(note, save_path):
    """导出单条笔记到txt"""
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(f"笔记ID: {note['id']}\n")
        f.write(f"标题: {note['title']}\n")
        f.write(f"创建时间: {note['create_time']}\n")
        f.write(f"修改时间: {note['update_time']}\n")
        f.write("=" * 40 + "\n")
        f.write(note["content"])


def export_all_notes(notes, save_path="all_notes.txt"):
    """导出全部笔记到同一个txt"""
    with open(save_path, "w", encoding="utf-8") as f:
        for note in notes:
            f.write(f"【ID:{note['id']}】 {note['title']}\n")
            f.write(f"创建:{note['create_time']} 修改:{note['update_time']}\n")
            f.write("-" * 50 + "\n")
            f.write(note["content"])
            f.write("\n" + ("=" * 60) + "\n\n")


def main():
    notes = load_notes()
    while True:
        print("\n=====简易记事本=====")
        print("1.添加笔记")
        print("2.查看所有笔记")
        print("3.删除一条笔记")
        print("4.修改笔记")
        print("5.搜索笔记")
        print("6.退出")
        choice = input("请输入你的选择（1-6）:")
        if choice == "1":
            title = input("请输入笔记标题：")
            print("请输入笔记内容，可多行输入，输入#end结束：")
            content_lines = []
            while True:
                line = input()
                end_flag = False
                if "#end" in line:
                    content_part = line.split("#end")[0]
                    if content_part.strip() != "":
                        content_lines.append(content_part)
                    end_flag = True
                else:
                    content_lines.append(line)
                if end_flag:
                    break
            new_note = {
                "id": len(notes)+1,
                "title": title,
                "content": "\n".join(content_lines),
                "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            notes.append(new_note)
            save_notes(notes)
            print("笔记保存成功！")
        elif choice == "2":
            if len(notes) == 0:
                print("还没有任何笔记")
            else:
                print("\n所有笔记（最新笔记在前）：")
                # 按修改时间倒序展示
                sorted_notes = sorted(notes, key=lambda x: x["update_time"], reverse=True)
                for note in sorted_notes:
                    print(f"\n【ID:{note['id']}】{note['title']}")
                    print(f"创建：{note['create_time']} | 修改：{note['update_time']}")
                    print("-" * 35)
                    preview = note['content'][:80] + ("..." if len(note['content']) > 80 else "")
                    print(preview)
                    print("-" * 35)
        elif choice == "3":
            if len(notes) == 0:
                print("没有笔记可以删除")
            else:
                try:
                    num = int(input("输入要删除的笔记ID："))
                    target_idx = None
                    for i, n in enumerate(notes):
                        if n["id"] == num:
                            target_idx = i
                            break
                    if target_idx is not None:
                        notes.pop(target_idx)
                        save_notes(notes)
                        print("删除完成！")
                    else:
                        print("该ID不存在！")
                except ValueError:
                    print("请输入数字ID！")
        elif choice == "4":
            if len(notes) == 0:
                print("还没有任何笔记")
            else:
                try:
                    num = int(input("请输入需要修改的笔记的ID："))
                    target = None
                    idx = None
                    for i, n in enumerate(notes):
                        if n["id"] == num:
                            target = n
                            idx = i
                            break
                    if target is not None:
                        new_title = input("请输入新标题：")
                        print("请输入新内容，以#end结束：")
                        lines = []
                        while True:
                            line = input()
                            end_flag = False
                            if "#end" in line:
                                content_part = line.split("#end")[0]
                                if content_part.strip() != "":
                                    lines.append(content_part)
                                end_flag = True
                            else:
                                lines.append(line)
                            if end_flag:
                                break
                        new_content = "\n".join(lines)
                        notes[idx]["title"] = new_title
                        notes[idx]["content"] = new_content
                        notes[idx]["update_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        save_notes(notes)
                        print("修改完成！")
                    else:
                        print("没有找到这个ID的笔记！")
                except ValueError:
                    print("请输入数字ID！")
        elif choice == "5":
            keyword = input("请输入搜索关键词：").strip()
            if not keyword:
                print("关键词不能为空！")
                continue
            find_count = 0
            print("\n-----搜索结果-----")
            for note in notes:
                if keyword in note["title"] or keyword in note["content"]:
                    print(f"笔记ID：{note['id']}|标题：{note['title']}|{note['create_time']}")
                    find_count += 1
            if find_count == 0:
                print("未找到匹配的笔记")
            print("--------------\n")
        elif choice == "6":
            print("程序结束，笔记已经自动保存。")
            break
        else:
            print("无效输入，请输入1~6之间的数字")


if __name__ == "__main__":
    main()
