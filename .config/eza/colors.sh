# eza — Gruvbox Material Alabaster
# Палитра и роли: ~/.config/palette/PALETTE.md
# Подключается из ~/.zshrc: source ~/.config/eza/colors.sh
#
# theme.yml в сборке eza 0.23.5 из homebrew молча игнорируется (даже
# заведомо битый YAML не вызывает ошибки), поэтому используется
# документированная переменная EZA_COLORS с двухбуквенными кодами.
#
# Что было не так: вывод был пёстрым — права доступа раскрашены посимвольно
# в жёлтый/красный/зелёный, владелец жирно-жёлтый, директории ярко-голубые,
# а дата шла ANSI-синим (код 34). Теперь цвет несут только тип файла и
# git-статус; всё служебное — коричнево-серое, дата — grey1.

_p_base='38;2;212;190;152'    # fg0    базовый текст
_p_bright='38;2;221;199;161'  # fg1    главное
_p_grey0='38;2;124;111;100'   # grey0  вспомогательное
_p_grey1='38;2;146;131;116'   # grey1  метаданные, даты
_p_red='38;2;204;36;29'
_p_orange='38;2;231;138;78'
_p_yellow='38;2;216;166;87'
_p_green='38;2;169;182;101'
_p_sage='38;2;137;180;130'
_p_purple='38;2;211;134;155'

EZA_COLORS="reset"

# --- Тип файла -------------------------------------------------
EZA_COLORS="${EZA_COLORS}:di=1;${_p_bright}"   # директории — светлее и жирным
EZA_COLORS="${EZA_COLORS}:fi=${_p_base}"       # обычные файлы — базовый
EZA_COLORS="${EZA_COLORS}:ex=${_p_green}"      # исполняемые
EZA_COLORS="${EZA_COLORS}:ln=${_p_grey1}"      # симлинки
EZA_COLORS="${EZA_COLORS}:or=${_p_red}"        # битые симлинки
EZA_COLORS="${EZA_COLORS}:lp=${_p_grey0}"      # путь симлинка
EZA_COLORS="${EZA_COLORS}:bO=${_p_red}"        # подсветка битого пути
EZA_COLORS="${EZA_COLORS}:sp=${_p_grey0}"      # прочее спецальное
EZA_COLORS="${EZA_COLORS}:mp=${_p_purple}"     # точки монтирования
EZA_COLORS="${EZA_COLORS}:pi=${_p_grey0}"      # именованные каналы
EZA_COLORS="${EZA_COLORS}:so=${_p_grey0}"      # сокеты
EZA_COLORS="${EZA_COLORS}:bd=${_p_grey0}"      # блочные устройства
EZA_COLORS="${EZA_COLORS}:cd=${_p_grey0}"      # символьные устройства

# --- Категории содержимого — сдержанно --------------------------
EZA_COLORS="${EZA_COLORS}:im=${_p_sage}"       # изображения
EZA_COLORS="${EZA_COLORS}:vi=${_p_yellow}"     # видео
EZA_COLORS="${EZA_COLORS}:mu=${_p_yellow}"     # музыка с потерями
EZA_COLORS="${EZA_COLORS}:lo=${_p_yellow}"     # музыка без потерь
EZA_COLORS="${EZA_COLORS}:cr=${_p_purple}"     # ключи, сертификаты

# --- Права доступа — всё вспомогательное, коричнево-серым --------
# Единственное исключение: бит записи жёлтый, потому что это
# единственное, что реально меняет решение при чтении листинга.
for _c in ur ux ue gr gx tr tx; do
  EZA_COLORS="${EZA_COLORS}:${_c}=${_p_grey0}"
done
for _c in uw gw tw; do
  EZA_COLORS="${EZA_COLORS}:${_c}=${_p_yellow}"
done
EZA_COLORS="${EZA_COLORS}:su=${_p_red}"        # setuid/setgid/sticky
EZA_COLORS="${EZA_COLORS}:sf=${_p_red}"
EZA_COLORS="${EZA_COLORS}:xa=${_p_grey0}"      # признак xattr
EZA_COLORS="${EZA_COLORS}:oc=${_p_grey0}"      # права в восьмеричном виде

# --- Размер ------------------------------------------------------
EZA_COLORS="${EZA_COLORS}:sn=${_p_base}"       # число
EZA_COLORS="${EZA_COLORS}:sb=${_p_grey0}"      # единица измерения
EZA_COLORS="${EZA_COLORS}:df=${_p_grey0}"      # major ID устройства
EZA_COLORS="${EZA_COLORS}:ds=${_p_grey0}"      # minor ID устройства

# --- Владелец и группа — метаданные ------------------------------
EZA_COLORS="${EZA_COLORS}:uu=${_p_grey1}"      # вы
EZA_COLORS="${EZA_COLORS}:uR=${_p_red}"        # root
EZA_COLORS="${EZA_COLORS}:un=${_p_grey0}"      # кто-то другой
EZA_COLORS="${EZA_COLORS}:gu=${_p_grey1}"
EZA_COLORS="${EZA_COLORS}:gR=${_p_red}"
EZA_COLORS="${EZA_COLORS}:gn=${_p_grey0}"

# --- Дата, ссылки, служебное -------------------------------------
EZA_COLORS="${EZA_COLORS}:da=${_p_grey1}"      # БЫЛА СИНЕЙ (ANSI 34)
EZA_COLORS="${EZA_COLORS}:lc=${_p_grey0}"      # число жёстких ссылок
EZA_COLORS="${EZA_COLORS}:lm=${_p_yellow}"     # файл с несколькими ссылками
EZA_COLORS="${EZA_COLORS}:in=${_p_grey0}"      # inode
EZA_COLORS="${EZA_COLORS}:bl=${_p_grey0}"      # блоки
EZA_COLORS="${EZA_COLORS}:xx=${_p_grey0}"      # пунктуация и фон UI
EZA_COLORS="${EZA_COLORS}:hd=1;${_p_bright}"   # заголовок таблицы
EZA_COLORS="${EZA_COLORS}:cc=${_p_red}"        # экранированный символ в имени

# --- Git ----------------------------------------------------------
EZA_COLORS="${EZA_COLORS}:ga=${_p_green}"      # новый
EZA_COLORS="${EZA_COLORS}:gm=${_p_yellow}"     # изменён
EZA_COLORS="${EZA_COLORS}:gd=${_p_red}"        # удалён
EZA_COLORS="${EZA_COLORS}:gv=${_p_orange}"     # переименован
EZA_COLORS="${EZA_COLORS}:gt=${_p_orange}"     # изменены метаданные
EZA_COLORS="${EZA_COLORS}:gi=${_p_grey0}"      # игнорируется
EZA_COLORS="${EZA_COLORS}:gc=${_p_red}"        # конфликт
EZA_COLORS="${EZA_COLORS}:Gm=${_p_base}"       # основная ветка
EZA_COLORS="${EZA_COLORS}:Go=${_p_grey1}"      # прочие ветки
EZA_COLORS="${EZA_COLORS}:Gc=${_p_green}"      # чистая ветка
EZA_COLORS="${EZA_COLORS}:Gd=${_p_yellow}"     # грязная ветка

export EZA_COLORS
unset _p_base _p_bright _p_grey0 _p_grey1 _p_red _p_orange _p_yellow _p_green _p_sage _p_purple _c
