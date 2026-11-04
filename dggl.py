# -*- coding: utf-8 -*-
"""
上班鼓励器 v4 - 可配置版
首次打开自己填上下班时间和日薪，保存后直接用
配置保存在同目录 config.json
"""
import tkinter as tk
from datetime import datetime, time, date
import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

DEFAULT_CONFIG = {
    "daily_wage": 250.0,
    "work_start": "09:00",
    "work_end": "19:00",
    "lunch_start": "12:00",
    "lunch_end": "13:00",
}

QUOTES_NEAR = [
    "快了快了，胜利就在前方",
    "最后冲刺阶段，坚持住",
    "马上就能解放了，再撑一下",
    "最后一程，工资马上到手",
    "胜利倒计时开启！",
]
QUOTES_MID = [
    "摸鱼也是工作的一部分",
    "你的时薪正在稳定上涨",
    "打工魂，人上人",
    "认真搬砖的样子最帅",
    "每一秒都是钱，别浪费",
    "再坚持一下，就下班了",
]
QUOTES_FAR = [
    "路还很长，喝口水慢慢来",
    "今天的努力，是明天的底气",
    "你的努力，时间看得见",
    "稳住，我们能赢",
    "今天也要元气满满",
]

BG = "#f5f5f7"
TEXT_DARK = "#1d1d1f"
TEXT_GRAY = "#86868b"
ACCENT_RED = "#ff3b30"
ACCENT_BLUE = "#007aff"
BORDER = "#e5e5ea"


def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except:
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()


def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def parse_time(s):
    h, m = s.split(":")
    return time(int(h), int(m))


class SettingsWindow:
    def __init__(self, parent, config, on_save):
        self.top = tk.Toplevel(parent)
        self.top.title("设置")
        self.top.configure(bg=BG)
        self.top.resizable(False, False)
        self.top.grab_set()

        w, h = 340, 360
        sw = self.top.winfo_screenwidth()
        sh = self.top.winfo_screenheight()
        self.top.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

        self.config = config
        self.on_save = on_save

        tk.Label(self.top, text="⚙️ 上班鼓励器设置", font=("Microsoft YaHei", 14, "bold"),
                 bg=BG, fg=TEXT_DARK).pack(pady=(16, 12))

        # 日薪
        row1 = tk.Frame(self.top, bg=BG)
        row1.pack(fill="x", padx=30, pady=4)
        tk.Label(row1, text="日薪（元）", font=("Microsoft YaHei", 11), bg=BG, fg=TEXT_DARK, width=12, anchor="w").pack(side="left")
        self.wage_entry = tk.Entry(row1, font=("Consolas", 12), width=10, justify="center")
        self.wage_entry.insert(0, str(config["daily_wage"]))
        self.wage_entry.pack(side="right")

        # 上班时间
        row2 = tk.Frame(self.top, bg=BG)
        row2.pack(fill="x", padx=30, pady=4)
        tk.Label(row2, text="上班时间", font=("Microsoft YaHei", 11), bg=BG, fg=TEXT_DARK, width=12, anchor="w").pack(side="left")
        self.start_entry = tk.Entry(row2, font=("Consolas", 12), width=10, justify="center")
        self.start_entry.insert(0, config["work_start"])
        self.start_entry.pack(side="right")

        # 下班时间
        row3 = tk.Frame(self.top, bg=BG)
        row3.pack(fill="x", padx=30, pady=4)
        tk.Label(row3, text="下班时间", font=("Microsoft YaHei", 11), bg=BG, fg=TEXT_DARK, width=12, anchor="w").pack(side="left")
        self.end_entry = tk.Entry(row3, font=("Consolas", 12), width=10, justify="center")
        self.end_entry.insert(0, config["work_end"])
        self.end_entry.pack(side="right")

        # 午休开始
        row4 = tk.Frame(self.top, bg=BG)
        row4.pack(fill="x", padx=30, pady=4)
        tk.Label(row4, text="午休开始", font=("Microsoft YaHei", 11), bg=BG, fg=TEXT_DARK, width=12, anchor="w").pack(side="left")
        self.lunch_s_entry = tk.Entry(row4, font=("Consolas", 12), width=10, justify="center")
        self.lunch_s_entry.insert(0, config["lunch_start"])
        self.lunch_s_entry.pack(side="right")

        # 午休结束
        row5 = tk.Frame(self.top, bg=BG)
        row5.pack(fill="x", padx=30, pady=4)
        tk.Label(row5, text="午休结束", font=("Microsoft YaHei", 11), bg=BG, fg=TEXT_DARK, width=12, anchor="w").pack(side="left")
        self.lunch_e_entry = tk.Entry(row5, font=("Consolas", 12), width=10, justify="center")
        self.lunch_e_entry.insert(0, config["lunch_end"])
        self.lunch_e_entry.pack(side="right")

        tk.Label(self.top, text="时间格式：HH:MM（如 09:00）", font=("Microsoft YaHei", 9),
                 bg=BG, fg=TEXT_GRAY).pack(pady=(8, 0))

        # 保存按钮
        tk.Button(self.top, text="保存并开始", font=("Microsoft YaHei", 12, "bold"),
                  bg="#1d1d1f", fg="white", activebackground="#333",
                  relief="flat", height=1, cursor="hand2",
                  command=self.save).pack(fill="x", padx=30, pady=(16, 0))

    def save(self):
        try:
            cfg = {
                "daily_wage": float(self.wage_entry.get()),
                "work_start": self.start_entry.get().strip(),
                "work_end": self.end_entry.get().strip(),
                "lunch_start": self.lunch_s_entry.get().strip(),
                "lunch_end": self.lunch_e_entry.get().strip(),
            }
            save_config(cfg)
            self.top.destroy()
            self.on_save(cfg)
        except Exception as e:
            tk.messagebox.showerror("错误", f"输入格式有误：{e}")


class SalaryWidget:
    def __init__(self, root, config):
        self.root = root
        self.update_config(config)

        self.root.title("上班鼓励器")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        w, h = 380, 560
        sw = self.root.winfo_screenwidth()
        self.root.geometry(f"{w}x{h}+{sw-w-40}+100")

        # 顶部
        top = tk.Frame(self.root, bg=BG)
        top.pack(fill="x", padx=16, pady=(12, 4))
        tk.Label(top, text="💧", font=("Segoe UI", 16), bg=BG, fg=TEXT_DARK).pack(side="left")
        tk.Label(top, text="上班鼓励器", font=("Microsoft YaHei", 13, "bold"),
                 bg=BG, fg=TEXT_DARK).pack(side="left", padx=6)
        tk.Label(top, text="⚙️ 设置", font=("Microsoft YaHei", 10),
                 bg=BG, fg=TEXT_GRAY, cursor="hand2").pack(side="right")
        top.winfo_children()[-1].bind("<Button-1>", lambda e: self.open_settings())

        self.date_label = tk.Label(self.root, text="", font=("Consolas", 10), bg=BG, fg=TEXT_GRAY)
        self.date_label.pack(anchor="w", padx=20, pady=(8, 0))

        self.status_label = tk.Label(self.root, text="", font=("Microsoft YaHei", 36, "bold"),
                                      bg=BG, fg=ACCENT_RED)
        self.status_label.pack(anchor="w", padx=20, pady=(4, 0))

        self.countdown_label = tk.Label(self.root, text="", font=("Microsoft YaHei", 13),
                                         bg=BG, fg=TEXT_DARK)
        self.countdown_label.pack(anchor="w", padx=20, pady=(4, 12))

        tk.Label(self.root, text="今日已赚", font=("Microsoft YaHei", 11),
                 bg=BG, fg=TEXT_GRAY).pack(anchor="w", padx=20)

        self.money_label = tk.Label(self.root, text="¥0.00000", font=("Consolas", 44, "bold"),
                                     bg=BG, fg=ACCENT_RED)
        self.money_label.pack(anchor="w", padx=16, pady=(0, 4))

        self.speed_label = tk.Label(self.root, text="", font=("Consolas", 11), bg=BG, fg=TEXT_GRAY)
        self.speed_label.pack(anchor="w", padx=20)

        self.quote_label = tk.Label(self.root, text="", font=("Microsoft YaHei", 10),
                                     bg=BG, fg=TEXT_GRAY, wraplength=340)
        self.quote_label.pack(anchor="w", padx=20, pady=(8, 8))

        tk.Button(self.root, text="退出计时", font=("Microsoft YaHei", 13, "bold"),
                  bg="#1d1d1f", fg="white", activebackground="#333",
                  relief="flat", height=2, cursor="hand2",
                  command=self.root.destroy).pack(fill="x", padx=20, pady=(4, 12))

        tk.Label(self.root, text="今日工时进度", font=("Microsoft YaHei", 10),
                 bg=BG, fg=TEXT_GRAY).pack(anchor="w", padx=20)
        self.progress_text = tk.Label(self.root, text="0.0%", font=("Microsoft YaHei", 10, "bold"),
                                       bg=BG, fg=TEXT_DARK)
        self.progress_text.pack(anchor="e", padx=20)

        self.pg_bg = tk.Frame(self.root, bg="#e5e5ea", height=8)
        self.pg_bg.pack(fill="x", padx=20, pady=(2, 4))
        self.pg_fill = tk.Frame(self.pg_bg, bg=ACCENT_BLUE, height=8)
        self.pg_fill.place(x=0, y=0, width=0, height=8)

        self.worked_text = tk.Label(self.root, text="", font=("Consolas", 10), bg=BG, fg=TEXT_GRAY)
        self.worked_text.pack(anchor="w", padx=20, pady=(0, 12))

        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=20, pady=4)

        row = tk.Frame(self.root, bg=BG)
        row.pack(fill="x", padx=20, pady=(8, 0))
        tk.Label(row, text="本月累计", font=("Microsoft YaHei", 11), bg=BG, fg=TEXT_DARK).pack(side="left")
        self.month_label = tk.Label(row, text="¥0.00000", font=("Consolas", 14, "bold"),
                                     bg=BG, fg=ACCENT_BLUE)
        self.month_label.pack(side="right")

        tk.Label(self.root, text="已过的日子按满勤补算，本月只计已赚，不含亏损。",
                 font=("Microsoft YaHei", 8), bg=BG, fg=TEXT_GRAY).pack(anchor="w", padx=20, pady=(2, 8))

        self.rate_label = tk.Label(self.root, text="", font=("Consolas", 11), bg=BG, fg=TEXT_DARK)
        self.rate_label.pack(anchor="w", padx=20)
        self.full_label = tk.Label(self.root, text="", font=("Consolas", 11), bg=BG, fg=TEXT_GRAY)
        self.full_label.pack(anchor="w", padx=20, pady=(2, 0))

        # 第一次启动：没有配置就弹设置
        if not os.path.exists(CONFIG_PATH):
            self.root.after(100, self.open_settings_first)
        else:
            self.update()

    def update_config(self, cfg):
        self.cfg = cfg
        self.DAILY_WAGE = float(cfg["daily_wage"])
        self.WORK_START = parse_time(cfg["work_start"])
        self.WORK_END = parse_time(cfg["work_end"])
        self.LUNCH_START = parse_time(cfg["lunch_start"])
        self.LUNCH_END = parse_time(cfg["lunch_end"])
        # 计算实际计薪秒数
        start_min = self.WORK_START.hour*60 + self.WORK_START.minute
        end_min = self.WORK_END.hour*60 + self.WORK_END.minute
        ls_min = self.LUNCH_START.hour*60 + self.LUNCH_START.minute
        le_min = self.LUNCH_END.hour*60 + self.LUNCH_END.minute
        work_minutes = (end_min - start_min) - (le_min - ls_min)
        self.WORK_SECONDS = work_minutes * 60
        self.PAID_HOURS = work_minutes / 60

    def open_settings_first(self):
        SettingsWindow(self.root, self.cfg, self.on_config_saved)

    def open_settings(self):
        SettingsWindow(self.root, self.cfg, self.on_config_saved)

    def on_config_saved(self, cfg):
        self.update_config(cfg)
        self.update()

    def is_workday(self, d):
        return d.weekday() < 5

    def monthly_earned(self):
        today = date.today()
        count = 0
        for day in range(1, today.day + 1):
            try:
                d = date(today.year, today.month, day)
                if self.is_workday(d):
                    count += 1
            except:
                pass
        return count * self.DAILY_WAGE

    def current_state(self):
        now = datetime.now()
        now_t = now.time()
        if now_t >= self.WORK_END:
            return self.DAILY_WAGE, "off", now
        if now_t < self.WORK_START:
            return 0.0, "before", now

        start_dt = datetime.combine(now.date(), self.WORK_START)
        lunch_s = datetime.combine(now.date(), self.LUNCH_START)
        lunch_e = datetime.combine(now.date(), self.LUNCH_END)

        if now < lunch_s:
            elapsed = (now - start_dt).total_seconds()
        elif now > lunch_e:
            elapsed = (lunch_s - start_dt).total_seconds() + (now - lunch_e).total_seconds()
        else:
            elapsed = (lunch_s - start_dt).total_seconds()

        salary = self.DAILY_WAGE * (elapsed / self.WORK_SECONDS)
        return min(max(salary, 0), self.DAILY_WAGE), "work", now

    def update(self):
        salary, state, now = self.current_state()
        month_total = self.monthly_earned()

        weekdays = ["周一","周二","周三","周四","周五","周六","周日"]
        self.date_label.config(text=f"{now.strftime('%Y-%m-%d')} {weekdays[now.weekday()]}")

        if state == "work":
            self.status_label.config(text="上班中", fg=ACCENT_RED)
            end_dt = datetime.combine(now.date(), self.WORK_END)
            remain = (end_dt - now).total_seconds()
            rh = int(remain // 3600)
            rm = int((remain % 3600) // 60)
            rs = int(remain % 60)
            self.countdown_label.config(text=f"距离下班还有 {rh}小时{rm}分{rs}秒")

            start_dt = datetime.combine(now.date(), self.WORK_START)
            lunch_s = datetime.combine(now.date(), self.LUNCH_START)
            lunch_e = datetime.combine(now.date(), self.LUNCH_END)
            if now < lunch_s:
                worked_sec = (now - start_dt).total_seconds()
            elif now > lunch_e:
                worked_sec = (lunch_s - start_dt).total_seconds() + (now - lunch_e).total_seconds()
            else:
                worked_sec = (lunch_s - start_dt).total_seconds()

            worked_hours = worked_sec / 3600
            pct = worked_sec / self.WORK_SECONDS

            self.worked_text.config(text=f"已工作 {worked_hours:.2f} / {self.PAID_HOURS:.2f} 小时")
            self.progress_text.config(text=f"{pct*100:.1f}%")
            self.pg_fill.place_configure(width=int(340 * pct))

            if remain < 3600:
                quote = QUOTES_NEAR[hash(str(now.minute)) % len(QUOTES_NEAR)]
            elif remain < 4*3600:
                quote = QUOTES_MID[hash(str(now.minute)) % len(QUOTES_MID)]
            else:
                quote = QUOTES_FAR[hash(str(now.minute)) % len(QUOTES_FAR)]
            self.quote_label.config(text=quote)

        elif state == "off":
            self.status_label.config(text="已下班", fg="#34c759")
            self.countdown_label.config(text="今日工资已结算")
            self.worked_text.config(text=f"已工作 {self.PAID_HOURS:.2f} / {self.PAID_HOURS:.2f} 小时")
            self.progress_text.config(text="100.0%")
            self.pg_fill.place_configure(width=340)
            self.quote_label.config(text="辛苦啦，明天继续加油！")
        else:
            self.status_label.config(text="未上班", fg=TEXT_GRAY)
            self.countdown_label.config(text="等待上班...")
            self.worked_text.config(text=f"已工作 0.00 / {self.PAID_HOURS:.2f} 小时")
            self.progress_text.config(text="0.0%")
            self.pg_fill.place_configure(width=0)
            self.quote_label.config(text="准备好迎接新的一天了吗？")

        per_sec = self.DAILY_WAGE / self.WORK_SECONDS
        self.money_label.config(text=f"¥{salary:.5f}")
        self.speed_label.config(text=f"当前赚钱速度 ¥{per_sec:.5f}/秒")
        self.month_label.config(text=f"¥{month_total:.5f}")

        hourly = self.DAILY_WAGE / self.PAID_HOURS
        self.rate_label.config(text=f"时薪 ¥{hourly:.2f}")
        self.full_label.config(text=f"今日满勤可得 ¥{self.DAILY_WAGE:.2f}")

        self.root.after(50, self.update)


if __name__ == "__main__":
    import tkinter.messagebox
    cfg = load_config()
    root = tk.Tk()
    app = SalaryWidget(root, cfg)
    root.mainloop()
