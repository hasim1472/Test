"""현재 월의 양력/음력 달력을 표시하는 데스크톱 프로그램.

설치: pip install -r requirements.txt
실행: python lunar_calendar.py
"""
import calendar
from datetime import date
import tkinter as tk
from tkinter import font, messagebox

try:
    from korean_lunar_calendar import KoreanLunarCalendar
except ImportError:
    raise SystemExit(
        "음력 변환 라이브러리가 필요합니다. 다음 명령으로 설치하세요:\n"
        "pip install -r requirements.txt"
    )

WEEKDAYS = ["일", "월", "화", "수", "목", "금", "토"]


def lunar_label(year: int, month: int, day: int) -> str:
    converter = KoreanLunarCalendar()
    if not converter.setSolarDate(year, month, day):
        return "음력 변환 불가"
    leap = "윤" if converter.isIntercalation else ""
    return f"음력 {leap}{converter.lunarMonth}.{converter.lunarDay}"


class LunarCalendarApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.today = date.today()
        self.year, self.month = self.today.year, self.today.month
        self.root.title("양력 · 음력 달력")
        self.root.geometry("760x680")
        self.root.minsize(620, 570)

        self.normal_font = font.Font(family="맑은 고딕", size=17, weight="bold")
        self.small_font = font.Font(family="맑은 고딕", size=10)
        self.heading_font = font.Font(family="맑은 고딕", size=12, weight="bold")

        top = tk.Frame(root, bg="#ffffff", pady=14)
        top.pack(fill="x")
        tk.Button(top, text="◀ 이전 달", command=lambda: self.shift_month(-1)).pack(side="left", padx=16)
        self.title_label = tk.Label(top, font=("맑은 고딕", 20, "bold"), bg="#ffffff")
        self.title_label.pack(side="left", expand=True)
        tk.Button(top, text="다음 달 ▶", command=lambda: self.shift_month(1)).pack(side="right", padx=16)

        self.grid_frame = tk.Frame(root, bg="#dfe4ea")
        self.grid_frame.pack(expand=True, fill="both", padx=12, pady=12)
        self.draw()

    def shift_month(self, delta: int) -> None:
        total = self.year * 12 + (self.month - 1) + delta
        new_year, new_month_zero = divmod(total, 12)
        if not 1000 <= new_year <= 2050:
            messagebox.showinfo("이동 제한", "지원되는 음력 변환 연도 범위를 벗어났습니다.")
            return
        self.year, self.month = new_year, new_month_zero + 1
        self.draw()

    def draw(self) -> None:
        self.title_label.config(text=f"{self.year}년 {self.month}월")
        for child in self.grid_frame.winfo_children():
            child.destroy()

        for col, name in enumerate(WEEKDAYS):
            color = "#d64545" if col == 0 else "#3370b8" if col == 6 else "#343a40"
            cell = tk.Label(self.grid_frame, text=name, fg=color, bg="#f6f8fa", font=self.heading_font)
            cell.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

        cal = calendar.Calendar(firstweekday=6)
        weeks = cal.monthdayscalendar(self.year, self.month)
        for row in range(6):
            week = weeks[row] if row < len(weeks) else [0] * 7
            for col, day in enumerate(week):
                selected = day == self.today.day and (self.year, self.month) == (self.today.year, self.today.month)
                bg = "#eaf4ff" if selected else "#ffffff"
                frame = tk.Frame(self.grid_frame, bg=bg, highlightthickness=1 if selected else 0,
                                 highlightbackground="#5b9bd5")
                frame.grid(row=row + 1, column=col, sticky="nsew", padx=1, pady=1)
                if day:
                    fg = "#d64545" if col == 0 else "#3370b8" if col == 6 else "#222222"
                    tk.Label(frame, text=str(day), fg=fg, bg=bg, font=self.normal_font).pack(anchor="nw", padx=8, pady=(6, 0))
                    tk.Label(frame, text=lunar_label(self.year, self.month, day),
                             fg="#777777", bg=bg, font=self.small_font).pack(anchor="nw", padx=8, pady=(0, 5))

        for col in range(7):
            self.grid_frame.grid_columnconfigure(col, weight=1, uniform="dates")
        self.grid_frame.grid_rowconfigure(0, weight=0, minsize=38)
        for row in range(1, 7):
            self.grid_frame.grid_rowconfigure(row, weight=1, uniform="weeks")


if __name__ == "__main__":
    root = tk.Tk()
    LunarCalendarApp(root)
    root.mainloop()
