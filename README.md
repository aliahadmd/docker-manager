# Docker Manager

![Docker Manager Icon](./docker-manager-icon.svg)

A lightweight, user-friendly GUI application for managing Docker containers and images on Linux Mint and other Debian-based systems. Built with Python and Tkinter, Docker Manager provides an intuitive interface for common Docker operations.

## Features

- 🐳 **Container Management**
  - View all containers with real-time status updates
  - Start, stop, and remove containers
  - View container details including ports and status
  - Auto-refresh container list

- 📦 **Image Management**
  - List all Docker images
  - Pull new images from Docker Hub
  - Remove unused images
  - View image details including size and tags

- 📝 **Logging System**
  - Real-time operation logs
  - Error tracking and display
  - Timestamp for all operations



1. Launch Docker Manager from the application menu or run `docker-manager` in terminal
2. Ensure Docker daemon is running (`sudo systemctl start docker`)
3. Use the tabs to navigate between container and image management
4. Right-click on containers or images for additional options
5. Check the logs tab for operation history and errors



## Roadmap

- [ ] Add container creation wizard
- [ ] Implement docker-compose support
- [ ] Add network management
- [ ] Include volume management
- [ ] Add dark mode support
- [ ] Implement search functionality
- [ ] Add container resource monitoring

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Docker team for the excellent Docker Engine API
- Python Tkinter documentation and community
- Linux Mint team for the excellent distribution

## Support

---

Made with ❤️ for the Docker community