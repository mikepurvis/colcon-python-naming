from colcon_core.dependency_descriptor import DependencyDescriptor
from colcon_core.package_augmentation import PackageAugmentationExtensionPoint
import copy

__version__ = '0.0.0'


class PythonPackageRenamer(PackageAugmentationExtensionPoint):
    def augment_packages(self, package_descriptors, *, additional_argument_names=None):
        for package_descriptor in package_descriptors:
            if package_descriptor.type == 'python':
                self._rename_package(package_descriptor)

    def _rename_package(self, package_descriptor):
        """
        Renames a package descriptor in-place.
        """
        package_descriptor.name = self._rename_name(package_descriptor.name)
        for deptype in package_descriptor.dependencies:
            self._rename_dependency_set(package_descriptor.dependencies[deptype])
        print(package_descriptor.name, package_descriptor) 

    def _rename_dependency_set(self, dependency_set):
        """
        Renames a dependency set in-place.
        """
        renamed_deps = set()
        for dep in dependency_set:
            renamed_deps.add(self._rename_dependency(dep))
        dependency_set.clear()
        dependency_set.update(renamed_deps)

    def _rename_dependency(self, dependency):
        """
        Renames an individual dependency and returns the result.
        """
        if isinstance(dependency, DependencyDescriptor):
            dependency = DependencyDescriptor(
                self._rename_name(dependency.name),
                metadata=copy.deepcopy(dependency.metadata)
            )
        elif isinstance(dependency, str):
            dependency = self._rename_name(dependency)
        return dependency

    def _rename_name(self, name):
        return f'python3-{name.lower()}'
