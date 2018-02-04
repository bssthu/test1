@echo off

REM �Ϲ���װ·��
set ESO_PATH=F:\Program Files (x86)\SteamLibrary\steamapps\common\Zenimax Online\The Elder Scrolls Online


set /p datestr="�������ļ���׺: (����: 20180204)"
echo %datestr%
mkdir ..\..\���\���·���\
mkdir ..\..\���\���·���\1_new\
mkdir ..\..\���\���·���\2_diff\
mkdir ..\..\���\���·���\4_old\
del /Q ..\..\���\���·���\1_new\*
del /Q ..\..\���\���·���\4_old\*

set MNF_PATH="%ESO_PATH%\depot\eso.mnf"
echo %MNF_PATH%
echo ###���ڽ�ѹ...
del /Q ..\..\temp\extract\*
EsoExtractData.exe %MNF_PATH% -a 0 ..\..\temp\extract
EsoExtractData.exe %MNF_PATH% -a 2 ..\..\temp\extract

echo ###���ڸ���...
copy ..\..\temp\extract\gamedata\lang\en.lang.csv ..\..\translation\lang\
copy ..\..\temp\extract\gamedata\lang\jp.lang.csv ..\..\translation\lang\
copy ..\..\temp\extract\esoui\lang\en_pregame.lua ..\..\translation\
copy ..\..\temp\extract\esoui\lang\en_client.lua ..\..\translation\

echo ###���ڲ��...
cd ../../scripts
python split_lang_csv_by_id.py
python split_lang_csv_by_id.py -l jp

echo ###������ȡ...
python prepare_lang.py --all
copy ..\translation\lang\en.*s.lang.xlsx ..\���\���·���\1_new\

del /Q ..\translation\zh_translate.txt
python convert_lua_to_txt.py
python convert_txt_to_xls.py
copy ..\translation\zh_translate.xlsx ..\���\���·���\1_new\
python rename_lang_xls.py %datestr% ../���/���·���/1_new/

echo ��ɣ���Ѿɵ��ļ������� 4_old\ ��
cd ..\���\���·���
explorer .

pause