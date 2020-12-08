$counter = typeperf "\Processor Information(_total)\% Processor Utility" -sc 1 | findstr .*/.*/.*
$proc = [regex]"""(.+)"",""((\d+).+)""$"
$value = $proc.match($counter)[0].Groups[3].Value + '%'
$warning=$args[0]
$critical=$args[1]
If($args.count -ne 2) {
Write-Host "OK: $value | cpu=$value"
exit 0
}
If($value -ge $critical) {
Write-Host "Critical: $value | cpu=$value"
exit 2
}
ElseIf($value -ge $warning) {
Write-Host "Warning: $value | cpu=$value"
exit 1
}
else {
Write-Output "OK: $value | cpu=$value"
}
