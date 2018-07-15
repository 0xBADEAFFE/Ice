$steam = Get-Process steam -ErrorAction SilentlyContinue
if ($steam) {
    $steam.CloseMainWindow()
    Start-Sleep 5
    if (!$steam.HasExited) {
        $steam | Stop-Process -Force
    }
}

Remove-Variable steam

Start-Process .\Ice.exe
$ice = Get-Process ice
while (!$ice.HasExited) {

}

Remove-Variable ice

Start-Process "steam:"