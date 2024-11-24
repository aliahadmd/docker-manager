#!/bin/bash

# Create package directory structure
mkdir -p docker-manager_1.0-1/DEBIAN
mkdir -p docker-manager_1.0-1/usr/bin
mkdir -p docker-manager_1.0-1/usr/share/applications
mkdir -p docker-manager_1.0-1/usr/share/icons/hicolor/scalable/apps
mkdir -p docker-manager_1.0-1/usr/lib/docker-manager

# Create control file
cat > docker-manager_1.0-1/DEBIAN/control << EOL
Package: docker-manager
Version: 1.0-1
Section: utils
Priority: optional
Architecture: all
Depends: python3 (>= 3.6), python3-tk, docker-ce | docker.io
Maintainer: Ali Ahad <ali@aliahad.com>
Description: Docker Manager GUI
 A graphical user interface for managing Docker containers
 and images on Linux systems. Provides easy access to common
 Docker operations through a user-friendly interface.
EOL

# Create postinst script
cat > docker-manager_1.0-1/DEBIAN/postinst << EOL
#!/bin/bash
chmod +x /usr/bin/docker-manager
EOL

# Make postinst executable
chmod 755 docker-manager_1.0-1/DEBIAN/postinst

# Copy application files
cp docker_manager.py docker-manager_1.0-1/usr/lib/docker-manager/
cp docker-manager-icon.svg docker-manager_1.0-1/usr/share/icons/hicolor/scalable/apps/docker-manager.svg

# Create launcher script
cat > docker-manager_1.0-1/usr/bin/docker-manager << EOL
#!/bin/bash
python3 /usr/lib/docker-manager/docker_manager.py
EOL

# Create desktop entry
cat > docker-manager_1.0-1/usr/share/applications/docker-manager.desktop << EOL
[Desktop Entry]
Version=1.0
Type=Application
Name=Docker Manager
Comment=Manage Docker containers and images
Exec=docker-manager
Icon=docker-manager
Categories=System;
Terminal=false
EOL

# Set permissions
chmod 755 docker-manager_1.0-1/usr/bin/docker-manager
chmod 644 docker-manager_1.0-1/usr/share/applications/docker-manager.desktop
chmod 644 docker-manager_1.0-1/usr/share/icons/hicolor/scalable/apps/docker-manager.svg
chmod 644 docker-manager_1.0-1/usr/lib/docker-manager/docker_manager.py

# Build the package
dpkg-deb --build docker-manager_1.0-1