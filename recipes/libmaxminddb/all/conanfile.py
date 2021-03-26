import os
import shutil
from conans import ConanFile, CMake, tools


class libmaxminddbConan(ConanFile):
    name = "libmaxminddb"
    license = "Apache-2.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "http://maxmind.github.io/libmaxminddb/"
    description = "C library for the MaxMind DB file format"
    topics = ("MaxMind", "GeoIP")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("libmaxminddb-{}".format(self.version), self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake

        cmake = CMake(self)
        cmake.configure(source_folder=self._source_subfolder, build_folder=self._build_subfolder)

        self._cmake = cmake
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        shutil.rmtree(os.path.join(self.package_folder, "lib", "cmake"))
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        libname = "libmaxminddb" if self.settings.os == "Windows" else "maxminddb"
        self.cpp_info.libs = [libname]
        self.cpp_info.names["cmake_find_package"] = "maxminddb"
        self.cpp_info.filenames["cmake_find_package"] = "maxminddb"
        self.cpp_info.names["cmake_find_package_multi"] = "maxminddb"
        self.cpp_info.filenames["cmake_find_package_multi"] = "maxminddb"

        if self.settings.os == "Windows":
            self.cpp_info.system_libs = ["ws2_32"]

        bin_path = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH environment variable: {}".format(bin_path))
        self.env_info.PATH.append(bin_path)
