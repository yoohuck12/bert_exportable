load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@my_deps//:requirements.bzl", "requirement")

py_library(
    name = "tokenization",
    srcs = [
        "tokenization.py",
    ],
    deps = [
        requirement("tensorflow"),
    ]
)

py_binary(
    name = "client",
    srcs = [
        "client.py",
    ],
    deps = [
        ":tokenization",
        requirement("grpcio"),
        requirement("numpy"),
        requirement("tensorflow"),
        requirement("tensorflow-serving-api")
    ]
)
