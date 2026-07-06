from frappe.printing import get_print_engines
from frappe.tests import UnitTestCase


class TestPrintEngines(UnitTestCase):
	def test_get_print_engines_returns_empty_dict_without_hooks(self):
		with self.patch_hooks({"print_engines": {}}):
			self.assertEqual(get_print_engines(), {})

	def test_get_print_engines_unwraps_aggregated_hook_values(self):
		with self.patch_hooks(
			{
				"print_engines": {
					"test": [
						{"renderer": "old-renderer", "script": "old.bundle.js"},
						{"renderer": "test-renderer", "script": "test.bundle.js"},
					]
				}
			}
		):
			self.assertEqual(
				get_print_engines(),
				{"test": {"renderer": "test-renderer", "script": "test.bundle.js"}},
			)

	def test_get_print_engines_unwraps_nested_dict_values(self):
		with self.patch_hooks(
			{
				"print_engines": {
					"test": {
						"renderer": ["test-renderer"],
						"script": ["test.bundle.js"],
						"options": {
							"route": ["old-route", "test-route"],
							"enabled": [True],
						},
					}
				}
			}
		):
			self.assertEqual(
				get_print_engines(),
				{
					"test": {
						"renderer": "test-renderer",
						"script": "test.bundle.js",
						"options": {"route": "test-route", "enabled": True},
					}
				},
			)
