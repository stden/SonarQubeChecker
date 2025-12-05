# IntelliJ IDEA Optimization Guide

## 🚀 Настройки производительности

### VM Options (Help → Edit Custom VM Options):
```
-Xms2048m
-Xmx8192m
-XX:ReservedCodeCacheSize=512m
-XX:+UseG1GC
-XX:SoftRefLRUPolicyMSPerMB=50
-XX:CICompilerCount=2
-XX:+HeapDumpOnOutOfMemoryError
-Dsun.io.useCanonPrefixCache=false
-Djdk.http.auth.tunneling.disabledSchemes=""
```

### Settings для отключения:
1. **File → Settings → Build, Execution, Deployment**
   - ☐ Build project automatically
   - ☐ Compile independent modules in parallel

2. **Editor → General**
   - ☐ Sync scrolling in split editor
   - ☐ Highlight usages of element at caret

3. **Editor → Code Completion**
   - ☐ Show suggestions as you type
   - Set "Autopopup in" to 1000ms

4. **Editor → Inspections**
   - Отключить неиспользуемые инспекции
   - Оставить только критичные

5. **Version Control**
   - ☐ Show author and date in the editor

## 🔌 Плагины для отключения

### Высокая нагрузка:
- [ ] AI Assistant
- [ ] GitHub Copilot
- [ ] Docker
- [ ] Kubernetes
- [ ] Database Tools and SQL
- [ ] Markdown

### Средняя нагрузка:
- [ ] Spring Boot
- [ ] Maven Helper
- [ ] HTTP Client
- [ ] UML Support
- [ ] Terminal
- [ ] Cloud Code (AWS/GCP)

### Индексация:
- Исключить из индексации:
  - node_modules/
  - .git/
  - target/
  - build/
  - dist/

## ⚡ Быстрые действия
1. File → Invalidate Caches and Restart
2. Увеличить Memory Heap в Help → Change Memory Settings
3. Отключить неиспользуемые языки в Settings → Languages & Frameworks