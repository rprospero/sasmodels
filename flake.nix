{
  # inputs.nixpkgs.url = "nixpkgs/nixos-unstable";
  inputs.nixpkgs.url = "nixpkgs/nixos-24.11";
  inputs.outdated.url = "nixpkgs/nixos-24.05";

  inputs.pyproject-nix.url = "github:pyproject-nix/pyproject.nix";
  inputs.pyproject-nix.inputs.nixpkgs.follows = "nixpkgs";

  inputs.hatch-sphinx.url = "github:llimeht/hatch-sphinx?ref=v0.0.3";
  inputs.hatch-sphinx.flake = false;

  inputs.siphash24.url = "github:dnicolodi/python-siphash24?ref=v1.7";
  inputs.siphash24.flake = false;

  inputs.columnize-src.url = "github:rocky/pycolumnize?ref=3.11";
  inputs.columnize-src.flake = false;

  outputs = { self, nixpkgs, outdated, pyproject-nix, hatch-sphinx, siphash24
    , columnize-src, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        past = import outdated { inherit system; };

        project =
          pyproject-nix.lib.project.loadPyproject { projectRoot = ./.; };
        python = pkgs.python312.override {
          packageOverrides = prev: super: {
            hatch-sphinx = self.packages.${system}.hatch-sphinx;
            columnize = self.packages.${system}.columnize;
            siphash24 = self.packages.${system}.siphash24;

            # Not actually tcc box, but we do not NEED tccbox, plus tccbox is *not* hermetic
            tccbox = self.packages.${system}.siphash24;
          };
        };

      in {

        # Build our package using `buildPythonPackage
        packages = {
          default = let
            # Returns an attribute set that can be passed to `buildPythonPackage`.
            attrs = project.renderers.buildPythonPackage { inherit python; };
            # Pass attributes to buildPythonPackage.
            # Here is a good spot to add on any missing or custom attributes.
          in python.pkgs.buildPythonPackage (attrs // {
            version = "v0.9.0";
            env.CUSTOM_ENVVAR = "hello";
            nativeBuildInputs = with pkgs; [ git tinycc ];
          });

          hatch-sphinx = python.pkgs.buildPythonPackage
            ((pyproject-nix.lib.project.loadPyproject {
              projectRoot = hatch-sphinx;
            }).renderers.buildPythonPackage { inherit python; } // {
              version = "v0.0.3";
            });

          columnize = python.pkgs.buildPythonPackage {
            pname = "pycolumnize";
            version = "3.11";
            src = columnize-src;
          };

          siphash24 = let
            attrs = (pyproject-nix.lib.project.loadPyproject {
              projectRoot = siphash24;
            }).renderers.buildPythonPackage { inherit python; };
          in python.pkgs.buildPythonPackage (attrs // { version = "1.7"; });
        };

        devShells.default = let
          # Returns a function that can be passed to `python.withPackages`
          arg = project.renderers.withPackages { inherit python; };

          # Returns a wrapped environment (virtualenv like) with all our packages
          pythonEnv = python.withPackages arg;

          # Create a devShell like normal.
        in pkgs.mkShell {
          packages = [
            pythonEnv
            past.hdfview
            pkgs.ruff
            pkgs.tinycc
            pkgs.python312Packages.python-lsp-server
            pkgs.python312Packages.python-lsp-ruff
            pkgs.python312Packages.pylsp-mypy
            pkgs.python312Packages.pylsp-rope
          ];
        };
      });
}
