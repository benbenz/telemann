let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-23.11";
  pkgs = import nixpkgs { config = {}; overlays = []; };
in

pkgs.mkShell {
  buildInputs = [
    pkgs.git
    pkgs.gcc
    pkgs.cmake
    pkgs.python311
    pkgs.openssl
    pkgs.libjpeg
    pkgs.zlib
  ];
}
