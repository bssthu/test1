@echo off

REM �Ϲ���װ·��
set ESO_PATH=F:\Program Files (x86)\SteamLibrary\steamapps\common\Zenimax Online\The Elder Scrolls Online

python main.py 1 %ESO_PATH%

if %ERRORLEVEL% == 0 (
cd ..\..\���\���·���
explorer .
echo ��ɣ���Ѿɵ��ļ������� 4_old\ ��
) else (
echo ### ����ʧ��
)

pause