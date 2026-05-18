{
  description = "Moondrop Dawn Pro USB control utility";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
    in {
      packages = forAllSystems (system:
        let pkgs = nixpkgs.legacyPackages.${system};
        in {
          default = pkgs.python3Packages.buildPythonApplication {
            pname = "dawn-pro-control";
            version = "0.1.0";
            src = ./.;
            format = "other";
            nativeBuildInputs = [ pkgs.makeWrapper ];
            propagatedBuildInputs = [ pkgs.python3Packages.pyusb ];
            installPhase = ''
              install -Dm755 dawn_pro_control.py $out/bin/dawn-pro-control
              wrapProgram $out/bin/dawn-pro-control \
                --prefix LD_LIBRARY_PATH : ${pkgs.libusb1}/lib
            '';
          };
        });

      apps = forAllSystems (system: {
        default = {
          type = "app";
          program = "${self.packages.${system}.default}/bin/dawn-pro-control";
        };
      });

      devShells = forAllSystems (system:
        let pkgs = nixpkgs.legacyPackages.${system};
        in {
          default = pkgs.mkShell {
            packages = [
              (pkgs.python3.withPackages (ps: [ ps.pyusb ]))
              pkgs.libusb1
            ];
          };
        });
    };
}
