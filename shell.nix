with import <nixpkgs> {}; (
    let
        structuraltools = python313.pkgs.buildPythonPackage {
            pname = "structuraltools";
            version = "0.1.0";
            pyproject = true;

            src = ./.;

            build-system = with python313Packages; [
                setuptools
                setuptools-scm
            ];

            doCheck = false;

            dependencies = with python313Packages; [
                numpy
                pandas
                pint
                sympy
            ];
        };
    in
    python313.withPackages (
        ps: with ps; [
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
