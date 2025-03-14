@echo off
chcp 65001
cd %~dp0
python sync_script.py
if errorlevel 1 (
    echo 同期処理でエラーが発生しました
    exit /b 1
)
echo 同期処理が完了しました
exit /b 0 