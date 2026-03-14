$json = Get-Content "D:\c2\fastapi\divers\yt_videos\cache\.tseries_videos_scrap_some.json" -Raw | ConvertFrom-Json
$videos = $json.videos
$total = $videos.Count
$ids = $videos | Where-Object { $_.id } | Select-Object -ExpandProperty id
$uniqueIds = $ids | Sort-Object -Unique
$dupCount = $total - $uniqueIds.Count

Write-Host "Nombre total d'enregistrements : $total"
Write-Host "IDs uniques                    : $($uniqueIds.Count)"
Write-Host "Doublons (entrées en trop)     : $dupCount"

if ($dupCount -gt 0) {
    $grouped = $ids | Group-Object | Where-Object { $_.Count -gt 1 }
    Write-Host "`nIDs en doublon ($($grouped.Count) IDs distincts concernés) :"
    $grouped | Select-Object -First 20 | ForEach-Object { Write-Host "  id=$($_.Name)  x$($_.Count)" }
}
else {
    Write-Host "`nAucun doublon détecté."
}

