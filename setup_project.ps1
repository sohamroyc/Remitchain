$sourcePath = "d:\Project\Remitchain\stitch\stitch"
$destPath = "d:\Project\Remitchain\public"

if (!(Test-Path $destPath)) {
    New-Item -ItemType Directory -Force -Path $destPath
}

$folders = Get-ChildItem -Directory -Path $sourcePath | Where-Object { $_.Name -ne "remitchain_global" }

foreach ($folder in $folders) {
    if (Test-Path "$($folder.FullName)\code.html") {
        Copy-Item "$($folder.FullName)\code.html" -Destination "$destPath\$($folder.Name).html"
    }
}

# Create a simple index file to navigate between them
$indexContent = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RemitChain Screens</title>
    <style>
        body { font-family: sans-serif; padding: 2rem; background: #f9f9ff; color: #141c2b; }
        h1 { font-family: 'Inter', sans-serif; color: #1a56db; }
        .screencards { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); }
        .card { padding: 1rem; background: white; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-decoration: none; color: inherit; }
        .card:hover { box-shadow: 0 8px 12px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <h1>RemitChain Screens</h1>
    <div class="screencards">
"@

foreach ($folder in $folders) {
    if (Test-Path "$($folder.FullName)\code.html") {
        $displayName = ($folder.Name -replace '_', ' ').ToUpper()
        $indexContent += "        <a class=`"card`" href=`"$($folder.Name).html`">$displayName</a>`n"
    }
}

$indexContent += @"
    </div>
</body>
</html>
"@

Set-Content -Path "$destPath\index.html" -Value $indexContent
