from abc import ABC, abstractmethod

import pytest

from witch_doctor import WitchDoctor, InjectionType


class IService(ABC):
    @abstractmethod
    def execute(self) -> str:
        pass


class ServiceImpl(IService):
    def execute(self) -> str:
        return "executed"


class TestContainerSpecialNames:
    def test_container_with_empty_name(self):
        container = WitchDoctor.container("")
        container(IService, ServiceImpl, InjectionType.FACTORY)
        assert "" in WitchDoctor._injection_map

    def test_container_with_underscore_prefix(self):
        container = WitchDoctor.container("__private__")
        container(IService, ServiceImpl, InjectionType.FACTORY)
        assert "__private__" in WitchDoctor._injection_map

    def test_container_with_unicode_name(self):
        container = WitchDoctor.container("contenedor_español")
        container(IService, ServiceImpl, InjectionType.FACTORY)
        assert "contenedor_español" in WitchDoctor._injection_map

    def test_container_with_whitespace_name(self):
        container = WitchDoctor.container("  spaced  ")
        container(IService, ServiceImpl, InjectionType.FACTORY)
        assert "  spaced  " in WitchDoctor._injection_map


class TestDuplicateRegistration:
    def test_duplicate_registration_overwrites(self):
        class ServiceImpl2(IService):
            def execute(self) -> str:
                return "second"

        WitchDoctor.register(IService, ServiceImpl, InjectionType.FACTORY)
        WitchDoctor.register(IService, ServiceImpl2, InjectionType.FACTORY)
        WitchDoctor.load_container()

        instance = WitchDoctor.resolve(IService)
        assert instance.execute() == "second"

    def test_duplicate_registration_different_injection_type(self):
        WitchDoctor.register(IService, ServiceImpl, InjectionType.FACTORY)
        WitchDoctor.register(IService, ServiceImpl, InjectionType.SINGLETON)
        WitchDoctor.load_container()

        instance1 = WitchDoctor.resolve(IService)
        instance2 = WitchDoctor.resolve(IService)
        assert id(instance1) == id(instance2)


class TestInvalidTypes:
    def test_register_none_interface(self):
        with pytest.raises(TypeError):
            WitchDoctor.register(None, ServiceImpl, InjectionType.FACTORY)

    def test_register_none_class_ref(self):
        with pytest.raises(TypeError):
            WitchDoctor.register(IService, None, InjectionType.FACTORY)

    def test_register_with_non_class_interface(self):
        with pytest.raises(TypeError):
            WitchDoctor.register("not_a_class", ServiceImpl, InjectionType.FACTORY)

    def test_register_with_non_class_implementation(self):
        with pytest.raises(TypeError):
            WitchDoctor.register(IService, "not_a_class", InjectionType.FACTORY)


class TestContainerIsolation:
    def test_containers_are_isolated(self):
        class ServiceA(IService):
            def execute(self) -> str:
                return "A"

        class ServiceB(IService):
            def execute(self) -> str:
                return "B"

        container_a = WitchDoctor.container("container_a")
        container_a(IService, ServiceA, InjectionType.FACTORY)

        container_b = WitchDoctor.container("container_b")
        container_b(IService, ServiceB, InjectionType.FACTORY)

        WitchDoctor.load_container("container_a")
        assert WitchDoctor.resolve(IService).execute() == "A"

        WitchDoctor.load_container("container_b")
        assert WitchDoctor.resolve(IService).execute() == "B"


class TestArgsHandling:
    def test_register_with_empty_args_list(self):
        WitchDoctor.register(IService, ServiceImpl, InjectionType.FACTORY, args=[])
        WitchDoctor.load_container()
        instance = WitchDoctor.resolve(IService)
        assert instance.execute() == "executed"

    def test_factory_with_args(self):
        class ServiceWithArgs(IService):
            def __init__(self, value: int):
                self.value = value

            def execute(self) -> str:
                return f"value={self.value}"

        WitchDoctor.register(
            IService, ServiceWithArgs, InjectionType.FACTORY, args=[42]
        )
        WitchDoctor.load_container()

        instance1 = WitchDoctor.resolve(IService)
        instance2 = WitchDoctor.resolve(IService)

        assert instance1.execute() == "value=42"
        assert instance2.execute() == "value=42"
        assert id(instance1) != id(instance2)


class TestSingletonBehavior:
    def test_singleton_returns_same_instance_across_resolves(self):
        WitchDoctor.register(IService, ServiceImpl, InjectionType.SINGLETON)
        WitchDoctor.load_container()

        instances = [WitchDoctor.resolve(IService) for _ in range(10)]
        first_id = id(instances[0])
        assert all(id(inst) == first_id for inst in instances)

    def test_singleton_persists_across_container_loads(self):
        WitchDoctor.register(IService, ServiceImpl, InjectionType.SINGLETON)
        WitchDoctor.load_container()

        instance1 = WitchDoctor.resolve(IService)
        WitchDoctor.load_container()
        instance2 = WitchDoctor.resolve(IService)

        assert id(instance1) == id(instance2)
