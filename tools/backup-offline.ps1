# backup-offline.ps1 — бэкап проекта БЕЗ GitHub: в указанную папку (сетевая шара, флешка,
# папка с облачной синхронизацией) кладётся 1) bundle со всей историей, 2) полная копия репозитория.
#
# Запуск:
#   pwsh -File tools\backup-offline.ps1 -Target "\\server\share\PHD\web-form"
#   pwsh -File tools\backup-offline.ps1 -Target "D:\Backup\web-form" -Message "правка СЭ: поля вывода"
#
# Восстановление из bundle:  git clone <файл>.bundle web-form-phd-artem

param(
	[Parameter(Mandatory = $true)][string]$Target,
	[string]$Message = ""
)

$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo

if (-not (Test-Path (Join-Path $repo '.git'))) {
	Write-Error "В папке $repo нет .git — запускать нужно из репозитория проекта."
	exit 1
}

# 1. Зафиксировать изменения, если они есть
git add -A
if (git status --porcelain) {
	if ([string]::IsNullOrWhiteSpace($Message)) { $Message = "Бэкап " + (Get-Date -Format 'yyyy-MM-dd HH:mm') }
	git commit -m $Message | Out-Null
	Write-Host "== коммит создан: $Message"
} else {
	Write-Host "== новых изменений нет, фиксируем текущее состояние"
}

# 2. Bundle — вся история в одном файле
New-Item -ItemType Directory -Force -Path $Target | Out-Null
$stamp = Get-Date -Format 'yyyy-MM-dd_HHmm'
$bundle = Join-Path $Target ("WEB-FORM-PHD-ARTEM-{0}.bundle" -f $stamp)
git bundle create $bundle --all | Out-Null
if ($LASTEXITCODE -ne 0) { Write-Error "Не удалось создать bundle"; exit 1 }
$bundleOk = (git bundle verify $bundle 2>&1 | Select-String -Quiet 'complete history|okay')
Write-Host ("== bundle: {0} ({1:N0} КБ), проверка: {2}" -f $bundle, ((Get-Item $bundle).Length / 1KB), $(if ($bundleOk) { 'ок' } else { 'ПРОВЕРИТЬ' }))

# 3. Полная копия репозитория (вместе с .git) — на случай, если bundle недоступен
$mirror = Join-Path $Target 'web-form-phd-artem-repo'
robocopy $repo $mirror /MIR /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) { Write-Error "robocopy завершился с кодом $LASTEXITCODE"; exit 1 }
Write-Host "== копия репозитория: $mirror"

# 4. Контроль: модуль формы не должен измениться по дороге
$form = Join-Path $mirror 'Fore\WFRM_PHD_ANALISIS_TEP_COPY_FOR_DEV.fore'
if (Test-Path $form) {
	$sha = (Get-FileHash $form -Algorithm SHA256).Hash.ToLower()
	Write-Host ("== модуль формы в копии: {0} байт, SHA-256 {1}…" -f (Get-Item $form).Length, $sha.Substring(0, 16))
}

Write-Host "== история: $(git log --oneline | Measure-Object | Select-Object -ExpandProperty Count) коммитов, ветка $(git rev-parse --abbrev-ref HEAD)"
