# write timestamp every one second
while ($true) {
    $timeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Output "$timeStamp"
    Start-Sleep -Seconds 1
}
