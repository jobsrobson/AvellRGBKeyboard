project(
  'avell-rgb-control',
  version: '0.1.0',
  meson_version: '>= 0.61.0'
)

python = import('python').find_installation('python3')

app_id = 'io.github.jobsr.AvellRGBControl'
app_name = 'avell-rgb-control'

datadir = get_option('datadir')
bindir = get_option('bindir')

appdir = join_paths(
  get_option('prefix'),
  datadir,
  app_name
)

# ============================================================
# Aplicação Python
# ============================================================

install_data(
  [
    'src/main.py',
    'src/hardware.py',
    'src/keyboard.py',
    'src/lightbar.py',
    'src/profiles.py',
    'src/window.py',
  ],
  install_dir: appdir
)

install_data(
  [
    'src/pages/__init__.py',
    'src/pages/keyboard_page.py',
    'src/pages/lightbar_page.py',
    'src/pages/profiles_page.py',
  ],
  install_dir: join_paths(appdir, 'pages')
)

# ============================================================
# Launcher
# ============================================================

install_data(
  'scripts/avell-rgb-control',
  install_dir: join_paths(
    get_option('prefix'),
    bindir
  ),
  install_mode: 'rwxr-xr-x'
)

# ============================================================
# Desktop entry
# ============================================================

install_data(
  'data/io.github.jobsr.AvellRGBControl.desktop',
  install_dir: join_paths(
    get_option('prefix'),
    datadir,
    'applications'
  )
)

# ============================================================
# Ícone
# ============================================================

install_data(
  'data/io.github.jobsr.AvellRGBControl.svg',
  install_dir: join_paths(
    get_option('prefix'),
    datadir,
    'icons',
    'hicolor',
    'scalable',
    'apps'
  )
)

# ============================================================
# AppStream metadata
# ============================================================

install_data(
  'data/io.github.jobsr.AvellRGBControl.metainfo.xml',
  install_dir: join_paths(
    get_option('prefix'),
    datadir,
    'metainfo'
  )
)

# ============================================================
# udev
# ============================================================

install_data(
  'data/99-avell-rgb-control.rules',
  install_dir: '/usr/lib/udev/rules.d'
)