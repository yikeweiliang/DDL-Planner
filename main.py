import sys
import datetime
import support as sp
import os
"""任务安排分为每日必做任务，ddl任务和某期前每日必做任务，每日必做的任务的属性：{名称，具体任务，每天需要多久，可否通勤时做}

需要填写的：任务名，任务类别，每天需要多少时间，能否兼容通勤，备注
任务名，任务类别，ddl日期，每天需要多少时间，能否兼容通勤，备注
任务名，任务类别，ddl日期，备注
任务名，任务类别，任务日期列表，任务每天所需时间段列表

"""
"""未来一天的时间表："""
class MISSIONS:
    def __init__(self, file_path):
        self.total_set = {}
        self.today = str(datetime.date.today())
        self.file_path = file_path



    def add_to_set(self, mission_name, lis):
        if mission_name not in self.total_set:
            self.total_set[mission_name] = {}
        self.total_set[mission_name]['class'] = lis[0]
        if lis[0] == '每日必做':
            self.total_set[mission_name]['time_needed'] = lis[1]
            if lis[2] == 'OK' or lis[2] == 'ok':
                self.total_set[mission_name]['commute'] = True
            else:
                self.total_set[mission_name]['commute'] = False
            self.total_set[mission_name]['remark'] = lis[3]
        elif lis[0] == '期前每日':
            self.total_set[mission_name]['ddl'] = lis[1]
            self.total_set[mission_name]['time_needed'] = lis[2]
            if lis[3] == 'OK' or lis[3] == 'ok':
                self.total_set[mission_name]['commute'] = True
            else:
                self.total_set[mission_name]['commute'] = False
            self.total_set[mission_name]['remark'] = lis[4]
        elif lis[0] == '普通ddl':
            self.total_set[mission_name]['ddl'] = lis[1]
            self.total_set[mission_name]['remark'] = lis[2]
        elif lis[0] == '直接安排':
            self.total_set[mission_name]['date_list'] = lis[1]
            self.total_set[mission_name]['time_plan_list'] = lis[2]
        else:
            pass
        self.total_set[mission_name]['done'] = False

    def get_set(self):
        return self.total_set
    
    def print_set(self):
        for mission_name, mission_info in self.total_set.items():
            print(f"missions: {mission_name}")
            for key, value in mission_info.items():
                print(f"  {key}: {value}")
            print()
    def done(self, mission_name):
        if mission_name in self.total_set:
            self.total_set[mission_name]['done'] = True
        else:
            print(f"Mission '{mission_name}' not found.")
    def update_mission(self, new_day = str(datetime.date.today())):
    
        if not new_day == self.today:
            list_of_done_missions = []
            list_of_not_done_missions = []
            for mission_name, mission_info in self.total_set.items():
                if mission_info['done']:
                    list_of_done_missions.append(mission_name)
                else:
                    list_of_not_done_missions.append(mission_name)
            with open(self.file_path+'\\log.txt', 'a', encoding='utf-8') as f:
                f.write(f"日期：{self.today}\n")
                f.write("已完成的任务：\n")
                for mission_name in list_of_done_missions:
                    f.write(f"  {mission_name}\n")
                f.write("未完成的任务：\n")
                for mission_name in list_of_not_done_missions:
                    f.write(f"  {mission_name}\n")
                f.write("\n")


            for mission_name, mission_info in self.total_set.items():
                if mission_info['class'] == '每日必做':
                    mission_info['done'] = False
                elif mission_info['class'] == '期前每日':
                    if sp.date_transform(str(datetime.date.today())) > sp.date_transform(mission_info['ddl']):
                        mission_info['done'] = True
                    else:
                        mission_info['done'] = False
            self.today = str(datetime.date.today())
        else:
            pass
    def display(self):
        print(f"今天是：{self.today}")
        print("今天的任务安排如下：")
        for mission_name, mission_info in self.total_set.items():
            if not mission_info['class'] == "直接安排":
                if not mission_info['done']:
                    if mission_info['class'] == '每日必做':
                        print(f"  {mission_name} (每日必做任务，需时{mission_info['time_needed']}小时，通勤可做：{mission_info['commute']})")
                    elif mission_info['class'] == '期前每日':
                        print(f"  {mission_name} (期前每日任务，ddl日期：{mission_info['ddl']}, 需时{mission_info['time_needed']}小时，通勤可做：{mission_info['commute']})")
                    elif mission_info['class'] == '普通ddl':
                        print(f"  {mission_name} (普通ddl任务，ddl日期：{mission_info['ddl']})")
            elif mission_info['class'] == "直接安排":
                if str(datetime.date.today()) in [str(i) for i in mission_info['date_list']]:
                    index = [str(i) for i in mission_info['date_list']].index(str(datetime.date.today()))
                    print(f"  {mission_name} (直接安排任务，今天的时间段为：{mission_info['time_plan_list'][index]})")

missions = MISSIONS(r'C:\Users\zheng\Desktop\PKU\Project\Latex\term\DDL')
missions.add_to_set('每日必做任务1', ['每日必做', 3, 'OK', '这是一个每日必做的任务'])
missions.add_to_set('期前每日任务1', ['期前每日', '2026-07-03', 4, 'NO', '这是一个期前每日的任务'])
missions.add_to_set('普通ddl任务1', ['普通ddl', '2026-07-14', '这是一个普通ddl任务'])
missions.add_to_set('直接安排任务1', ['直接安排', ['2026-06-28', '2026-06-29'], [[9, 11], [14, 16]]])   

missions.done('每日必做任务1')

missions.display()

missions.update_mission('2026-06-28')




missions.display()



