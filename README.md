1. flask framework과 Webflow를 사용하여 UI-backend 연결 중

2. flask framework으로 작업한 local web을 desktop app으로 패키지화 방법
    - 필요한 패키지
        *Pyinstaller dev 4.0 / auto-py-to-exe / pyqt5 / pyfladesk / flask
        (참고: https://stackoverflow.com/questions/37815371/
            pyinstaller-failed-to-execute-script-pyi-rth-pkgres-and-missing-packages)
    - 위의 python package들을 설치 후 auto-py-to-exe를 사용하여 패키지화
        (pyinstaller --noconfirm --onedir --noconsole --icon "C:/project/pero_UCP/palmcat_icon.ico" --uac-admin 
         --add-data "C:/project/pero_UCP/static;static/" --add-data "C:/project/pero_UCP/templates;templates/" 
         --paths "C:/Users/USER/anaconda3/envs/pyflask/Lib/site-packages"  "C:/project/pero_UCP/pero UCP.py")
    - HM NIS Edit을 사용하여 python code를 패키지화 한 파일을 담은 디렉토리를 설치프로그램으로 만드는 script 작성
        (스크립트 작성 마법사)
    - NSIS를 실행하여 위에서 작성한 HM NIS script를 load
        (참고: https://m.blog.naver.com/PostView.nhn?blogId=likelotos&logNo=221289192376&proxyReferer=https:%2F%2Fwww.google.com%2F)
    - 모든 과정을 마치고 설치 프로그램으로 만들었으나 unicodeDecodeError가 발생하는 경우
      [Windows의 hostname이 한글로 되어 있지않나 확인 – powershell : hostname 입력]
        1. 내 pc의 시스템 열기 (환경 변수 설정할 때)
        2. 설정 변경 클릭
        3. 전체 컴퓨터 이름 변경 => 영어로
