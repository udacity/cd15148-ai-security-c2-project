$ImageName = "offensive-ai-course"
$OutputFile = "06_trivy_report.json"

Write-Host "Building Docker image..."
docker build -t $ImageName .

Write-Host "Running Trivy scan..."
trivy image --format json --output $OutputFile $ImageName

Write-Host "Copying artifacts to starter\docs..."
New-Item -ItemType Directory -Force -Path .\starter\docs | Out-Null
Copy-Item .\Dockerfile .\starter\docs\Dockerfile -Force
Copy-Item .\$OutputFile .\starter\docs\$OutputFile -Force

Write-Host "Done."