# Передача контекста: VR360 Room / Meta Quest

## Путь к проекту

`F:\Users\kosho\Documents\Codex\2026-09-27\x20\outputs\VR360Room\VR360Room.uproject`

Это Unreal Engine 5.6-проект для автономного просмотра 360°-панорам в VR на Meta Quest. Цель — находиться в центре сцены и смотреть вокруг, при этом панорама отображается на внутренней стороне сферы.

## Что сейчас подключено

- Стартовая карта: `/Game/VR360/Maps/VR360Map` (`Content/VR360/Maps/VR360Map.umap`).
- В карте используется сферический меш с панорамным материалом; точка просмотра находится в центре сферы.
- Активный материал последней сборки: `/Game/VR360/Materials/M_BazaarPanorama_Unlit`.
- Текстура последней сборки: `/Game/VR360/Textures/T_BazaarPanorama_3K`.
- Исходный файл: `Content/VR360/Textures/T_BazaarPanorama_3K.png`, **2896×1440** (примерно 2.9K по ширине, 4.17 Мп), без апскейла.
- Панорама импортирована без mipmaps и texture streaming; материал unlit, двусторонний. UV: U wrap, V clamp.
- В исходнике есть небольшое несовпадение левого и правого краёв, поэтому стык может быть виден на сфере. Картинка намеренно не ретушировалась.

В `Content/VR360/Textures` также есть другие панорамы и исходники на 8K/16K. Само наличие этих файлов **не означает**, что они назначены в карте или вошли в последнюю сборку. Перед заменой текстуры проверяйте назначение материала в `VR360Map` и cook-результат.

## Движок и платформенные настройки

- Unreal Engine: 5.6 (`VR360Room.uproject`).
- Плагины: OpenXR, OpenXRHandTracking, PythonScriptPlugin.
- Android: arm64, Vulkan, Meta Quest, OpenXR; package id `com.codex.vr360room`.
- Ключевые конфиги: `Config/DefaultEngine.ini`, `Config/DefaultGame.ini`.
- Для Android в конфиге выставлены ASTC quality 4×4; при этом нужно отдельно проверять, какой mip/размер реально включён при готовке текстуры, и расход памяти на Quest.

## Последняя сборка и состояние устройства

Последняя сборка Bazaar3K:

`Build/Android_OpenXR_Bazaar3K/VR360Room-arm64.apk`

OBB:

`Build/Android_OpenXR_Bazaar3K/main.1.com.codex.vr360room.obb`

Она была собрана успешно и установлена на Quest 3S (`340YC10G7D0NLZ`). В логах подтверждены запуск процесса и монтирование OBB; падения приложения в проверенном фрагменте логов не было. Однако движок сообщил, что окно VR приостановлено/неактивно (`SuspendApp_EventThread`, ожидание активного окна). Поэтому фактическое отображение панорамы в шлеме после этой установки **не подтверждено** — нужно разбудить/надеть Quest, открыть приложение из библиотеки шлема и проверить картинку и ориентацию лично.

## Сборка и установка (PowerShell)

Запускать из PowerShell. При необходимости поменять каталог сборки и серийный номер устройства.

```powershell
$project = 'F:\Users\kosho\Documents\Codex\2026-09-27\x20\outputs\VR360Room\VR360Room.uproject'
$archive = 'F:\Users\kosho\Documents\Codex\2026-09-27\x20\outputs\VR360Room\Build\Android_OpenXR_Bazaar3K'
& 'F:\Program Files\Epic Games\UE_5.6\Engine\Build\BatchFiles\RunUAT.bat' BuildCookRun `
  "-project=$project" -noP4 -utf8output -platform=Android -cookflavor=OpenXR `
  -clientconfig=Development -build -cook -stage -pak -package -archive `
  "-archivedirectory=$archive"

$adb = 'F:\Users\kosho\AppData\Local\Android\Sdk\platform-tools\adb.exe'
$serial = '340YC10G7D0NLZ'
& $adb -s $serial install -r "$archive\VR360Room-arm64.apk"
& $adb -s $serial shell mkdir -p /sdcard/Android/obb/com.codex.vr360room
& $adb -s $serial push "$archive\main.1.com.codex.vr360room.obb" /sdcard/Android/obb/com.codex.vr360room/main.1.com.codex.vr360room.obb
& $adb -s $serial shell am force-stop com.codex.vr360room
& $adb -s $serial shell monkey -p com.codex.vr360room 1
```

## Что проверить следующим шагом

1. В надетом/разбуженном шлеме убедиться, что приложение действительно входит в immersive OpenXR, а не остаётся приостановленным.
2. Проверить направление панорамы (горизонт, пол/потолок, направление взгляда) и видимость стыка на 360°-шве.
3. В Unreal проверить фактическое разрешение импортированной текстуры и Android cooked ASTC mip chain; не делать вывод о качестве по имени `16K` или исходному PNG.
4. Проверить логи после полного запуска: `adb logcat -d -s UE:V AndroidRuntime:E DEBUG:E`, наличие загрузки карты, отсутствие Fatal/OOM/ANR.
5. Если нужна бесшовная панорама, работать с источником/швом отдельно; простая установка другой текстуры или переименование в 16K проблему не решает.

## Важные ограничения передачи

- Не заявлять, что последняя Bazaar3K-сборка показана пользователю в шлеме: это ещё не подтверждено.
- Не заменять активный материал только потому, что рядом есть 16K-изображение. Сначала сверить, какую текстуру читает материал и что попало в OBB.
- Сохранять оригиналы панорам и Blender-файлы; новые варианты класть рядом под новым именем, пока не проверены качество, UV/ориентация, seam и запуск на устройстве.
