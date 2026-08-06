$WshShell = New-Object -ComObject WScript.Shell

$Shortcut = $WshShell.CreateShortcut(
    (Join-Path ([Environment]::GetFolderPath("Desktop")) "AI Chat.lnk")
)

$Shortcut.TargetPath = Join-Path $PSScriptRoot "run.bat"
$Shortcut.WorkingDirectory = $PSScriptRoot
$Shortcut.Save()