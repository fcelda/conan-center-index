import os.path

from conans import ConanFile, CMake, tools


class libmaxminddbTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "pkg_config"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self):
            self.run(os.path.join(".", "example"), run_environment=True)
