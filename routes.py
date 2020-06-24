import os
import sqlite3
import subprocess

import psutil
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, json

from functools import wraps, update_wrapper
from datetime import datetime

# cache = Cache(config={'CACHE_TYPE': 'simple'})


conn = sqlite3.connect('./static/set_db/UCP_Database.db', check_same_thread=False)
cur = conn.cursor()

subprocess_list = []


def kill_process():
    for proc in psutil.process_iter():
        if any(procstr in proc.name() for procstr in
               ['gestureShortcut.exe', 'gestureShortcut.exe']):
            print(f'Killing {proc.name()}')
            proc.kill()


def insertToCmdOption(ges_name, app_name):
    cmds = []
    group_names = []
    ft_cmdIds = []
    ft_cmdNames = []

    # app에 대한 명령id들 조회
    cur.execute('''SELECT cmd_id FROM AppCmd_Combi
                    WHERE app_id = (
                        SELECT app_id
                        FROM Application
                        WHERE app_name='%s')''' % app_name)
    for row in cur:
        cmds.append(str(row[0]))

    # 선택한 제스처의 그룹명들 조회
    cur.execute('''SELECT gg_typeName FROM Ges_Group
                    WHERE ges_id = (
                        SELECT ges_id
                        FROM Gesture 
                        WHERE ges_name='%s')''' % ges_name)
    for row in cur:
        group_names.append("'" + row[0] + "'")

    # 선택한 app에 대한 명령 중 해당 그룹에 속한 명령id들 조회
    cur.execute('''SELECT DISTINCT cmd_id
                    FROM Cmd_Group
                    WHERE cg_typeName IN (%s) AND cmd_id IN (%s)'''
                % (','.join(group_names), ','.join(cmds)))
    for row in cur:
        ft_cmdIds.append(str(row[0]))

    # cmd_id로 명령들 이름 조회 ft_cmdNames: 선택할 수 있는 명령들
    cur.execute('''SELECT cmd_name
                            FROM Command
                            WHERE cmd_id IN (%s)'''
                % ','.join(ft_cmdIds))
    for row in cur:
        ft_cmdNames.append(row[0])
    # 현재 선택한 제스처에 매핑된 명령들 조회 구문
    # ges_name으로 ges_id(3개) 조회
    ges_ids = []
    cur.execute('''SELECT ges_id FROM Gesture WHERE ges_name = "%s"''' % ges_name)
    for row in cur:
        ges_ids.append(str(row[0]))
    # 선택한 제스처(ges_id 3개) 중 세팅된 데이터가 있는지 조회 (acc_id, ges_id)
    cur.execute('''SELECT acc_id, ges_id FROM Use_Set WHERE ges_id IN (%s)''' % ','.join(ges_ids))
    acc_ges = cur.fetchall()
    # 그 중에 현재 app에 대한 세팅 데이터가 있는지
    set_cg_ids = []  # option에 표시할 (cmd_id, ges_id) 리스트
    for i in range(len(acc_ges)):
        cur.execute('''SELECT cmd_id, app_id 
                                FROM AppCmd_Combi 
                                WHERE acc_id = "%s" 
                                    AND app_id = (SELECT app_id
                                                    FROM Application
                                                    WHERE app_name='%s')'''
                    % (acc_ges[i][0], app_name))
        for row in cur:
            set_cg_ids.append((str(row[0]), acc_ges[i][1]))
    # 세팅된 데이터 없을 때
    if not set_cg_ids:
        pass
    else:  # 세팅된 데이터 있을 때 각 제스처마다 touch2,3,4에 대한 문자를 붙여준다
        for sc in set_cg_ids:
            cur.execute("SELECT cmd_name FROM Command WHERE cmd_id = %s" % sc[0])
            dis_cmdName = cur.fetchall()[0][0]
            idx = ft_cmdNames.index(dis_cmdName)
            if sc[1] % 3 == 1:
                ft_cmdNames[idx] = dis_cmdName + '_t2'
            elif sc[1] % 3 == 2:
                ft_cmdNames[idx] = dis_cmdName + '_t3'
            elif sc[1] % 3 == 0:
                ft_cmdNames[idx] = dis_cmdName + '_t4'

    return ft_cmdNames


def UseSetDatabase(ges_name, app_name, touch, cmd_name):
    cmd_ids = []
    app_id = ''
    app_ids = []
    acc_id = 0
    acc_ids = []
    ges_id = 0

    if cmd_name == "Not Selected":
        print("여기서 해당 데이터 삭제할거임")
        # ges_id 조회
        cur.execute('''SELECT ges_id FROM Gesture
                            WHERE ges_name ="%s" AND touch = "%s"''' % (ges_name, touch))
        for row in cur:
            ges_id = str(row[0])
        # app_id 조회
        cur.execute('''SELECT app_id FROM Application
                                        WHERE app_name ="%s"''' % app_name)
        for row in cur:
            app_id = str(row[0])
        # Use_Set에서 ges_id로 acc_id 조회
        cur.execute('''SELECT acc_id
                                FROM Use_Set
                                WHERE ges_id = %s''' % ges_id)
        for row in cur:
            acc_ids.append(str(row[0]))
        # AppCmd_Combi에서 현재 app과 같은 acc_id 조회
        cur.execute('''SELECT acc_id FROM AppCmd_Combi
                            WHERE acc_id IN (%s) AND app_id = %s''' % (','.join(acc_ids), app_id))
        for row in cur:
            acc_id = row[0]
        # Use_Set에서 acc_id(int)와 ges_id(string)으로 조회하여 해당 row 삭제
        cur.execute("delete from Use_Set where acc_id=%d AND ges_id = %s" % (acc_id, ges_id))
        conn.commit()
    else:
        # cmd_id 조회
        cur.execute('''SELECT cmd_id FROM Command
                        WHERE cmd_name ="%s"''' % cmd_name)
        for row in cur:
            cmd_ids.append(str(row[0]))

        # app_id 조회
        cur.execute('''SELECT app_id FROM Application
                        WHERE app_name ="%s"''' % app_name)
        for row in cur:
            app_id = str(row[0])

        # acc_id 조회
        cur.execute('''SELECT acc_id
                        FROM AppCmd_Combi
                        WHERE cmd_id IN (%s) AND app_id = %s'''
                    % (','.join(cmd_ids), app_id))
        for row in cur:
            acc_id = row[0]
        # ges_id 조회
        cur.execute('''SELECT ges_id FROM Gesture
                        WHERE ges_name ="%s" AND touch = "%s"''' % (ges_name, touch))
        for row in cur:
            ges_id = row[0]

        # 같은 app에 data 이미 존재하면 update / 처음 저장하는 것이면 insert
        cur.execute('''SELECT acc_id FROM Use_Set WHERE ges_id = %s''' % ges_id)
        for row in cur:
            acc_ids.append(str(row[0]))
        cur.execute('''SELECT DISTINCT app_id FROM AppCmd_Combi
                        WHERE acc_id IN (%s)''' % ','.join(acc_ids))
        for row in cur:
            app_ids.append(row[0])
        if not app_ids:  # 처음 데이터 setting 때
            cur.execute("INSERT INTO Use_Set(acc_id, ges_id) VALUES (?, ?)", (acc_id, ges_id))
            conn.commit()
        else:
            if int(app_id) in app_ids:  # 이미 중복된 App setting된 데이터가 있을 때
                cur.execute("SELECT acc_id FROM AppCmd_Combi WHERE acc_id IN (%s) AND app_id = %s" % (','.join(acc_ids), app_id))
                before_acc_id = cur.fetchall()[0][0]
                cur.execute('''UPDATE Use_Set SET acc_id = %s 
                                WHERE acc_id = %s AND ges_id = %s'''
                            % (str(acc_id), str(before_acc_id), ges_id))
                conn.commit()
            else:  # 데이터는 있으나 App이 중복되지 않을 때
                cur.execute("INSERT INTO Use_Set(acc_id, ges_id) VALUES (?, ?)", (acc_id, ges_id))
                conn.commit()


app = Flask(__name__, static_url_path='/static')
# ui = FlaskUI(app)


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)


@app.route('/')
@nocache
def index():
    # 1. gestureShortcut.exe를 무조건 process에서 삭제
    kill_process()
    # 2. initializing 진행 여부 확인: table값 조회
    cur.execute("SELECT init_state FROM Check_init")
    init_state = cur.fetchall()[0][0]
    print(init_state)
    # 2-1. initializing 미진행: index.html을 return
    if init_state == 0:
        return render_template('index.html')
    # 2-2. initializing 진행: gestureShortcut.exe을 실행 후 c2.html을 return
    elif init_state == 1:
        cur_path = os.path.dirname(os.path.abspath(__file__))
        subprocess_list.append(
        subprocess.Popen('%s\\static\\set_db\\gestureShortcut.exe' % cur_path, shell=True, encoding='utf-8'))
        return render_template('c2.html')


@app.route('/g1')
@nocache
def g1():
    return render_template('g1.html')


@app.route('/g2')
@nocache
def g2():
    return render_template('g2.html')


@app.route('/g3')
@nocache
def g3():
    return render_template('g3.html')


@app.route('/g3_1', methods=['GET', 'POST'])
@nocache
def g3_1():
    if request.method == 'POST':
        c_hand = request.form['left']
        print(c_hand)
    return render_template('g3.html')


@app.route('/g3_2', methods=['GET', 'POST'])
@nocache
def g3_2():
    if request.method == 'POST':
        c_hand = request.form['right']
        print(c_hand)
    return render_template('g3.html')


@app.route('/g4')
@nocache
def g4():
    return render_template('g4.html')


@app.route('/g4_1', methods=['GET', 'POST'])
@nocache
def g4_1():
    if request.method == 'POST':
        g3_answer = request.form['answer1']
        print(g3_answer)
    return render_template('g4.html')


@app.route('/g4_2', methods=['GET', 'POST'])
@nocache
def g4_2():
    if request.method == 'POST':
        g3_answer = request.form['answer2']
        print(g3_answer)
    return render_template('g4.html')


@app.route('/g4_3', methods=['GET', 'POST'])
@nocache
def g4_3():
    if request.method == 'POST':
        g3_answer = request.form['answer3']
        print(g3_answer)
    return render_template('g4.html')


@app.route('/g5')
@nocache
def g5():
    return render_template('g5.html')


@app.route('/g5_1', methods=['GET', 'POST'])
@nocache
def g5_1():
    if request.method == 'POST':
        g4_answer = request.form['answer1']
        print(g4_answer)
    return render_template('g5.html')


@app.route('/g5_2', methods=['GET', 'POST'])
@nocache
def g5_2():
    if request.method == 'POST':
        g4_answer = request.form['answer2']
        print(g4_answer)
    return render_template('g5.html')


@app.route('/g5_3', methods=['GET', 'POST'])
@nocache
def g5_3():
    if request.method == 'POST':
        g4_answer = request.form['answer3']
        print(g4_answer)
    return render_template('g5.html')


@app.route('/c1')
@nocache
def c1():
    return render_template('c1.html')


@app.route('/c1_1', methods=['GET', 'POST'])
@nocache
def c1_1():
    if request.method == 'POST':
        g5_answer = request.form['answer1']
        print(g5_answer)
    return render_template('c1.html')


@app.route('/c1_2', methods=['GET', 'POST'])
@nocache
def c1_2():
    if request.method == 'POST':
        g5_answer = request.form['answer2']
        print(g5_answer)
    return render_template('c1.html')


@app.route('/c1_3', methods=['GET', 'POST'])
@nocache
def c1_3():
    if request.method == 'POST':
        g5_answer = request.form['answer3']
        print(g5_answer)
    return render_template('c1.html')


@app.route('/f1')
@nocache
def f1():
    return render_template('f1.html')


@app.route('/f2')
@nocache
def f2():
    return render_template('f2.html')


@app.route('/f3')
@nocache
def f3():
    return render_template('f3.html')


@app.route('/c2')
@nocache
def c2():
    cur.execute("UPDATE Check_init SET init_state=1")
    conn.commit()
    cur_path = os.path.dirname(os.path.abspath(__file__))
    subprocess_list.append(subprocess.Popen('%s\\static\\set_db\\gestureShortcut.exe' % cur_path, shell=True, encoding='utf-8'))
    return render_template('c2.html')


@app.route('/m2-app1')
@nocache
def m1():
    # windows
    return render_template('m2-app1_data.html')


@app.route('/m2-app-getData', methods=["GET", "POST"])
@nocache
def m1_getData():
    if request.method == "POST":
        ges_name = request.form["gesture_data"]
        app_name = request.form["active_app"]
        cmd_group = insertToCmdOption(ges_name, app_name)
        print(cmd_group)
    return jsonify(list_of_data=cmd_group)


@app.route('/m2-app-data', methods=["GET", "POST"])
@nocache
def m1_data():
    # windows
    if request.method == "POST":
        ges_name = request.form["gesture_data"]
        touch = request.form["touch_data"]
        cmd_name = request.form["command"]
        app_name = request.form["active_app"]
        print(ges_name)
        print(touch)
        print(cmd_name)
        print(app_name)
        UseSetDatabase(ges_name, app_name, touch, cmd_name)
        resp = jsonify(success=True)
    return resp


@app.route('/m2-app2')
@nocache
def m2():
    # ms word
    cmd_group = insertToCmdOption('L1', 'MS word')
    sel_cmds = {'touch2': 'x', 'touch3': 'x', 'touch4': 'x'}
    for i in range(len(cmd_group)):
        if '_' in cmd_group[i]:
            if cmd_group[i].split('_')[1] == 't2':
                sel_cmds['touch2'] = cmd_group[i].split('_')[0]
            elif cmd_group[i].split('_')[1] == 't3':
                sel_cmds['touch3'] = cmd_group[i].split('_')[0]
            elif cmd_group[i].split('_')[1] == 't4':
                sel_cmds['touch4'] = cmd_group[i].split('_')[0]
            cmd_group[i] = cmd_group[i].split('_')[0]
    print(cmd_group)
    print(sel_cmds)
    return render_template('m2-app2_data.html', options=cmd_group, sel_cmd=sel_cmds)


@app.route('/m2-app3')
@nocache
def m3():
    # ms excel
    return render_template('m2-app3_data.html')


@app.route('/m2-app4')
@nocache
def m4():
    # ms powerpoint
    return render_template('m2-app4_data.html')


@app.route('/m2-app5')
@nocache
def m5():
    # explorer
    return render_template('m2-app5_data.html')


@app.route('/m2-app6')
@nocache
def m6():
    # chrome
    return render_template('m2-app6_data.html')


@app.route('/m2-app7')
@nocache
def m7():
    # youtube
    cmd_group = insertToCmdOption('L1', 'Youtube')
    sel_cmds = {'touch2': 'x', 'touch3': 'x', 'touch4': 'x'}
    for i in range(len(cmd_group)):
        if '_' in cmd_group[i]:
            if cmd_group[i].split('_')[1] == 't2':
                sel_cmds['touch2'] = cmd_group[i].split('_')[0]
            elif cmd_group[i].split('_')[1] == 't3':
                sel_cmds['touch3'] = cmd_group[i].split('_')[0]
            elif cmd_group[i].split('_')[1] == 't4':
                sel_cmds['touch4'] = cmd_group[i].split('_')[0]
            cmd_group[i] = cmd_group[i].split('_')[0]
    return render_template('m2-app7_data.html', options=cmd_group, sel_cmd=sel_cmds)


@app.route('/m2-app8')
@nocache
def m8():
    # media player
    return render_template('m2-app8_data.html')


@app.route('/m2-app9')
@nocache
def m9():
    # netflix
    cmd_group = insertToCmdOption('L1', 'Netflix')
    sel_cmds = {'touch2': 'x', 'touch3': 'x', 'touch4': 'x'}
    for i in range(len(cmd_group)):
        if '_' in cmd_group[i]:
            if cmd_group[i].split('_')[1] == 't2':
                sel_cmds['touch2'] = cmd_group[i].split('_')[0]
            elif cmd_group[i].split('_')[1] == 't3':
                sel_cmds['touch3'] = cmd_group[i].split('_')[0]
            elif cmd_group[i].split('_')[1] == 't4':
                sel_cmds['touch4'] = cmd_group[i].split('_')[0]
            cmd_group[i] = cmd_group[i].split('_')[0]
    return render_template('m2-app9_data.html', options=cmd_group, sel_cmd=sel_cmds)


@app.route('/m2-app10')
@nocache
def m10():
    return render_template('m2-app10_data.html')


if __name__ == '__main__':
    app.debug = False
    app.run(host="localhost", port="2001")
    # ui.run()
