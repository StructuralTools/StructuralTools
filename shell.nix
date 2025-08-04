# A similar shell.nix got me up and running with an editable install of
# innerscope, but this is giving me a `ModuleNotFoundError` when I try to import
# structuraltools.

with import <nixpkgs> {}; (
    let
        structuraltools = python313Packages.mkPythonEditablePackage {
            pname = "structuraltools";
            version = "0.1.0";
            root = "/home/joebot/git/structuraltools/src/structuraltools";
        };
    in
    python313.withPackages (
        ps: with ps; [
            numpy
            pandas
            pint
            pytest
            ruff
            sphinx
            sphinx-book-theme
            structuraltools
            sympy
        ]
    )
).env
