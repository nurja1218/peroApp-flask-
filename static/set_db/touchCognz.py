import os
import sqlite3

from pynput import keyboard

# 사용할 DB
db_path = os.getcwd()
print(db_path)
conn = sqlite3.connect('%s\\static\\set_db\\UCP_Database.db' % db_path, check_same_thread=False)
# conn = sqlite3.connect('../set_db/UCP_Database.db', check_same_thread=False)
cur = conn.cursor()

controller = keyboard.Controller()

touch_state = []
data_check = False
td = ""


def f_key_test(ts):
    if not ts:
        pass
    else:
        print(ts)
        cur.execute("SELECT td_id FROM Touch_check")
        td_id = cur.fetchall()[0][0]
        print(type(td_id))
        cur.execute('''UPDATE Touch_check
                        SET d1 = %s, d2 = %s, d3 = %s
                        WHERE td_id = %d''' % (ts[0], ts[1], ts[2], td_id))
        conn.commit()


def on_press(key):
    if type(key) == keyboard.Key:
        print("text 데이터 아님")
    else:
        cur_key = key.char
        if cur_key is not None:
            touch_state.append(cur_key)


def on_release(key):
    global touch_state
    global data_check
    global td
    for td in touch_state:
        if 47 < ord(td) <= 57:
            data_check = True
        else:
            data_check = False
            break

    if data_check and len(touch_state) == 3:
        f_key_test(touch_state)

    touch_state.clear()


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
