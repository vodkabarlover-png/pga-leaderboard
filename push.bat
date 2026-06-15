@echo off
:loop
git add Leaderboard.json
git commit -m "Update Open leaderboard"
git push
timeout /t 300 >nul
goto loop
