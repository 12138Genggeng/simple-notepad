import json #专门用来把列表/字典存在文件，这样关掉程序笔记不会消失。
import os #操作系统工具，可以判断文件有没有存在你的电脑里
FILE_NAME = "notes.json"
def load_notes():
    """从文件读取笔记，如果文件不存在就返回空列表"""
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []
def save_notes(notes):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)
def main():
    notes = load_notes()
    while True:
        print("\n=====简易记事本=====")
        print("1.添加笔记")
        print("2.查看所有笔记")
        print("3.删除一条笔记")
        print("4.退出")
        choice = input("请输入你的选择（1-4）：")
        if choice == "1":
            content = input("请输入笔记内容:")
            notes.append(content)
            save_notes(notes)
            print("笔记保存成功！")
        elif choice == "2":
            if len(notes) == 0:
                print("还没有任何笔记")
            else:
                print("\n所有笔记：")
                for idx, item in enumerate(notes):
                    print(f"[{idx+1}]{item}")
        elif choice == "3":
            if len(notes) == 0:
                print("没有笔记可以删除")
            else:
                try:
                    num = int(input("输入要删除的笔记编号："))
                    if 1 <= num <= len(notes):
                        del notes[num - 1]
                        save_notes(notes)
                        print("删除完成！")
                    else:
                        print("编号超出范围！")
                except ValueError:
                    print("请输入数字！")
        elif choice == "4":
            print("程序结束，笔记已经自动保存。")
            break
        else:
            print("无效输入，请输入1~4之间的数字")
if __name__=="__main__":
    main()



