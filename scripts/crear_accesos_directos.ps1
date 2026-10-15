# Crea los accesos directos en el escritorio para Finca Vistabonita:
#   - "Finca"        → Finca.bat (procesa buzón + abre dashboard en :8501)
#   - "BUZON Finca"  → carpeta Excel-Lunes\BUZON (drop zone semanal)

$ErrorActionPreference = "Stop"

$raiz       = Split-Path -Parent $PSScriptRoot
$desktop    = [Environment]::GetFolderPath("Desktop")
$bat        = Join-Path $raiz "Finca.bat"
$buzon      = Join-Path $raiz "Excel-Lunes\BUZON"

if (!(Test-Path $bat))   { throw "No existe $bat" }
if (!(Test-Path $buzon)) { throw "No existe $buzon" }

$ws = New-Object -ComObject WScript.Shell

# 1) Acceso directo "Finca" -> Finca.bat
$lnkFinca = $ws.CreateShortcut((Join-Path $desktop "Finca.lnk"))
$lnkFinca.TargetPath       = $bat
$lnkFinca.WorkingDirectory = $raiz
$lnkFinca.Description      = "Finca Vistabonita - Procesa el buzón y abre el dashboard"
$lnkFinca.IconLocation     = "$env:SystemRoot\System32\imageres.dll,109"
$lnkFinca.Save()
Write-Host "OK  $($lnkFinca.FullName)"

# 2) Acceso directo "BUZON Finca" -> carpeta BUZON
$lnkBuzon = $ws.CreateShortcut((Join-Path $desktop "BUZON Finca.lnk"))
$lnkBuzon.TargetPath       = $buzon
$lnkBuzon.WorkingDirectory = $raiz
$lnkBuzon.Description      = "Suelta aquí el Excel Planning de PickUpADR de cada lunes (Finca Vistabonita)"
$lnkBuzon.IconLocation     = "$env:SystemRoot\System32\imageres.dll,3"
$lnkBuzon.Save()
Write-Host "OK  $($lnkBuzon.FullName)"

Write-Host ""
Write-Host "Accesos directos creados en el escritorio."
