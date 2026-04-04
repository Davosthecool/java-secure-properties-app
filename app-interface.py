from __future__ import annotations

from pathlib import Path
import importlib.util
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
	QApplication,
	QCheckBox,
	QComboBox,
	QDialog,
	QDialogButtonBox,
	QFileDialog,
	QFormLayout,
	QGridLayout,
	QGroupBox,
	QHBoxLayout,
	QLabel,
	QLineEdit,
	QMainWindow,
	QMessageBox,
	QPushButton,
	QRadioButton,
	QTextEdit,
	QVBoxLayout,
	QWidget,
)


PROJECT_NAME = "Java Secure Properties App"
PROJECT_DESCRIPTION = "Interface pour chiffrer/déchiffrer des valeurs via MuleSoft Secure Properties Tool."
PROJECT_VERSION = "1.0.0"
PROJECT_AUTHOR = "David CHOCHO"
PROJECT_SOURCE_URL = "https://github.com/Davosthecool/java-secure-properties-app"


def _load_executor_module():
	executor_path = Path(__file__).with_name("secure-properties-executor.py")
	spec = importlib.util.spec_from_file_location("secure_properties_executor", executor_path)
	if spec is None or spec.loader is None:
		raise ImportError("Unable to load secure-properties-executor.py")

	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


_executor = _load_executor_module()
execute_secure_properties = _executor.execute_secure_properties


def _find_default_jar() -> str:
	default_path = Path(__file__).resolve().parent / "ressources" / "secure-properties-tool-j17.jar"

	if default_path.exists():
		return str(default_path)

	return ""


class SecurePropertiesWindow(QMainWindow):
	def __init__(self) -> None:
		super().__init__()
		self.setWindowTitle("MuleSoft Secure Properties Tool")
		self.resize(600, 800)
		self._build_ui()

	def _build_ui(self) -> None:
		central = QWidget()
		self.setCentralWidget(central)

		root_layout = QVBoxLayout()
		central.setLayout(root_layout)

		top_layout = QHBoxLayout()
		top_layout.addStretch(1)
		self.info_button = QPushButton("Infos")
		self.info_button.setMaximumWidth(90)
		self.info_button.clicked.connect(self._on_show_infos)
		top_layout.addWidget(self.info_button)

		root_layout.addLayout(top_layout)

		root_layout.addWidget(self._build_config_group())
		root_layout.addWidget(self._build_action_group())
		root_layout.addWidget(self._build_data_group())
		root_layout.addWidget(self._build_result_group())

	def _build_config_group(self) -> QGroupBox:
		group = QGroupBox("Configuration")
		form = QFormLayout()

		default_jar = _find_default_jar()

		self.jar_input = QLineEdit(default_jar)
		self.browse_jar_button = QPushButton("Browse...")
		self.browse_jar_button.clicked.connect(self._on_browse_jar)

		jar_layout = QHBoxLayout()
		jar_layout.addWidget(self.jar_input)
		jar_layout.addWidget(self.browse_jar_button)
		self.key_input = QLineEdit()
		self.key_input.setPlaceholderText("Encryption key")
		self.key_input.setEchoMode(QLineEdit.EchoMode.Password)
		self.show_key_checkbox = QCheckBox("Show key")
		self.show_key_checkbox.toggled.connect(self._on_toggle_key_visibility)

		key_layout = QHBoxLayout()
		key_layout.addWidget(self.key_input)
		key_layout.addWidget(self.show_key_checkbox)

		self.algorithm_combo = QComboBox()
		self.algorithm_combo.addItems(["AES", "Blowfish", "DES", "DESede"])

		self.mode_combo = QComboBox()
		self.mode_combo.addItems(["CBC", "CFB", "ECB", "OFB"])

		self.random_iv_checkbox = QCheckBox("Use random IV")
		self.random_iv_checkbox.setChecked(False)

		form.addRow("JAR path", jar_layout)
		form.addRow("Key", key_layout)
		form.addRow("Algorithm", self.algorithm_combo)
		form.addRow("Mode", self.mode_combo)
		form.addRow("", self.random_iv_checkbox)

		group.setLayout(form)
		return group

	def _build_action_group(self) -> QGroupBox:
		group = QGroupBox("Action")
		layout = QHBoxLayout()

		self.encrypt_radio = QRadioButton("Encrypt")
		self.decrypt_radio = QRadioButton("Decrypt")
		self.encrypt_radio.setChecked(True)

		layout.addWidget(self.encrypt_radio)
		layout.addWidget(self.decrypt_radio)
		layout.addStretch(1)
		group.setLayout(layout)
		return group

	def _build_data_group(self) -> QGroupBox:
		group = QGroupBox("Input Data")
		layout = QVBoxLayout()

		self.input_data = QTextEdit()
		self.input_data.setPlaceholderText("Text to encrypt/decrypt")

		button_layout = QGridLayout()
		self.execute_button = QPushButton("Execute")
		self.clear_button = QPushButton("Clear")

		self.execute_button.clicked.connect(self._on_execute)
		self.clear_button.clicked.connect(self._on_clear)

		button_layout.addWidget(self.execute_button, 0, 0)
		button_layout.addWidget(self.clear_button, 0, 1)

		layout.addWidget(self.input_data)
		layout.addLayout(button_layout)
		group.setLayout(layout)
		return group

	def _build_result_group(self) -> QGroupBox:
		group = QGroupBox("Result")
		layout = QVBoxLayout()

		info = QLabel("Execution output from SecurePropertiesTool")
		info.setAlignment(Qt.AlignmentFlag.AlignLeft)

		self.result_data = QTextEdit()
		self.result_data.setReadOnly(True)
		self.copy_result_button = QPushButton("Copy result")
		self.copy_result_button.clicked.connect(self._on_copy_result)

		layout.addWidget(info)
		layout.addWidget(self.result_data)
		layout.addWidget(self.copy_result_button)
		group.setLayout(layout)
		return group

	def _on_clear(self) -> None:
		self.input_data.clear()
		self.result_data.clear()

	def _on_browse_jar(self) -> None:
		selected_file, _ = QFileDialog.getOpenFileName(
			self,
			"Select secure-properties tool JAR",
			str(Path(self.jar_input.text().strip()).parent if self.jar_input.text().strip() else Path.cwd()),
			"JAR files (*.jar);;All files (*)",
		)

		if selected_file:
			self.jar_input.setText(selected_file)

	def _on_toggle_key_visibility(self, is_visible: bool) -> None:
		mode = QLineEdit.EchoMode.Normal if is_visible else QLineEdit.EchoMode.Password
		self.key_input.setEchoMode(mode)

	def _on_show_infos(self) -> None:
		dialog = QDialog(self)
		dialog.setWindowTitle("Infos projet")
		dialog.setMinimumWidth(450)

		layout = QVBoxLayout(dialog)
		info_label = QLabel(
			f"<b>{PROJECT_NAME}</b><br><br>"
			f"{PROJECT_DESCRIPTION}<br><br>"
			f"<b>Version:</b> {PROJECT_VERSION}<br>"
			f"<b>Auteur:</b> {PROJECT_AUTHOR}<br>"
			f"<b>Source code:</b> <a href='{PROJECT_SOURCE_URL}'>{PROJECT_SOURCE_URL}</a>"
		)
		info_label.setTextFormat(Qt.TextFormat.RichText)
		info_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
		info_label.setOpenExternalLinks(True)
		info_label.setWordWrap(True)

		buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
		buttons.accepted.connect(dialog.accept)

		layout.addWidget(info_label)
		layout.addWidget(buttons)

		dialog.exec()

	def _on_copy_result(self) -> None:
		result_text = self.result_data.toPlainText()
		if not result_text.strip():
			QMessageBox.information(self, "Nothing to copy", "There is no result to copy yet.")
			return

		QApplication.clipboard().setText(result_text)
		QMessageBox.information(self, "Copied", "Result copied to clipboard.")

	def _validate_form(self) -> bool:
		jar_path = self.jar_input.text().strip()
		key = self.key_input.text().strip()
		data = self.input_data.toPlainText().strip()

		if not jar_path:
			QMessageBox.warning(self, "Missing value", "Please provide a JAR path.")
			return False
		if not Path(jar_path).exists():
			QMessageBox.warning(self, "Invalid path", "JAR file not found.")
			return False
		if not key:
			QMessageBox.warning(self, "Missing value", "Please provide an encryption key.")
			return False
		if not data:
			QMessageBox.warning(self, "Missing value", "Please provide input data.")
			return False

		return True

	def _on_execute(self) -> None:
		if not self._validate_form():
			return

		jar_path = self.jar_input.text().strip()
		key = self.key_input.text().strip()
		data = self.input_data.toPlainText().strip()
		is_encryption = self.encrypt_radio.isChecked()
		algorithm = self.algorithm_combo.currentText()
		mode = self.mode_combo.currentText()
		use_random_iv = self.random_iv_checkbox.isChecked()

		self.execute_button.setEnabled(False)
		self.result_data.setPlainText("Running command...")

		output = execute_secure_properties(
			jar_path=jar_path,
			encryption_key=key,
			data=data,
			is_encryption=is_encryption,
			algorithm=algorithm,
			mode=mode,
			use_random_iv=use_random_iv,
		)

		self.execute_button.setEnabled(True)

		if output is None:
			self.result_data.setPlainText("Execution failed. Check terminal logs for details.")
			return

		self.result_data.setPlainText(output)


def run_app() -> int:
	app = QApplication(sys.argv)
	window = SecurePropertiesWindow()
	window.show()
	return app.exec()
