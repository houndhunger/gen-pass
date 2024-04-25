@echo off
setlocal

rem Get the directory of the batch script
set "script_dir=%~dp0"

rem Specify the file name for the output
set "output_file=%script_dir%list.txt"

rem List the file names in the directory and save to output file
dir /b "%script_dir%" > "%output_file%"

endlocal
