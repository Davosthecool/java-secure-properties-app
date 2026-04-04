from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def _load_build_properties(properties_file: Path) -> dict[str, str]:
	properties: dict[str, str] = {}
	if not properties_file.exists():
		return properties

	for raw_line in properties_file.read_text(encoding="utf-8").splitlines():
		line = raw_line.strip()
		if not line or line.startswith("#"):
			continue

		if "=" not in line:
			continue

		key, value = line.split("=", 1)
		key = key.strip()
		value = value.strip()
		if key:
			properties[key] = value

	return properties


def build_exe() -> int:
	project_root = Path(__file__).resolve().parent
	main_file = project_root / "main.py"
	build_properties_file = project_root / "build.properties"

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
		f"{build_properties_file}{separator}.",
		f"{resources_dir}{separator}ressources",
	]

	build_properties = _load_build_properties(build_properties_file)
	app_version = build_properties.get("APP_VERSION", "dev").strip() or "dev"

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

	print(f"Using app version: {app_version}")
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
