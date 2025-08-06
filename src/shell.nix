# The follow works to get an editable install when the structuraltools directory
# is brought out from under src/

with import <nixpkgs> {}; (
    let
        structuraltools = python313Packages.mkPythonEditablePackage {
            pname = "structuraltools";
            version = "0.1.0";
            root = "./.";
        };
    in
    python313.withPackages (
        ps: with ps; [
            hatch
            hatchling
            numpy
            pandas
            pint
            pytest
            ruff
            setuptools
            sphinx
            sphinx-book-theme
            structuraltools
            sympy
        ]
    )
).env
