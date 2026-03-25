import os
import sys
# 判断操作系统
is_windows = sys.platform == 'win32'
if not is_windows:
    import curses
def show_logo():
    print("""
    ╔═════════════════════════════════════╗
    ║                                     ║
    ║   ███████╗ █████╗ ███████╗██╗   ██╗ ║
    ║   ██╔════╝██╔══██╗██╔════╝╚██╗ ██╔╝ ║
    ║   █████╗  ███████║███████╗ ╚████╔╝  ║
    ║   ██╔══╝  ██╔══██║╚════██║  ╚██╔╝   ║
    ║   ███████╗██║  ██║███████║   ██║    ║
    ║   ╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ║
    ║                                     ║
    ║           EASY EDT v1.0             ║
    ║         简单好用的文本编辑器        ║
    ║            B站：云川星纪            ║
    ╚═════════════════════════════════════╝
    """)
def easyide_full(filepath):
    def editor(stdscr):
        curses.noecho()
        curses.raw()
        stdscr.keypad(True)
        curses.curs_set(1)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.read().split('\n')
        except:
            lines = ['']
        y, x = 0, 0
        scroll = 0          # 屏幕顶部行号
        
        while True:
            h, w = stdscr.getmaxyx()
            
            if h < 5 or w < 20:
                stdscr.clear()
                stdscr.addstr(0, 0, "窗口太小！")
                stdscr.refresh()
                stdscr.getch()
                continue
            line_num_width = len(str(len(lines))) + 2
            # 限制滚动范围
            max_scroll = max(0, len(lines) - (h - 2))
            scroll = max(0, min(scroll, max_scroll))
            # 光标自动跟随：保证光标在可见区域内
            if y < scroll:
                scroll = y
            elif y >= scroll + h - 2:
                scroll = y - (h - 3)
            # 再次限制
            scroll = max(0, min(scroll, max_scroll))
            # 全屏刷新（每次循环都刷新，保证行号正确）
            stdscr.clear()
            for i in range(scroll, min(len(lines), scroll + h - 2)):
                line = lines[i]
                try:
                    line_num = f"{i+1:>{line_num_width-1}} "
                    stdscr.addstr(i - scroll, 0, line_num, curses.A_DIM)
                    stdscr.addstr(i - scroll, line_num_width, line[:w-line_num_width-1])
                except:
                    pass
            # 状态栏
            short_name = os.path.basename(filepath)
            if len(short_name) > 20:
                short_name = short_name[:17] + "..."
            status = f" {short_name} {y+1}/{len(lines)}   Ctrl+S保存  Ctrl+Q退出  Ctrl+U上翻  Ctrl+D下翻  Tab缩进4空格 "
            try:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(h-1, 0, status[:w-1])
                stdscr.attroff(curses.A_REVERSE)
            except:
                pass
            # 光标定位
            try:
                stdscr.move(y - scroll, x + line_num_width)
            except:
                pass
            stdscr.refresh()
            key = stdscr.getch()
            # Ctrl+Q 退出
            if key == 17:
                break
            # Ctrl+S 保存
            elif key == 19:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))
                try:
                    stdscr.addstr(h-2, 0, " 已保存 ")
                    stdscr.refresh()
                    curses.napms(500)
                except:
                    pass
            # 普通字符
            elif 32 <= key <= 126:
                lines[y] = lines[y][:x] + chr(key) + lines[y][x:]
                x += 1
            # 回车
            elif key in (10, 13):
                lines.insert(y+1, lines[y][x:])
                lines[y] = lines[y][:x]
                y += 1
                x = 0
            # 退格
            elif key in (127, 8, curses.KEY_BACKSPACE):
                if x > 0:
                    lines[y] = lines[y][:x-1] + lines[y][x:]
                    x -= 1
                elif y > 0:
                    x = len(lines[y-1])
                    lines[y-1] += lines[y]
                    del lines[y]
                    y -= 1
            # Tab
            elif key == 9:
                lines[y] = lines[y][:x] + "    " + lines[y][x:]
                x += 4
            # 方向键
            elif key == curses.KEY_UP:
                if y > 0:
                    y -= 1
                    x = min(x, len(lines[y]))
            elif key == curses.KEY_DOWN:
                if y < len(lines) - 1:
                    y += 1
                    x = min(x, len(lines[y]))
            elif key == curses.KEY_LEFT:
                x = max(0, x-1)
            elif key == curses.KEY_RIGHT:
                x = min(len(lines[y]), x+1)
            # 翻页：Ctrl+U 上翻，Ctrl+D 下翻
            elif key == 21:  # Ctrl+U
                scroll = max(0, scroll - (h - 3))
                # 光标跟随翻页（可选：光标移到页面顶部）
                if y > scroll + (h - 3):
                    y = scroll + (h - 3)
                if y < scroll:
                    y = scroll
            elif key == 4:   # Ctrl+D
                scroll = min(max_scroll, scroll + (h - 3))
                if y < scroll:
                    y = scroll
                if y > scroll + (h - 3):
                    y = scroll + (h - 3)
    curses.wrapper(editor)
def easyide_simple(filepath):
    """Windows """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except:
        lines = []
    print("\n--- 编辑模式  ---")
    print("输入 :w 保存，:q 退出，直接输入文字添加行")
    print("当前文件:", filepath)
    while True:
        user_input = input(">>> ")
        if user_input == ":w":
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print("✅ 已保存")
        elif user_input == ":q":
            break
        else:
            lines.append(user_input + "\n")
            print(f"✅ 已添加第 {len(lines)} 行")
def main():
    show_logo()
    print("1. 新建文件")
    print("2. 打开文件")
    print("3. 看看logo")
    choice = input("请选择 (1/2/3): ").strip()
    if choice == "1":
        print("\n--- 新建文件 ---")
        path = input("保存路径 (留空为当前目录): ").strip()
        name = input("文件名: ").strip()
        ext = input("扩展名 (如 py, txt): ").strip()
        if path:
            filepath = os.path.join(path, f"{name}.{ext}")
        else:
            filepath = f"{name}.{ext}"
        # 检查路径是否是文件夹
        if os.path.isdir(filepath):
            print(f"❌ 错误：'{filepath}' 是一个文件夹，不能创建同名文件")
            return
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                pass
            print(f"✅ 已创建: {filepath}")
        except Exception as e:
            print(f"❌ 创建失败: {e}")
            return
    elif choice == "2":
        print("\n--- 打开文件 ---")
        filepath = input("文件路径(包括文件本身): ").strip()
        # 判断是否是文件夹
        if os.path.isdir(filepath):
            print(f"❌ 错误：'{filepath}' 是一个文件夹，不是文件")
            print("   请输入完整的文件路径，例如: C:\\Users\\xxx\\Desktop\\test.py")
            return
        if not os.path.exists(filepath):
            print(f"❌ 文件不存在: {filepath}")
            return
    elif choice == "3":
        show_logo()
        print("看完了？那下次见👋")
        return
    else:
        show_logo()
        print("没有这个选项，送你个 Logo，下次见～")
        return
    # 根据系统选择编辑器
    if is_windows:
        easyide_simple(filepath)
    else:
        easyide_full(filepath)
if __name__ == "__main__":
    main()