import os
import sqlite3
import sys

import psutil
import win32gui
import win32process

from pynput import keyboard


# 사용할 DB
db_path = os.getcwd()
print(db_path)
# subprocess로 실행시키면 실행 위치가 route와 같은 위치가 된다.
# conn = sqlite3.connect('%s\\static\\set_db\\UCP_Database.db' % db_path, check_same_thread=False)
conn = sqlite3.connect('../set_db/UCP_Database.db', check_same_thread=False)
cur = conn.cursor()


# # 키보드 에러 핸들링
class MyException(Exception):
    pass


class keyboardFunction:

    def __init__(self):
        super().__init__()

        self.listen_key = False

        self.all_key = [{"scroll_lock": keyboard.Key.scroll_lock}, {"insert": keyboard.Key.insert},
                        {"Shift": keyboard.Key.shift},
                        {"Shift": keyboard.Key.shift_l}, {"Shift": keyboard.Key.shift_r}, {"Alt": keyboard.Key.alt},
                        {"Alt": keyboard.Key.alt_l}, {"Alt": keyboard.Key.alt_r}, {"Ctrl": keyboard.Key.ctrl},
                        {"Ctrl": keyboard.Key.ctrl_l}, {"Ctrl": keyboard.Key.ctrl_r}, {"space": keyboard.Key.space},
                        {"tab": keyboard.Key.tab}, {"caps_lock": keyboard.Key.caps_lock}, {"cmd": keyboard.Key.cmd},
                        {"cmd": keyboard.Key.cmd_l}, {"cmd": keyboard.Key.cmd_r}, {"esc": keyboard.Key.esc},
                        {"Enter": keyboard.Key.enter}, {"End": keyboard.Key.end}, {"Home": keyboard.Key.home},
                        {"page_up": keyboard.Key.page_up}, {"page_down": keyboard.Key.page_down},
                        {"backspace": keyboard.Key.backspace}, {"delete": keyboard.Key.delete}, {"up": keyboard.Key.up},
                        {"down": keyboard.Key.down}, {"left": keyboard.Key.left}, {"right": keyboard.Key.right},
                        {"menu": keyboard.Key.menu}, {"pause": keyboard.Key.pause},
                        {"print_screen": keyboard.Key.print_screen},
                        {"media_next": keyboard.Key.media_next}, {"media_play_pause": keyboard.Key.media_play_pause},
                        {"media_previous": keyboard.Key.media_previous},
                        {"media_volume_down": keyboard.Key.media_volume_down},
                        {"media_volume_mute": keyboard.Key.media_volume_mute},
                        {"media_volume_up": keyboard.Key.media_volume_up},
                        {"F1": keyboard.Key.f1}, {"F2": keyboard.Key.f2}, {"F3": keyboard.Key.f3},
                        {"F4": keyboard.Key.f4}, {"F5": keyboard.Key.f5}, {"F6": keyboard.Key.f6},
                        {"F7": keyboard.Key.f7}, {"F8": keyboard.Key.f8}, {"F9": keyboard.Key.f9},
                        {"F10": keyboard.Key.f10}, {"F11": keyboard.Key.f11}, {"F12": keyboard.Key.f12},
                        {"F13": keyboard.Key.f13}, {"F14": keyboard.Key.f14}, {"F15": keyboard.Key.f15},
                        {"F16": keyboard.Key.f16}, {"F17": keyboard.Key.f17}, {"F18": keyboard.Key.f18},
                        {"F19": keyboard.Key.f19}, {"F20": keyboard.Key.f20},
                        {"`": keyboard.KeyCode(192)}, {"0": keyboard.KeyCode(48)},
                        {"1": keyboard.KeyCode(49)}, {"2": keyboard.KeyCode(50)},
                        {"3": keyboard.KeyCode(51)}, {"4": keyboard.KeyCode(52)},
                        {"5": keyboard.KeyCode(53)}, {"6": keyboard.KeyCode(54)},
                        {"7": keyboard.KeyCode(55)}, {"8": keyboard.KeyCode(56)},
                        {"9": keyboard.KeyCode(57)}, {"-": keyboard.KeyCode(189)},
                        {"=": keyboard.KeyCode(187)}, {"q": keyboard.KeyCode(81)},
                        {"w": keyboard.KeyCode(87)}, {"e": keyboard.KeyCode(69)},
                        {"r": keyboard.KeyCode(82)}, {"t": keyboard.KeyCode(84)},
                        {"y": keyboard.KeyCode(89)}, {"u": keyboard.KeyCode(85)},
                        {"i": keyboard.KeyCode(73)}, {"o": keyboard.KeyCode(79)},
                        {"p": keyboard.KeyCode(80)}, {"[": keyboard.KeyCode(221)},
                        {"]": keyboard.KeyCode(219)}, {"\\": keyboard.KeyCode(220)},
                        {"a": keyboard.KeyCode(65)}, {"s": keyboard.KeyCode(83)},
                        {"d": keyboard.KeyCode(68)}, {"f": keyboard.KeyCode(70)},
                        {"g": keyboard.KeyCode(71)}, {"h": keyboard.KeyCode(72)},
                        {"j": keyboard.KeyCode(74)}, {"k": keyboard.KeyCode(75)},
                        {"l": keyboard.KeyCode(76)}, {";": keyboard.KeyCode(186)},
                        {"'": keyboard.KeyCode(222)}, {"z": keyboard.KeyCode(90)},
                        {"x": keyboard.KeyCode(88)}, {"c": keyboard.KeyCode(67)},
                        {"v": keyboard.KeyCode(86)}, {"b": keyboard.KeyCode(66)},
                        {"n": keyboard.KeyCode(78)}, {"m": keyboard.KeyCode(77)},
                        {",": keyboard.KeyCode(188)}, {".": keyboard.KeyCode(190)},
                        {"/": keyboard.KeyCode(191)}, {"한영": keyboard.KeyCode(21)},
                        {"한자": keyboard.KeyCode(25)}]

        self.COMBINATIONS = [{'L1/touch4': [keyboard.Key.f9]},
                             {'L2/touch4': [keyboard.Key.alt_l, keyboard.Key.f2]},
                             {'L3/touch4': [keyboard.Key.f2]},
                             {'L4/touch4': [keyboard.Key.f4]},
                             {'L5/touch4': [keyboard.Key.alt_l, keyboard.Key.f3]},
                             {'L6/touch4': [keyboard.Key.alt_l, keyboard.Key.f12]},
                             {'L7/touch4': [keyboard.Key.alt_l, keyboard.Key.f9]},
                             {'L8/touch4': [keyboard.Key.ctrl_l, keyboard.Key.shift]}]

        # 현재 입력받은 키
        self.currentValue = []

        self.keyAction = keyboard.Controller()

    #########################################
    # 현재 활성화된 app의 process name을 확인
    def funWin(self):
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        return psutil.Process(pid[-1]).name()
    
    #########################################
    # 현재 활성화된 browser의 title을 확인
    def currentURL(self):
        hwnd = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(hwnd)

    #########################################
    # Windows Default 단축키 실행 함수
    def windowsDefault(self, i_key, cmd_id):
        print(i_key)
        print(cmd_id)
        cur.execute("SELECT shortcut FROM Command WHERE cmd_id=%s" % cmd_id)
        action_key = cur.fetchall()[0][0]
        self.keyAction.release(i_key)
        action_key = action_key.split("+")
        print(action_key)
        for i in range(len(action_key)):
            for k in self.all_key:
                if k.get(action_key[i]) is not None:
                    self.keyAction.press(k.get(action_key[i]))
                    break

        for i in reversed(range(len(action_key))):
            for k in self.all_key:
                if k.get(action_key[i]) is not None:
                    self.keyAction.release(k.get(action_key[i]))
                    break

    # Windows가 아닌 활성화된 app에 대응하는 단축키 실행 함수
    def otherApplication(self, i_key, cmd_id):
        print(i_key)
        print(cmd_id)
        cur.execute("SELECT shortcut FROM Command WHERE cmd_id=%s" % cmd_id)
        action_key = cur.fetchall()[0][0]
        self.keyAction.release(i_key)
        action_key = action_key.split("+")
        print(action_key)
        for i in range(len(action_key)):
            for k in self.all_key:
                if k.get(action_key[i]) is not None:
                    self.keyAction.press(k.get(action_key[i]))
                    break

        for i in reversed(range(len(action_key))):
            for k in self.all_key:
                if k.get(action_key[i]) is not None:
                    self.keyAction.release(k.get(action_key[i]))
                    break

    #########################################
    def keyMapping(self, key, gesture):
        print(gesture)
        browser = ['msedge.exe', 'firefox.exe', 'iexplore.exe', 'chrome.exe']
        gesture = gesture.split('/')
        # 동작을 위해 필요한 정보: 단축키, process_name, app_name
        # ges_id 조회
        cur.execute("SELECT ges_id FROM Gesture WHERE ges_name='%s' AND touch='%s'" % (gesture[0], gesture[1]))
        ges_id = cur.fetchall()
        ges_id = ges_id[0][0]
        # acc_id 조회
        cur.execute("SELECT acc_id FROM Use_Set WHERE ges_id=%s" % ges_id)
        acc_id = cur.fetchall()
        # 아직 설정하지 않은 제스처일 경우 acc_id=[]가 된다. acc_id=[]이라면
        if not acc_id:
            print("이건 아직 등록되지 않은 제스처에요~")
        else:
            # acc_id로 세팅된 (app, cmd)id 데이터 조회
            app_cmd_ids = []
            for ai in acc_id:
                cur.execute("SELECT app_id, cmd_id FROM AppCmd_Combi WHERE acc_id = %s" % str(ai[0]))
                app_cmd_ids.append(cur.fetchall()[0])
            # app_id로 process_name을 조회하여 현재 활성화된 app의 process name과 비교
            for ac_c in app_cmd_ids:
                cur.execute("SELECT process_name, browser_name FROM Application WHERE app_id = %s" % str(ac_c[0]))
                pb_name = cur.fetchall()[0]
                # print(pb_name)
                # # 활성화된 app에 해당하는 cmd_id를 otherApplication에 전달
                if pb_name[0] == self.funWin():
                    self.otherApplication(key, ac_c[1])
                    break
                elif pb_name[0] == 'browser':
                    if self.funWin() in browser:
                        if pb_name[1] in self.currentURL() and 'YouTube' in self.currentURL():
                            self.otherApplication(key, ac_c[1])
                            break
                        elif pb_name[1] in self.currentURL() and 'Netflix' in self.currentURL():
                            self.otherApplication(key, ac_c[1])
                            break
                elif pb_name[0] == 'default':
                    self.windowsDefault(key, ac_c[1])

    def execute(self, cur_key):
        print(cur_key)
        # cur_key로 현재 제스처와 터치가 무엇인지 판별
        for i in range(len(self.COMBINATIONS)):
            if cur_key == list(self.COMBINATIONS[i].values())[0]:
                # 확인된 gesture를 파라미터로 keyMapping함수 호출
                self.keyMapping(cur_key[0], list(self.COMBINATIONS[i].keys())[0])
        if len(self.currentValue) > len(self.COMBINATIONS):
            print(self.currentValue)
            self.currentValue.clear()

    def keyFunction(self):
        COMBINATIONS = self.COMBINATIONS
        cur_key = []
        all_key = []
        all_key = self.all_key

        # 키보드 클릭시(press) 아래 함수 실행
        def on_press(key):
            try:
                for i in COMBINATIONS:
                    for j in i.values():
                        for k in j:
                            if key == k:
                                if not cur_key:
                                    cur_key.append(key)
                                else:
                                    for t in cur_key:
                                        if key != t:
                                            print("첨들어가는 키")
                                            cur_key.append(key)
                                        elif key == t:
                                            print("반복")
                                raise NotImplementedError
                            else:
                                pass
            except NotImplementedError:
                pass

        def on_release(key):
            try:
                for m in COMBINATIONS:
                    for n, l in m.items():
                        if cur_key == l:
                            self.execute(l)
                            raise NotImplementedError
            except NotImplementedError:
                pass
            try:
                cur_key.clear()
            except KeyError:
                pass

        # 키보드 예외처리도 고려
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            try:
                listener.join()
            except MyException as e:
                print('{0} was pressed'.format(e.args[0]))


def main():
    peroAction = keyboardFunction()
    peroAction.keyFunction()
    sys.exit(peroAction.exec_())


if __name__ == '__main__':
    main()
