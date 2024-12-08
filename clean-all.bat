@echo on
for /d /r . %%d in (__pycache__) do @if exist "%%d" echo "%%d" && rd /s/q "%%d"
if exist build (rd /S /Q build)
if exist dist (rd /S /Q dist)
del /Q /F *.spec
pause