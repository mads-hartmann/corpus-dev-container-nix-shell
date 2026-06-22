let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/archive/06278c77b5d162e62df170fec307e83f1812d94b.tar.gz";
  pkgs = import nixpkgs { config = {}; overlays = []; };
in

pkgs.mkShellNoCC {
  packages = with pkgs; [
    curl
    gnumake
    python3
  ];

  CORPUS_SERVICE_PORT = "8000";

  shellHook = ''
    echo "nix-shell ready: run make check or make serve"
  '';
}
