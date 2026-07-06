import frappe


def _unwrap_hook_value(value):
	if isinstance(value, list):
		return value[-1] if value else None

	if isinstance(value, dict):
		return {key: _unwrap_hook_value(val) for key, val in value.items()}

	return value


def get_print_engines() -> dict:
	"""Print engines registered by installed apps via the `print_engines` hook."""
	return {
		name: _unwrap_hook_value(config) for name, config in frappe.get_hooks("print_engines", {}).items()
	}
