from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def build_exe() -> int:
	project_root = Path(__file__).resolve().parent
	main_file = project_root / "main.py"

	if not main_file.exists():
		print(f"main.py not found: {main_file}")
		return 1

	resources_dir = project_root / "ressources"
	dist_dir = project_root / "dist"

	if not resources_dir.exists():
		print("Unable to find resources directory (expected ressources/ or utils/ressources/).")
		return 1

	dist_dir.mkdir(exist_ok=True)

	separator = ";" if sys.platform.startswith("win") else ":"
	data_files = [
		f"{project_root / 'app-interface.py'}{separator}.",
		f"{project_root / 'secure-properties-executor.py'}{separator}.",
		f"{resources_dir}{separator}ressources",
	]

	command = [
		sys.executable,
		"-m",
		"PyInstaller",
		"--noconfirm",
		"--clean",
		"--onefile",
		"--specpath",
		str(dist_dir),
		"--name",
		"secure-properties-app",
		"--windowed",
		"--hidden-import",
		"PyQt6",
		"--hidden-import",
		"PyQt6.QtCore",
		"--hidden-import",
		"PyQt6.QtWidgets",
		"--collect-submodules",
		"PyQt6",
	]

	for data in data_files:
		command.extend(["--add-data", data])

	command.append(str(main_file))

	print("Running:", " ".join(command))
	result = subprocess.run(command, cwd=project_root)
	if result.returncode != 0:
		print("Build failed.")
		return result.returncode

	print("Build succeeded.")
	print(f"EXE file: {project_root / 'dist' / 'secure-properties-app.exe'}")
	return 0


if __name__ == "__main__":
	raise SystemExit(build_exe())
