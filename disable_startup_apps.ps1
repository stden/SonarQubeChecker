# Скрипт отключения ненужных программ из автозагрузки
Write-Host "🔧 Оптимизация автозагрузки..." -ForegroundColor Green

# Программы, которые можно безопасно отключить из автозагрузки
$AppsToDisable = @(
    "DeepL auto-start",
    "Docker Desktop", 
    "electron.app.LM Studio",
    "JetBrains Toolbox",
    "MicrosoftEdgeAutoLaunch_*",
    "Microsoft.Lists",
    "Mathworks Service Host"
)

Write-Host "`nПрограммы в автозагрузке, которые можно отключить:" -ForegroundColor Yellow
foreach ($app in $AppsToDisable) {
    Write-Host "❌ $app - можно отключить для ускорения загрузки" -ForegroundColor Red
}

Write-Host "`nПрограммы, которые лучше оставить:" -ForegroundColor Yellow
Write-Host "✅ SecurityHealth - системная безопасность" -ForegroundColor Green
Write-Host "✅ Greenshot - скриншоты" -ForegroundColor Green
Write-Host "✅ Acronis Scheduler2 Service - резервное копирование" -ForegroundColor Green

Write-Host "`nДля отключения автозагрузки:" -ForegroundColor Cyan
Write-Host "1. Win + R → msconfig → Автозагрузка" -ForegroundColor Gray
Write-Host "2. Или Ctrl + Shift + Esc → Автозагрузка" -ForegroundColor Gray
Write-Host "3. Отключить приложения с высоким влиянием на запуск" -ForegroundColor Gray