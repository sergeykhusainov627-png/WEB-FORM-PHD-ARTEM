# git-backup.ps1 — быстрый бэкап проекта в GitHub одним запуском.
#
# Запуск (из любой папки):
#   pwsh -File tools\git-backup.ps1                     # сообщение коммита с датой
#   pwsh -File tools\git-backup.ps1 "правка СЭ: поля вывода"
#
# Что делает: git add -A -> commit -> push в origin/main.
# Требуются сохранённые учётные данные GitHub (Git Credential Manager: вход выполняется один раз).

param([string]$Message = "")

$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo

if (-not (Test-Path (Join-Path $repo '.git'))) {
	Write-Error "В папке $repo нет .git — запускать нужно из клонированного репозитория."
	exit 1
}

$branch = (git rev-parse --abbrev-ref HEAD).Trim()
if ([string]::IsNullOrWhiteSpace($Message)) { $Message = "Бэкап " + (Get-Date -Format 'yyyy-MM-dd HH:mm') }

Write-Host "== git add -A"
git add -A

Write-Host "== git commit"
git commit -m $Message
if ($LASTEXITCODE -ne 0) { Write-Host "   (изменений для коммита нет — продолжаем)" }

Write-Host "== git push origin $branch"
git push -u origin $branch
if ($LASTEXITCODE -ne 0) {
	Write-Error "Пуш не выполнен. Проверьте вход в GitHub (Git Credential Manager) и права на репозиторий."
	exit 1
}

Write-Host "== Готово: $(git log --oneline -1)"
Write-Host "== Проверка целостности модуля формы:"
$f = Join-Path $repo 'Fore\WFRM_PHD_ANALISIS_TEP_COPY_FOR_DEV.fore'
if (Test-Path $f) {
	$len = (Get-Item $f).Length
	$sha = (Get-FileHash $f -Algorithm SHA256).Hash.ToLower().Substring(0, 16)
	Write-Host ("   {0} — {1} байт, SHA-256 {2}…" -f (Split-Path $f -Leaf), $len, $sha)
}
