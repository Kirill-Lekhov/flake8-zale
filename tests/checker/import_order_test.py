from src.checker.import_order import ImportOrderChecker, PackageType
from src.constant import ErrorCode

from unittest.mock import Mock, patch
from ast import Module, parse
from argparse import Namespace
from typing import Optional

import pytest


def make_checker(tree: Optional[Module] = None, project_packages: str = "") -> ImportOrderChecker:
	return ImportOrderChecker(tree or Module([], []), False, Namespace(project_packages=project_packages))


class TestImportOrderChecker:
	def test___init__(self):
		tree = Module([], [])
		options = Namespace(project_packages="project1,project2")
		checker = ImportOrderChecker(tree, True, options)

		assert checker.project_packages == frozenset()

		with patch.object(ImportOrderChecker, "check") as check_method:
			checker = ImportOrderChecker(tree, False, options)
			check_method.assert_called_once()
			assert check_method.call_args_list[0][0][0] is tree

	def test_check__without_tree_body(self):
		checker = make_checker(Module([], []))
		assert checker.error_messages == []

	def test_check__without_imports(self):
		checker = make_checker(
			parse("""\
name = input('Enter your name:')
print("Hello,", name)
""")
		)
		assert checker.error_messages == []

	def test_check__import_order_errors(self):
		checker = make_checker(
			parse("""\
import package

from src import module
"""),
			"src,app",
		)
		assert len(checker.error_messages) == 1
		assert checker.error_messages[0].error_code is ErrorCode.INVALID_IMPORT_ORDER
		assert checker.error_messages[0].line_number == 3
		assert checker.error_messages[0].column == 22

		checker = make_checker(
			parse("""\
import math

from src import module
"""),
			"src,app",
		)

		assert len(checker.error_messages) == 1
		assert checker.error_messages[0].error_code is ErrorCode.INVALID_IMPORT_ORDER
		assert checker.error_messages[0].line_number == 3
		assert checker.error_messages[0].column == 22

		checker = make_checker(
			parse("""\
from package import app

from src import module

import math
"""),
			"src,app",
		)

		assert len(checker.error_messages) == 2
		assert checker.error_messages[0].error_code is ErrorCode.INVALID_IMPORT_ORDER
		assert checker.error_messages[0].line_number == 3
		assert checker.error_messages[0].column == 22

		assert checker.error_messages[1].error_code is ErrorCode.INVALID_IMPORT_ORDER
		assert checker.error_messages[1].line_number == 5
		assert checker.error_messages[1].column == 11

		checker = make_checker(
			parse("""\
import math

from src import module

from package import app
"""),
			"src,app",
		)

		assert len(checker.error_messages) == 1
		assert checker.error_messages[0].error_code is ErrorCode.INVALID_IMPORT_ORDER
		assert checker.error_messages[0].line_number == 3
		assert checker.error_messages[0].column == 22

		checker = make_checker(parse("import math, app"), "src,app")

		assert len(checker.error_messages) == 1
		assert checker.error_messages[0].error_code is ErrorCode.MIXED_IMPORT
		assert checker.error_messages[0].line_number == 1
		assert checker.error_messages[0].column == 16

	def test_check_warnings(self):
		checker = make_checker()

		with patch.object(checker, "get_package_type") as get_package_type_method:
			get_package_type_method.return_value = None

			with pytest.warns(UserWarning, match="Unknown package type: None"):
				checker.check(parse("import app"))

	def test_check__without_errors(self):
		checker = make_checker(
			parse("""\
import app
from src import module
from ..package import module1 as module2

import re
from math import cos

import flake8
from pytest.mark import parametrize
"""),
			"src,app",
		)

		assert checker.error_messages == []

	def test_get_package_type(self):
		checker = make_checker()

		with patch.object(checker, "is_project_package") as is_project_package_method:
			is_project_package_method.return_value = False

			with patch.object(checker, "is_std_package") as is_std_package_method:
				is_std_package_method.return_value = False

				assert checker.get_package_type("package") is PackageType.EXTERNAL
				is_project_package_method.assert_called_once_with("package")
				is_std_package_method.assert_called_once_with("package")

				is_std_package_method.reset_mock(return_value=True)
				is_project_package_method.reset_mock(return_value=False)

				assert checker.get_package_type("package") is PackageType.STD
				is_project_package_method.assert_called_once_with("package")
				is_std_package_method.assert_called_once_with("package")

				is_std_package_method.reset_mock(return_value=False)
				is_project_package_method.reset_mock(return_value=True)

				assert checker.get_package_type("package") is PackageType.PROJECT
				is_project_package_method.assert_called_once_with("package")
				is_std_package_method.assert_not_called()

	def test_is_project_package(self):
		checker = make_checker(project_packages="package1,package2")

		assert not checker.is_project_package("package3")
		assert not checker.is_project_package("package3.package1")
		assert not checker.is_project_package("package3.package2.package1")
		assert checker.is_project_package("package1.package2.package3")
		assert checker.is_project_package("package2.package1")
		assert checker.is_project_package("package2")
		assert checker.is_project_package("package1")

	def test_is_std_package(self):
		with patch.object(ImportOrderChecker, "STD_PACKAGES", frozenset(["package1", "package2"])):
			checker = make_checker()

			assert not checker.is_std_package("package3")
			assert not checker.is_std_package("package3.package1")
			assert not checker.is_std_package("package3.package2.package1")
			assert checker.is_std_package("package1.package2.package3")
			assert checker.is_std_package("package2.package1")
			assert checker.is_std_package("package2")
			assert checker.is_std_package("package1")

	def test_add_options(self):
		fake_option_manager = Mock()
		fake_option_manager.add_option = Mock()
		ImportOrderChecker.add_options(fake_option_manager)

		fake_option_manager.add_option.assert_called_once_with(
			"--project-packages",
			default=None,
			parse_from_config=True,
			help="Name of project packages",
		)
