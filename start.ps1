param(
  [ValidateSet("run", "0", "1", "help", "--help")]
  [string]$mode = "run",

  [Alias("h", "help")]
  [switch]$HelpSwitch
)

# --- Configuration globale ---
$VenvPath = ".venv/Scripts/python.exe"
$ActivateScript = ".\.venv\Scripts\Activate.ps1"
$MinPSVersion = [Version]"7.5.4"

# Encodage UTF‑8 complet
[System.Console]::InputEncoding = [System.Text.Encoding]::UTF8
[System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# --- Fonctions utilitaires ---
function Show-PauseMessage {
  param([string]$Message)
  Write-Host ""
  Write-Host $Message
  Write-Host ""
  Write-Host "Appuyer sur une touche pour continuer..."
  Write-Host ""
  [void][System.Console]::ReadKey($true)
}

function Check-PowerShellVersion {
  param([Version]$RequiredVersion)
  if ($PSVersionTable.PSVersion -lt $RequiredVersion) {
    Show-PauseMessage "*** ATTENTION: INSTALLER PowerShell >= $RequiredVersion pour profiter pleinement des messages (Voir README.md, Tips/2) ***"
    return $false
  }
  return $true
}

function Show-Help {
  Write-Host "Utilisation : ./start [mode]"
  Write-Host "  Sans argument  -> (.venv) flet run main.py"
  Write-Host "  0              -> Reset total (VEnv + dépendances)"
  Write-Host "  1              -> Ré-installe uniquement PyMoX_Kit"
  Write-Host "Options : -h, --help, help"
}

function Show-VenvMissingError {
  param([string]$ExtraMessage = "")
  Write-Host '[ERREUR] Aucun .venv détecté. Lancer " ./start 0 " pour initialiser l''environnement.'
  if ($ExtraMessage) { Write-Host $ExtraMessage }
  exit 1
}

function Deactivate-ExistingVenv {
  if (Get-Command deactivate -ErrorAction SilentlyContinue) {
    Write-Host "Je sors si besoin, du venv actuel, le vide et le supprime..."
    deactivate
    Write-Host "1 - Sorti → Root."
  }
}

function Remove-Venv {
  param(
    [int]$MaxAttempts = 5,
    [int]$DelaySeconds = 1
  )

  if (-not (Test-Path ".venv")) {
    Write-Host "Aucun .venv trouvé, rien à supprimer."
    return
  }

  Write-Host "2 - Suppression du VE (Virtual Environment)..."

  # Fermer processus Python/Flet/Pip susceptibles de verrouiller des fichiers
  $procs = Get-Process -Name python, flet, pip -ErrorAction SilentlyContinue
  if ($procs) {
    Write-Host "Arrêt des processus Python/Flet/Pip en cours..."
    $procs | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
  }

  # Retirer attributs lecture-seule pour éviter les blocages
  try {
    Get-ChildItem -Path ".venv" -Recurse -Force -ErrorAction SilentlyContinue |
    ForEach-Object { $_.Attributes = 'Normal' }
  }
  catch {
    # non bloquant
  }

  $attempt = 0
  while ($attempt -lt $MaxAttempts) {
    $attempt++
    try {
      Remove-Item ".venv" -Recurse -Force -ErrorAction Stop
      Write-Host "Suppression du VE terminée."
      return
    }
    catch {
      Write-Host "Tentative $attempt/$MaxAttempts : échec de Remove-Item. Message: $($_.Exception.Message)"
      Start-Sleep -Seconds $DelaySeconds
    }
  }

  # Dernier recours : utiliser rmdir via cmd (parfois plus efficace sur Windows)
  Write-Host "Tentative finale avec rmdir (cmd)..."
  try {
    cmd /c "rmdir /s /q .venv"
    if (-not (Test-Path ".venv")) {
      Write-Host "Suppression du VE terminée (rmdir)."
      return
    }
    else {
      Write-Host "[ERREUR] Impossible de supprimer .venv même après rmdir."
    }
  }
  catch {
    Write-Host "[ERREUR] rmdir a échoué : $($_.Exception.Message)"
  }

  Write-Host "Si le problème persiste : fermez les applications utilisant Python, désactivez l'antivirus temporairement, ou redémarrez la machine."
}


function Ensure-Venv {
  Write-Host "Création de l'environnement virtuel ← racine..."
  # py -3.11 -m venv .venv
  # py -3.12 -m venv .venv
  # py -3.13 -m venv .venv
  py -m venv .venv
  if (-not (Test-Path $VenvPath)) {
    Write-Host "[ERREUR] Échec de création de l'environnement virtuel."
    exit 1
  }
}

function Activate-Venv {
  if (-not (Test-Path $ActivateScript)) {
    Show-VenvMissingError
  }
  . $ActivateScript
  Write-Host "VEnv activé."
  
  # Le fichier ./v/Lib/site-packages/sitecustomize.py
  # est chargé automatiquement par Python au démarrage
  # Il configure le sys.path pour tous les scripts, même lancés via Flet


  # --- Copie automatique de sitecustomize.py ( Juste for fastapi/ ) ---
  # $Source = "tools\sitecustomize.py"
  # $Target = ".venv\Lib\site-packages\sitecustomize.py"

  # if (Test-Path $Source) {
  #   Copy-Item $Source $Target -Force
  #   Write-Host "sitecustomize.py copié dans le venv."
  # }
  # else {
  #   Write-Host "[AVERTISSEMENT] tools\sitecustomize.py introuvable."
  # }

}

function Upgrade-Pip {
  Write-Host "Mise à jour de pip..."
  python -m pip install --upgrade pip
  if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERREUR] ❌ Échec de la mise à jour de pip"
    exit 1
  }
}

function Install-Requirements {
  Write-Host "Installation des dépendances..."

  if (Test-Path "requirements.txt") {
    Write-Host "requirements.txt détecté, installation via ce fichier..."
    pip install -r requirements.txt
  }
  else {
    Write-Host "requirements.txt absent, installation de pymox_kit.uniquement..."
    pip install pymox_kit
  }

  if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERREUR] ❌ Installation échouée"
    exit 1
  }

  Write-Host "[OK] ✅ Dépendances installées"
}

function Run-PymoxKitFresh {
  Write-Host "Réinstallation de pymox_kit..."
  pip uninstall pymox_kit -y | Out-Null
  pip install pymox_kit
  if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERREUR] ❌ Réinstallation de pymox_kit échouée"
    exit 1
  }
}

function Start-App {
  Write-Host "========================================"
  Write-Host "  Lancement de ./main.py"
  Write-Host "========================================"
  Write-Host ""
  Write-Host "Démarrage automatique du script ./main.py... 🚀"
  Write-Host ""
  # Flet CLI supports --ignore-dirs (no --ignore-files in this version).
  # Prevent writing .pyc files during run to mimic "**/*.pyc" ignore behavior.
  $env:PYTHONDONTWRITEBYTECODE = "1"
  flet run -d -r --ignore-dirs ".git,.venv,__pycache__" main.py
}

# --- Aide ---
if ($HelpSwitch -or $mode -in @("help", "--help")) {
  Show-Help
  exit 0
}

# --- Modes ---
switch ($mode) {
  "0" {
    Write-Host "----------------------------------------"
    Write-Host "Reset..."
    Write-Host "----------------------------------------"
    Write-Host ""
    Write-Host "Suppression des fichiers et dossiers..."
    Write-Host ""

    Deactivate-ExistingVenv

    if (Test-Path ".pytest_cache") {
      Remove-Item ".pytest_cache" -Recurse -Force
      Write-Host "Suppression de .pytest_cache terminée."
    }

    Remove-Venv

    Write-Host "Réinitialisation terminée (Configuration réinitialisée et environnement supprimé)."
    Write-Host ""

    Write-Host "----------------------------------------"
    Write-Host "(Re)-Installation des dependances..."
    Write-Host "----------------------------------------"

    Ensure-Venv
    Activate-Venv
    Upgrade-Pip
    Install-Requirements

    Write-Host ""
    Write-Host "========================================"
    Write-Host "  (Re)-Installation terminée !"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "Prochaines étapes:"
    Write-Host "  1. Copier/coller .env_example en .env le cas échéant"
    Write-Host "  2. Lire README.md pour les instructions détaillées"
    Write-Host ""

    Start-App
  }

  "1" {
    Write-Host "Mode 1 : réinstallation rapide de PyMoX_Kit"
    if (-not (Test-Path $VenvPath)) {
      Show-VenvMissingError
    }
    Activate-Venv
    Run-PymoxKitFresh
    Start-App
  }

  default {
    if (-not (Test-Path $VenvPath)) {
      # Afficher rappel de version si nécessaire, puis message d'erreur centralisé
      Check-PowerShellVersion -RequiredVersion $MinPSVersion | Out-Null
      Show-VenvMissingError
    }

    # Affichage informatif de la version PowerShell (non bloquant)
    Write-Host "----------------------------------------"
    Write-Host "PowerShell utilisé : $($PSVersionTable.PSEdition) - Version $($PSVersionTable.PSVersion)"
    Write-Host "----------------------------------------"

    # Avertissement non bloquant si version inférieure
    Check-PowerShellVersion -RequiredVersion $MinPSVersion | Out-Null

    Activate-Venv
    Start-App
  }
}
