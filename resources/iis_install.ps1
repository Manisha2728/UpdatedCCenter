Param (
   [Parameter(Mandatory=$true, ValueFromPipelineByPropertyName=$true )]
   [string] $thumbprint
)

Import-Module WebAdministration

$website= Get-Website -Name 'CCenter'

#Finish if CCenter not in IIS.
if($website -eq $null)
{
    return
}


function Bind-IISCertificate
{
    [CmdletBinding()]
    [Alias()]
    [OutputType([int])]
    Param
    (
        # Param1 help description
        [Parameter(Mandatory=$true, ValueFromPipelineByPropertyName=$true, Position=0)]
        $Thumbprint
    )

    Begin
    {
    $ScriptBlock= '
              $Thumbprint= "ThumbPrinToReplace"
              Import-Module WebAdministration
              $certificate= get-item "Cert:\LocalMachine\My\$Thumbprint"
              $certificate
              if(Test-Path -Path "IIS:\SSLBindings\0.0.0.0!8040")
              {
                  if (Get-Item "IIS:\SSLBindings\0.0.0.0!8040")
                    {
                        remove-Item "IIS:\SSLBindings\0.0.0.0!8040"
                        #Remove-WebBinding -Name "CCenter" -IP * -Port 8040 -Protocol https
                    }
               }
              $certificate | New-Item "IIS:\SSLBindings\0.0.0.0!8040"
              New-WebBinding -Name "CCenter" -IP * -Port 8040 -Protocol https
              Remove-WebBinding -Name "CCenter" -IP * -Port 80 -Protocol http
			  New-WebBinding -Name "Default Web Site" -IP * -Port 80 -Protocol http'
    $ScriptBlock= $ScriptBlock.Replace("ThumbPrinToReplace","$Thumbprint")
    

    }
    Process
    {

        Invoke-Expression -Command $ScriptBlock
    }
    End
    {
        $newThumbprint = Get-Item "IIS:\SSLBindings\0.0.0.0!8040" | select thumbprint
        if ($Thumbprint -eq $newThumbprint.Thumbprint)
        {
            Write-Output "Certificate was Bind Succesfully "
        }
        else
        {
            throw ("Error with Binding")
        }
    }
}

$serviceStatus=(Get-Service 'TrustedInstaller').StartType

if($serviceStatus -eq "Disabled")
{
    Write-Host 'Enabling TrustedInstaller Service...'
    Set-Service 'TrustedInstaller' -StartupType Automatic
    Start-Service 'TrustedInstaller'
}

$featureStatusCGI=(Get-WindowsOptionalFeature -online -featurename 'IIS-CGI').State


if($featureStatusCGI -eq "Disabled")
{
    Write-Host 'Enabling IIS-CGI Feature...'
    Enable-windowsoptionalfeature -online -FeatureName 'IIS-CGI' -NoRestart
    Write-Host 'Restarting IIS...'
    invoke-command -scriptblock {iisreset /restart }
}

Import-Module WebAdministration

$certificate=(Get-ChildItem -path cert:\LocalMachine\My | Where-Object {$_.Thumbprint -like "$thumbprint"})[0]

Write-Host 'Binding Certificate...'
Bind-IISCertificate -Thumbprint ($certificate.thumbprint) 

Write-Host 'Adding fastCGI Application to fastCGI settings...'
try
{
	$PyPath="C:\Program Files\Python27-11\python.exe"
	ADD-WebConfigurationProperty -pspath 'MACHINE/WEBROOT/APPHOST'  -filter "system.webServer/fastCgi" -name "." -value @{fullPath=$PyPath; arguments='"C:\Program Files\dbMotion\Services\CCenter\ConfigCenter\manage.py" fcgi --pythonpath "C:\Program Files\dbMotion\Services\CCenter\ConfigCenter" --settings configcenter.settings'}
}
catch
{
	Write-Host 'Application was already there...'
}

$hendler=Get-WebHandler -PSPath "IIS:\sites\CCenter" -Name "CCenter Handler"
if($hendler -eq $null)
{
	Write-Host 'Creating new Web Hendler For CCenter CGI Module...'
	$sp='C:\Program Files\python27-11\python.exe|"C:\Program Files\dbMotion\Services\CCenter\ConfigCenter\manage.py" fcgi --pythonpath "C:\Program Files\dbMotion\Services\CCenter\ConfigCenter" --settings configcenter.settings'
	New-WebHandler -Name "CCenter Handler" -PSPath 'IIS:\Sites\CCenter' -Path * -Verb * -ScriptProcessor $sp -Modules FastCgiModule -ResourceType Unspecified -RequiredAccess Script

}


$hendler=Get-WebHandler -PSPath "IIS:\sites\CCenter\static" -Name "CCenter Handler"
if($hendler -ne $null)
{ 
	Write-Host 'Removing CCenter Handler from static Virtual Directory...'
	Remove-WebHandler -PSPath "IIS:\sites\CCenter\static" -Name "CCenter Handler"
}

Write-Host 'Removing Certificate from old apachi service...'
Get-ChildItem -Path "C:\Program Files\dbMotion\Services\CCenter\Apache2\conf\ssl" -Include * -File -Recurse | foreach { $_.Delete()}  

Write-Host 'Restarting IIS...'
invoke-command -scriptblock {iisreset /restart }