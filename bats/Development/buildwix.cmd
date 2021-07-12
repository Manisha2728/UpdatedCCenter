set SrcRootPath=C:\CM\DBMOTION
set MsiFileVersion=48.0.705.0
 
set PackageSolutionDir=%SrcRootPath%\dbm_System\Package\Setups
 
c:\Windows\Microsoft.NET\Framework\v4.0.30319\msbuild "%PackageSolutionDir%\Common Resources\dbmCommonCustomActions\_dbmCommonCustomActions.csproj" /p:Configuration=Release /p:Platform=x64 /p:SolutionDir="%PackageSolutionDir%" /t:rebuild
IF %ERRORLEVEL% NEQ 0 (
     pause
)

rem TODO: Add setups to be built
 
FOR %%p in (
 
"%PackageSolutionDir%\Configuration Service\Configuration Service.wixproj" 
 
) DO (
 
		echo %%p
		c:\Windows\Microsoft.NET\Framework\v4.0.30319\msbuild %%p /p:Configuration=Release /p:Platform=x64 /p:SolutionDir="%PackageSolutionDir%" /t:rebuild
                IF %ERRORLEVEL% NEQ 0 (
                              pause
                )
 
 
)
pause

IF %ERRORLEVEL%==0 explorer "%SrcRootPath%\dbm_System\Package\bin\Release\Setups\x64