$ErrorActionPreference = 'Stop'

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
$rootCa = Get-ChildItem Cert:\LocalMachine\Root |
    Where-Object Thumbprint -eq 'EC2C834072AF269510FF0EF203EE3170F6789DCA' |
    Select-Object -First 1
if (-not $rootCa) {
    throw 'The Windows trusted SSL.com TLS RSA Root CA 2022 certificate was not found.'
}

$caFile = Join-Path ([IO.Path]::GetTempPath()) "weconomy-aura-export-ca-$PID.pem"
$oldCaPath = $env:NEO4J_CA_CERT
$bytes = $rootCa.Export([Security.Cryptography.X509Certificates.X509ContentType]::Cert)
$pem = "-----BEGIN CERTIFICATE-----`n$([Convert]::ToBase64String($bytes, 'InsertLineBreaks'))`n-----END CERTIFICATE-----`n"
[IO.File]::WriteAllText($caFile, $pem, [Text.Encoding]::ASCII)
$env:NEO4J_CA_CERT = $caFile

try {
    Push-Location $repoRoot
    try {
        & uv run --no-sync python scripts/build_public_graph_export.py
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
    finally {
        Pop-Location
    }
}
finally {
    if ($null -eq $oldCaPath) { Remove-Item Env:NEO4J_CA_CERT -ErrorAction SilentlyContinue }
    else { $env:NEO4J_CA_CERT = $oldCaPath }
    Remove-Item -LiteralPath $caFile -Force -ErrorAction SilentlyContinue
}
