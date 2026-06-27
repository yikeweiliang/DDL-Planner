# -*- coding: utf-8 -*-
import sys, os, datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import MISSIONS

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex as rgb

# Color palette
BG = rgb("#F0F2F5")
PRIMARY = rgb("#1A73E8")
ACCENT = rgb("#34A853")
TEXT1 = rgb("#1F1F1F")
TEXT2 = rgb("#5F6368")
DONE = rgb("#BDBDBD")
WHITE = rgb("#FFFFFF")
CARD_BG = rgb("#FFFFFF")

# Use FangSong (simfang.ttf) directly - handles both Chinese and English
FONT = r"C:\Windows\Fonts\simfang.ttf"
Window.size = (420, 760)
Window.title = "DDL 任务规划器"


class StyledLabel(Label):
    def __init__(self, **kw):
        kw.setdefault("font_name", FONT)
        kw.setdefault("color", TEXT1)
        super().__init__(**kw)

class MGhostButton(Button):
    def __init__(self, **kw):
        kw.setdefault("font_name", FONT)
        kw.setdefault("size_hint", (0.7, None))
        kw.setdefault("height", dp(52))
        kw.setdefault("background_normal", "")
        kw.setdefault("background_color", WHITE)
        kw.setdefault("color", PRIMARY)
        kw.setdefault("bold", True)
        kw.setdefault("font_size", sp(16))
        super().__init__(**kw)

def TopBar(title, back_target=None, screen_ref=None):
    bar = BoxLayout(size_hint_y=None, height=dp(52), padding=[dp(4),0])
    with bar.canvas.before:
        from kivy.graphics import Color, Rectangle
        Color(1,1,1,1)
        Rectangle(pos=bar.pos, size=bar.size)
        bar.bind(pos=lambda w,v: setattr(bar.canvas.before.children[-1],"pos",v))
        bar.bind(size=lambda w,v: setattr(bar.canvas.before.children[-1],"size",v))
    if back_target and screen_ref:
        bk = Button(text="◀ 返回", font_name=FONT, size_hint=(0.2,1), height=dp(52),
            background_normal="", background_color=rgb("#E8F0FE"), color=PRIMARY, bold=True)
        bk.bind(on_press=lambda x, s=screen_ref, t=back_target: setattr(s.manager, "current", t))
        bar.add_widget(bk)
    else:
        bar.add_widget(Widget(size_hint_x=0.2))
    bar.add_widget(StyledLabel(text=title, font_size=sp(16), bold=True, halign="center", valign="middle", size_hint_x=0.6))
    bar.add_widget(Widget(size_hint_x=0.2))
    return bar

class MainScreen(Screen):
    def __init__(self, missions, **kw):
        super().__init__(**kw)
        self.m = missions
        outer = BoxLayout(orientation="vertical", padding=dp(30), spacing=dp(20))
        with outer.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.941,0.953,0.961,1)
            Rectangle(pos=outer.pos, size=outer.size)
            outer.bind(pos=lambda w,v: setattr(outer.canvas.before.children[-1],"pos",v))
            outer.bind(size=lambda w,v: setattr(outer.canvas.before.children[-1],"size",v))
        outer.add_widget(Widget())
        outer.add_widget(StyledLabel(text="📅 DDL 任务规划器", font_size=sp(26), bold=True, color=PRIMARY, size_hint_y=None, height=dp(60), halign="center", valign="middle"))
        outer.add_widget(StyledLabel(text=f"今天是: {missions.today}", font_size=sp(14), color=TEXT2, size_hint_y=None, height=dp(30), halign="center", valign="middle"))
        outer.add_widget(Widget(size_hint_y=0.1))
        # Three main buttons
        btn1 = MGhostButton(text="✏ 修改计划", background_color=PRIMARY, color=WHITE)
        btn1.bind(on_press=lambda x: setattr(self.manager, "current", "modify"))
        btn2 = MGhostButton(text="🔍 查看计划", background_color=ACCENT, color=WHITE)
        btn2.bind(on_press=lambda x: setattr(self.manager, "current", "view"))
        btn3 = MGhostButton(text="📋 查看日志", background_color=rgb("#FBBC04"), color=TEXT1)
        btn3.bind(on_press=self.show_log)
        outer.add_widget(btn1)
        outer.add_widget(Widget(size_hint_y=0.05))
        outer.add_widget(btn2)
        outer.add_widget(Widget(size_hint_y=0.05))
        outer.add_widget(btn3)
        outer.add_widget(Widget())
        self.add_widget(outer)

    def show_log(self, inst):
        content = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(16))
        scroll = ScrollView(bar_width=dp(4))
        try:
            log_path = os.path.join(self.m.file_path, "log.txt")
            with open(log_path, "r", encoding="utf-8") as lf:
                log_text = lf.read()
            if not log_text.strip(): log_text = "暂无日志记录"
        except:
            log_text = "日志文件读取失败"
        lbl = StyledLabel(text=log_text, font_size=sp(13), color=TEXT1, size_hint_y=None, halign="left", valign="top")
        lbl.bind(width=lambda w,v: setattr(lbl, "text_size", (v, None)))
        lbl.bind(texture_size=lambda w,v: setattr(lbl, "height", v[1]))
        scroll.add_widget(lbl)
        content.add_widget(scroll)
        close_btn = Button(text="关 闭", font_name=FONT, size_hint_y=None, height=dp(44),
            background_normal="", background_color=PRIMARY, color=WHITE, bold=True)
        popup = Popup(title=" 日 志 记 录 ", title_color=PRIMARY, title_size=sp(16), title_font=FONT,
            title_align="center", content=content)
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        popup.open()

class ModifyPlanScreen(Screen):
    def __init__(self, missions, **kw):
        super().__init__(**kw)
        self.m = missions
        outer = BoxLayout(orientation="vertical")
        with outer.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.941,0.953,0.961,1)
            Rectangle(pos=outer.pos, size=outer.size)
            outer.bind(pos=lambda w,v: setattr(outer.canvas.before.children[-1],"pos",v))
            outer.bind(size=lambda w,v: setattr(outer.canvas.before.children[-1],"size",v))
        outer.add_widget(TopBar("✏ 修改计划", "main", self))
        mid = BoxLayout(orientation="vertical", spacing=dp(30), padding=dp(40), size_hint_y=0.6, pos_hint={"center_y":0.5})
        mid.add_widget(Widget())
        add_btn = MGhostButton(text="➕ 添加计划", background_color=PRIMARY, color=WHITE)
        add_btn.bind(on_press=self.show_add)
        done_btn = MGhostButton(text="✅ 完成计划", background_color=ACCENT, color=WHITE)
        done_btn.bind(on_press=self.show_complete)
        mid.add_widget(add_btn)
        mid.add_widget(Widget(size_hint_y=0.1))
        mid.add_widget(done_btn)
        mid.add_widget(Widget())
        outer.add_widget(mid)
        self.add_widget(outer)

    def show_add(self, inst):
        AddTaskPopup(self.m, self.refresh_cb).open()
    def refresh_cb(self):
        pass
    def show_complete(self, inst):
        self.manager.get_screen("complete").refresh_tasks()
        self.manager.current = "complete"

class CompleteTasksScreen(Screen):
    def __init__(self, missions, **kw):
        super().__init__(**kw)
        self.m = missions
        outer = BoxLayout(orientation="vertical")
        with outer.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.941,0.953,0.961,1)
            Rectangle(pos=outer.pos, size=outer.size)
            outer.bind(pos=lambda w,v: setattr(outer.canvas.before.children[-1],"pos",v))
            outer.bind(size=lambda w,v: setattr(outer.canvas.before.children[-1],"size",v))
        outer.add_widget(TopBar("✅ 完成计划", "modify", self))
        self.scroll = ScrollView(bar_width=dp(4))
        self.task_grid = GridLayout(cols=1, spacing=dp(6), size_hint_y=None, padding=[dp(16),dp(8),dp(16),dp(8)])
        self.task_grid.bind(minimum_height=self.task_grid.setter("height"))
        self.scroll.add_widget(self.task_grid)
        outer.add_widget(self.scroll)
        self.add_widget(outer)

    def refresh_tasks(self):
        self.task_grid.clear_widgets()
        count = 0
        for name, info in self.m.total_set.items():
            if not info.get("done", False):
                count += 1
                card = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(56), padding=[dp(12),dp(6)])
                with card.canvas.before:
                    from kivy.graphics import Color, RoundedRectangle
                    Color(1,1,1,1)
                    RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(6)])
                    card.bind(pos=lambda w,v: setattr(card.canvas.before.children[-1],"pos",v))
                    card.bind(size=lambda w,v: setattr(card.canvas.before.children[-1],"size",v))
                cb = CheckBox(size_hint=(0.12,1), color=PRIMARY)
                nm = name
                cl = info.get("class","")
                cb.bind(active=lambda chk, v, n=nm, i=info: self.do_done(n, v))
                card.add_widget(cb)
                lbl = StyledLabel(text=f"{nm}  ({cl})", font_size=sp(14), size_hint=(0.88,1), halign="left", valign="middle")
                lbl.bind(size=lbl.setter("text_size"))
                card.add_widget(lbl)
                self.task_grid.add_widget(card)
        if count == 0:
            self.task_grid.add_widget(StyledLabel(text="🎉 所有任务已完成！", font_size=sp(16), color=TEXT2, size_hint_y=None, height=dp(60), halign="center", valign="middle"))

    def do_done(self, name, val):
        if val:
            self.m.done(name)
            self.refresh_tasks()

class ViewPlanScreen(Screen):
    def __init__(self, missions, **kw):
        super().__init__(**kw)
        self.m = missions
        outer = BoxLayout(orientation="vertical")
        with outer.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.941,0.953,0.961,1)
            Rectangle(pos=outer.pos, size=outer.size)
            outer.bind(pos=lambda w,v: setattr(outer.canvas.before.children[-1],"pos",v))
            outer.bind(size=lambda w,v: setattr(outer.canvas.before.children[-1],"size",v))
        outer.add_widget(TopBar("🔍 查看计划", "main", self))
        mid = BoxLayout(orientation="vertical", spacing=dp(30), padding=dp(40), size_hint_y=0.5, pos_hint={"center_y":0.5})
        mid.add_widget(Widget())
        today_btn = MGhostButton(text="📅 查看今日计划", background_color=PRIMARY, color=WHITE)
        today_btn.bind(on_press=lambda x: self.show_today())
        all_btn = MGhostButton(text="📂 查看所有计划", background_color=ACCENT, color=WHITE)
        all_btn.bind(on_press=lambda x: self.show_all())
        mid.add_widget(today_btn)
        mid.add_widget(Widget(size_hint_y=0.1))
        mid.add_widget(all_btn)
        mid.add_widget(Widget())
        outer.add_widget(mid)
        self.add_widget(outer)

    def show_today(self):
        self.manager.get_screen("today").refresh_tasks()
        self.manager.current = "today"
    def show_all(self):
        self.manager.get_screen("alltasks").refresh_tasks()
        self.manager.current = "alltasks"

class TodayPlanScreen(Screen):
    def __init__(self, missions, **kw):
        super().__init__(**kw)
        self.m = missions
        outer = BoxLayout(orientation="vertical")
        with outer.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.941,0.953,0.961,1)
            Rectangle(pos=outer.pos, size=outer.size)
            outer.bind(pos=lambda w,v: setattr(outer.canvas.before.children[-1],"pos",v))
            outer.bind(size=lambda w,v: setattr(outer.canvas.before.children[-1],"size",v))
        outer.add_widget(TopBar("📅 今日计划", "view", self))
        self.scroll = ScrollView(bar_width=dp(4))
        self.grid = GridLayout(cols=1, spacing=dp(6), size_hint_y=None, padding=[dp(16),dp(8)])
        self.grid.bind(minimum_height=self.grid.setter("height"))
        self.scroll.add_widget(self.grid)
        outer.add_widget(self.scroll)
        self.add_widget(outer)

    def refresh_tasks(self):
        self.grid.clear_widgets()
        count = 0
        for name, info in self.m.total_set.items():
            cls = info.get("class","")
            show = False
            if cls == "直接安排":
                ts = str(datetime.date.today())
                if ts in [str(d) for d in info.get("date_list",[])]: show = True
            else:
                if not info.get("done", False): show = True
            if not show: continue
            count += 1
            card = self.make_card(name, info)
            self.grid.add_widget(card)
        if count == 0:
            self.grid.add_widget(StyledLabel(text="🎉 今日无待办任务", font_size=sp(16), color=TEXT2, size_hint_y=None, height=dp(60), halign="center", valign="middle"))

    def make_card(self, name, info):
        card = BoxLayout(orientation="vertical", size_hint_y=None, padding=[dp(14),dp(10)])
        card.bind(minimum_height=card.setter("height"))
        card.height = dp(60)
        with card.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(1,1,1,1)
            RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(8)])
            card.bind(pos=lambda w,v: setattr(card.canvas.before.children[-1],"pos",v))
            card.bind(size=lambda w,v: setattr(card.canvas.before.children[-1],"size",v))
        cls = info.get("class","")
        detail = f"[{cls}]"
        if cls == "每日必做":
            t = info.get("time_needed","?")
            detail += f" 需{t}h"
            if info.get("commute"): detail += " 🚶可通勤"
        elif cls == "期前每日":
            ddl = info.get("ddl","?")
            t = info.get("time_needed","?")
            detail += f" DDL:{ddl} 需{t}h"
            if info.get("commute"): detail += " 🚶可通勤"
        elif cls == "普通ddl":
            ddl = info.get("ddl","?")
            detail += f" DDL:{ddl}"
        elif cls == "直接安排":
            dl = info.get("date_list",[])
            tl = info.get("time_plan_list",[])
            ts = str(datetime.date.today())
            if ts in [str(d) for d in dl]:
                idx = [str(d) for d in dl].index(ts)
                sl = tl[idx]
                detail += f" 今日 {sl[0]}:00-{sl[1]}:00"
        remark = info.get("remark","")
        if remark: detail += f" | {remark}"
        name_lbl = StyledLabel(text=name, bold=True, font_size=sp(15), size_hint_y=None, height=dp(24), halign="left", valign="middle")
        name_lbl.bind(size=name_lbl.setter("text_size"))
        det_lbl = StyledLabel(text=detail, font_size=sp(12), color=TEXT2, size_hint_y=None, height=dp(20), halign="left", valign="middle")
        det_lbl.bind(size=det_lbl.setter("text_size"))
        card.add_widget(name_lbl)
        card.add_widget(det_lbl)
        return card

class AllPlansScreen(Screen):
    def __init__(self, missions, **kw):
        super().__init__(**kw)
        self.m = missions
        outer = BoxLayout(orientation="vertical")
        with outer.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.941,0.953,0.961,1)
            Rectangle(pos=outer.pos, size=outer.size)
            outer.bind(pos=lambda w,v: setattr(outer.canvas.before.children[-1],"pos",v))
            outer.bind(size=lambda w,v: setattr(outer.canvas.before.children[-1],"size",v))
        outer.add_widget(TopBar("📂 全部计划", "view", self))
        self.scroll = ScrollView(bar_width=dp(4))
        self.grid = GridLayout(cols=1, spacing=dp(4), size_hint_y=None, padding=[dp(16),dp(8)])
        self.grid.bind(minimum_height=self.grid.setter("height"))
        self.scroll.add_widget(self.grid)
        outer.add_widget(self.scroll)
        self.add_widget(outer)

    def refresh_tasks(self):
        self.grid.clear_widgets()
        if not self.m.total_set:
            self.grid.add_widget(StyledLabel(text="暂无任务", size_hint_y=None, height=dp(40)))
            return
        for name, info in self.m.total_set.items():
            st = "✅" if info.get("done") else "⬜"
            cls = info.get("class","?")
            card = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(40), padding=[dp(12),dp(4)])
            with card.canvas.before:
                from kivy.graphics import Color, RoundedRectangle
                Color(1,1,1,1)
                RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(6)])
                card.bind(pos=lambda w,v: setattr(card.canvas.before.children[-1],"pos",v))
                card.bind(size=lambda w,v: setattr(card.canvas.before.children[-1],"size",v))
            done_flag = info.get("done", False)
            c = DONE if done_flag else TEXT1
            lbl = StyledLabel(text=f"{st}  {name}  ({cls})", font_size=sp(14), color=c, halign="left", valign="middle")
            lbl.bind(size=lbl.setter("text_size"))
            card.add_widget(lbl)
            self.grid.add_widget(card)


class AddTaskPopup(Popup):
    def __init__(self, missions_obj, on_success_callback, **kwargs):
        super().__init__(**kwargs)
        self.missions = missions_obj
        self.on_success = on_success_callback
        self.title = " "
        self.size_hint = (0.88, 0.82)
        self.background_color = WHITE
        self.separator_height = 0
        outer = BoxLayout(orientation="vertical", spacing=dp(6), padding=dp(20))
        tbar = BoxLayout(size_hint_y=None, height=dp(36))
        tbar.add_widget(Widget())
        ilbl = StyledLabel(text="➕ 添加新任务", bold=True, font_size=sp(18), color=PRIMARY, size_hint_x=0.7)
        tbar.add_widget(ilbl)
        tbar.add_widget(Widget())
        outer.add_widget(tbar)
        outer.add_widget(StyledLabel(text="任务名称", font_size=sp(13), color=TEXT2, size_hint_y=None, height=dp(20)))
        self.name_input = TextInput(multiline=False, font_name=FONT, size_hint_y=None, height=dp(38),
            background_color=rgb("#F0F2F5"), foreground_color=TEXT1, cursor_color=PRIMARY, padding=[dp(10),dp(2)])
        outer.add_widget(self.name_input)
        outer.add_widget(StyledLabel(text="任务类别", font_size=sp(13), color=TEXT2, size_hint_y=None, height=dp(20)))
        self.type_spinner = Spinner(text="每日必做",
            values=["每日必做","期前每日","普通ddl","直接安排"],
            font_name=FONT, size_hint_y=None, height=dp(38), background_color=rgb("#E8F0FE"),
            color=PRIMARY, size_hint=(0.5,None))
        self.type_spinner.bind(text=self.on_type_change)
        outer.add_widget(self.type_spinner)
        self.dynamic_box = BoxLayout(orientation="vertical", spacing=dp(8), size_hint_y=None)
        self.dynamic_box.bind(minimum_height=self.dynamic_box.setter("height"))
        outer.add_widget(self.dynamic_box)
        self.current_fields = []
        self.build_daily_fields()
        outer.add_widget(Widget(size_hint_y=0.01))
        btn_row = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(12))
        cancel_btn = Button(text="取 消", font_name=FONT, size_hint=(0.4,1),
            background_normal="", background_color=rgb("#F0F2F5"), color=TEXT1, bold=True)
        cancel_btn.bind(on_press=self.dismiss)
        submit_btn = Button(text="确 认添加", font_name=FONT, size_hint=(0.6,1),
            background_normal="", background_color=ACCENT, color=WHITE, bold=True)
        submit_btn.bind(on_press=self.submit)
        btn_row.add_widget(cancel_btn)
        btn_row.add_widget(submit_btn)
        outer.add_widget(btn_row)
        self.add_widget(outer)

    def clear_dynamic_fields(self):
        self.dynamic_box.clear_widgets(); self.current_fields = []

    def add_field(self, label, default=""):
        self.dynamic_box.add_widget(Widget(size_hint_y=None, height=dp(4)))
        self.dynamic_box.add_widget(StyledLabel(text=label, font_size=sp(13), color=TEXT2, size_hint_y=None, height=dp(22)))
        inp = TextInput(multiline=False, text=default, font_name=FONT, size_hint_y=None, height=dp(40),
            background_color=rgb("#F0F2F5"), foreground_color=TEXT1, padding=[dp(12),dp(8)])
        self.dynamic_box.add_widget(inp)
        self.current_fields.append(inp)

    def build_daily_fields(self):
        self.clear_dynamic_fields(); self.add_field("所需时间(小时):","1"); self.add_field("通勤可做? (OK/NO):","NO"); self.add_field("备注:")
    def build_before_ddl_fields(self):
        self.clear_dynamic_fields(); self.add_field("DDL日期 (YYYY-MM-DD):","2026-07-01"); self.add_field("所需时间(小时):","1"); self.add_field("通勤可做? (OK/NO):","NO"); self.add_field("备注:")
    def build_normal_ddl_fields(self):
        self.clear_dynamic_fields(); self.add_field("DDL日期 (YYYY-MM-DD):","2026-07-01"); self.add_field("备注:")
    def build_direct_fields(self):
        self.clear_dynamic_fields(); self.add_field("日期列表 (逗号分隔):"); self.add_field("时间段 (格式:9-11,14-16):")
    def on_type_change(self, sp, txt):
        if txt=="每日必做": self.build_daily_fields()
        elif txt=="期前每日": self.build_before_ddl_fields()
        elif txt=="普通ddl": self.build_normal_ddl_fields()
        elif txt=="直接安排": self.build_direct_fields()

    def submit(self, inst):
        name = self.name_input.text.strip()
        if not name: return
        tt = self.type_spinner.text
        try:
            if tt=="每日必做": lis=[tt,float(self.current_fields[0].text),self.current_fields[1].text.strip().upper(),self.current_fields[2].text.strip()]
            elif tt=="期前每日": lis=[tt,self.current_fields[0].text.strip(),float(self.current_fields[1].text),self.current_fields[2].text.strip().upper(),self.current_fields[3].text.strip()]
            elif tt=="普通ddl": lis=[tt,self.current_fields[0].text.strip(),self.current_fields[1].text.strip()]
            elif tt=="直接安排":
                dates=[d.strip() for d in self.current_fields[0].text.split(",") if d.strip()]
                times=[]
                for p in self.current_fields[1].text.split(","):
                    parts=p.strip().split("-")
                    if len(parts)==2: times.append([int(parts[0]),int(parts[1])])
                lis=[tt,dates,times]
            else: return
            self.missions.add_to_set(name, lis); self.dismiss()
            if self.on_success: self.on_success()
        except Exception as e:
            Popup(title=" ", content=StyledLabel(text="输入错误: "+str(e), font_size=sp(15), color=TEXT1, halign="center"), size_hint=(0.8,0.4), title_color=PRIMARY, title_size=sp(0)).open()


class DDLPlannerApp(App):
    def build(self):
        ddl_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        m = MISSIONS(ddl_path)
        sm = ScreenManager()
        sm.add_widget(MainScreen(m, name="main"))
        sm.add_widget(ModifyPlanScreen(m, name="modify"))
        sm.add_widget(ViewPlanScreen(m, name="view"))
        sm.add_widget(CompleteTasksScreen(m, name="complete"))
        sm.add_widget(TodayPlanScreen(m, name="today"))
        sm.add_widget(AllPlansScreen(m, name="alltasks"))
        return sm

if __name__ == "__main__":
    DDLPlannerApp().run()
