from src.checker.iface import TreeChecker
from src.error_message import ErrorMessage
from src.constant import ErrorCode

from argparse import Namespace
from ast import Import, ImportFrom, Module
from typing import Final, Set
from enum import IntEnum
from warnings import warn

from stdlib_list import stdlib_list


class PackageType(IntEnum):
	PROJECT = 1
	STD = 2
	EXTERNAL = 3


class ImportOrderChecker(TreeChecker):
	STD_PACKAGES: Final[Set[str]] = set(stdlib_list())

	project_packages: Final[Set[str]]

	def __init__(self, tree: Module, noqa: bool, options: Namespace) -> None:
		super(TreeChecker, self).__init__(options)

		if not noqa:
			self.project_packages = set((self.options.project_packages or "").split(","))
			self.check(tree)

	def check(self, tree):
		project_packages_imported = False
		std_packages_imported = False
		external_packages_imported = False

		for token in tree.body:
			project_package_import = False
			std_package_import = False
			external_package_import = False

			if isinstance(token, Import):
				package_types = {self.get_package_type(i.name) for i in token.names}

				if len(package_types) > 1:
					self.error_messages.append(
						# TODO: Check in which case the positions may not be specified
						ErrorMessage(ErrorCode.MIXED_IMPORT, token.end_lineno or 0, token.end_col_offset or 0)
					)

				if PackageType.PROJECT in package_types:
					project_package_import = True
				elif PackageType.STD in package_types:
					std_package_import = True
				elif PackageType.EXTERNAL in package_types:
					external_package_import = True
				else:
					warn(f"Unknown package type: {package_types.pop()}")

			elif isinstance(token, ImportFrom):
				if token.level == 0:
					if self.is_project_package(token.module or ""):		# Module cannot be None when level is not 0
						project_package_import = True
					elif self.is_std_package(token.module or ""):
						std_package_import = True
					else:
						external_package_import = True
				else:
					project_package_import = True
			else:
				continue

			if (
				(project_package_import and (std_packages_imported or external_packages_imported)) or
				(std_package_import and external_packages_imported)
			):
				self.error_messages.append(
					ErrorMessage(ErrorCode.INVALID_IMPORT_ORDER, token.end_lineno or 0, token.end_col_offset or 0)
				)

			project_packages_imported |= project_package_import
			std_packages_imported |= std_package_import
			external_packages_imported |= external_package_import

	def get_package_type(self, package_name: str) -> PackageType:
		if self.is_project_package(package_name):
			return PackageType.PROJECT
		elif self.is_std_package(package_name):
			return PackageType.STD

		return PackageType.EXTERNAL

	def is_project_package(self, package_name: str) -> bool:
		return package_name.split(".")[0] in self.project_packages

	def is_std_package(self, package_name: str) -> bool:
		return package_name.split(".")[0] in self.STD_PACKAGES

	@classmethod
	def add_options(cls, option_manager) -> None:
		option_manager.add_option(
			"--project-packages",
			default=None,
			parse_from_config=True,
			help="Name of project packages",
		)
