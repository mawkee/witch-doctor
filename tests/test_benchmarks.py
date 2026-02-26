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


class ServiceWithArgs(IService):
    def __init__(self, a: int, b: str, c: float):
        self.a = a
        self.b = b
        self.c = c

    def execute(self) -> str:
        return f"{self.a}-{self.b}-{self.c}"


class TestRegistrationBenchmarks:
    def test_register_factory(self, benchmark):
        def register():
            WitchDoctor._reset()
            WitchDoctor.register(IService, ServiceImpl, InjectionType.FACTORY)

        benchmark(register)

    def test_register_singleton(self, benchmark):
        def register():
            WitchDoctor._reset()
            WitchDoctor.register(IService, ServiceImpl, InjectionType.SINGLETON)

        benchmark(register)

    def test_register_with_args(self, benchmark):
        def register():
            WitchDoctor._reset()
            WitchDoctor.register(
                IService, ServiceWithArgs, InjectionType.FACTORY, args=[1, "test", 3.14]
            )

        benchmark(register)


class TestResolutionBenchmarks:
    def test_resolve_factory(self, benchmark):
        WitchDoctor.register(IService, ServiceImpl, InjectionType.FACTORY)
        WitchDoctor.load_container()

        benchmark(lambda: WitchDoctor.resolve(IService))

    def test_resolve_singleton(self, benchmark):
        WitchDoctor.register(IService, ServiceImpl, InjectionType.SINGLETON)
        WitchDoctor.load_container()

        benchmark(lambda: WitchDoctor.resolve(IService))

    def test_resolve_factory_with_args(self, benchmark):
        WitchDoctor.register(
            IService, ServiceWithArgs, InjectionType.FACTORY, args=[1, "test", 3.14]
        )
        WitchDoctor.load_container()

        benchmark(lambda: WitchDoctor.resolve(IService))


class TestInjectionBenchmarks:
    def test_injection_single_dependency(self, benchmark):
        WitchDoctor.register(IService, ServiceImpl, InjectionType.FACTORY)
        WitchDoctor.load_container()

        @WitchDoctor.injection
        def func(service: IService):
            return service.execute()

        benchmark(func)

    def test_injection_singleton(self, benchmark):
        WitchDoctor.register(IService, ServiceImpl, InjectionType.SINGLETON)
        WitchDoctor.load_container()

        @WitchDoctor.injection
        def func(service: IService):
            return service.execute()

        benchmark(func)

    def test_injection_with_regular_args(self, benchmark):
        WitchDoctor.register(IService, ServiceImpl, InjectionType.FACTORY)
        WitchDoctor.load_container()

        @WitchDoctor.injection
        def func(a: int, b: str, service: IService):
            return f"{a}-{b}-{service.execute()}"

        benchmark(lambda: func(1, "test"))

    def test_injection_multiple_dependencies(self, benchmark):
        class IService2(ABC):
            @abstractmethod
            def execute(self) -> str:
                pass

        class Service2Impl(IService2):
            def execute(self) -> str:
                return "service2"

        class IService3(ABC):
            @abstractmethod
            def execute(self) -> str:
                pass

        class Service3Impl(IService3):
            def execute(self) -> str:
                return "service3"

        WitchDoctor.register(IService, ServiceImpl, InjectionType.FACTORY)
        WitchDoctor.register(IService2, Service2Impl, InjectionType.FACTORY)
        WitchDoctor.register(IService3, Service3Impl, InjectionType.FACTORY)
        WitchDoctor.load_container()

        @WitchDoctor.injection
        def func(s1: IService, s2: IService2, s3: IService3):
            return f"{s1.execute()}-{s2.execute()}-{s3.execute()}"

        benchmark(func)


class TestContainerBenchmarks:
    def test_container_creation(self, benchmark):
        counter = [0]

        def create_container():
            name = f"container_{counter[0]}"
            counter[0] += 1
            return WitchDoctor.container(name)

        benchmark(create_container)

    def test_container_load(self, benchmark):
        WitchDoctor.container("bench_container")

        benchmark(lambda: WitchDoctor.load_container("bench_container"))

    def test_full_workflow(self, benchmark):
        counter = [0]

        def workflow():
            name = f"workflow_{counter[0]}"
            counter[0] += 1
            container = WitchDoctor.container(name)
            container(IService, ServiceImpl, InjectionType.SINGLETON)
            WitchDoctor.load_container(name)
            return WitchDoctor.resolve(IService)

        benchmark(workflow)
