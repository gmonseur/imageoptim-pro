#!/bin/bash
set -e

INSTALL_DIR="$HOME/.local/share/ImageOptimPro"
BIN_DIR="$HOME/.local/bin"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"
DESKTOP_DIR="$HOME/.local/share/applications"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Installation de ImageOptim Pro..."

mkdir -p "$INSTALL_DIR" "$BIN_DIR" "$ICON_DIR" "$DESKTOP_DIR"

cp -r "$SCRIPT_DIR"/. "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/ImageOptimPro"

ln -sf "$INSTALL_DIR/ImageOptimPro" "$BIN_DIR/imageoptimpro"

if [ -f "$SCRIPT_DIR/icon.png" ]; then
    cp "$SCRIPT_DIR/icon.png" "$ICON_DIR/imageoptimpro.png"
fi

cat > "$DESKTOP_DIR/imageoptimpro.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=ImageOptim Pro
Comment=Redimensionnez et compressez vos images par lot
Exec=$INSTALL_DIR/ImageOptimPro
Icon=imageoptimpro
Categories=Graphics;
Terminal=false
EOF

if command -v update-desktop-database &>/dev/null; then
    update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
fi
if command -v gtk-update-icon-cache &>/dev/null; then
    gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" 2>/dev/null || true
fi

echo "Installation terminée."
echo "Lancez l'app avec : imageoptimpro"
echo "Ou cherchez 'ImageOptim Pro' dans votre menu d'applications."
