@echo off

echo ### ���ںϲ�
cd ../../scripts/
python merge_xls_dir.py ../���/���·���/1_new/ ../���/���·���/4_old/ ../���/���·���/2_diff/

echo ### �������ø�ʽ
python apply_xls_format.py ../���/���·���/1_new/ ../���/���·���/2_diff/
pause
