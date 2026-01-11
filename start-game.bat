@echo off
title Web Fishing Server
echo --- DANG KHOI DONG SERVER CAU CA ---
echo.

:: 1. Nhảy vào thư mục backend
cd backend

:: 2. Chạy server (Lệnh này sẽ dùng Python đang kích hoạt)
python run.py

:: 3. Giữ màn hình không bị tắt nếu server crash
pause