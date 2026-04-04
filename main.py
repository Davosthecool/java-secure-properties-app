from pathlib import Path
import importlib.util


def _load_app_interface_module():
	app_interface_path = Path(__file__).with_name("app-interface.py")
	spec = importlib.util.spec_from_file_location("app_interface", app_interface_path)
	if spec is None or spec.loader is None:
		raise ImportError("Unable to load app-interface.py")

	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


def main() -> int:
	app_interface = _load_app_interface_module()
	return app_interface.run_app()


if __name__ == "__main__":
	raise SystemExit(main())
