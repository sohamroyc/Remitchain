$screens = @(
    @{ name="Receive_Money.html"; url="https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sX2FiMGEzYjkxNmEzNDQ1MzliMWM1YjFhY2Q4NThhNmFlEgsSBxD46I-8whEYAZIBIwoKcHJvamVjdF9pZBIVQhM1NTg5Nzg1MzM3OTIwMzUxMTEz&filename=&opi=89354086" },
    @{ name="Settings.html"; url="https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sX2JhZDM2MDdkMzM0YzQ1OTk5YjMwODdmZGQzOGRmMjcyEgsSBxD46I-8whEYAZIBIwoKcHJvamVjdF9pZBIVQhM1NTg5Nzg1MzM3OTIwMzUxMTEz&filename=&opi=89354086" },
    @{ name="Send_Money.html"; url="https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sX2VkNWM3MGNhZjI5YTQ4OWJhZWNmNGVjZTUwYjZhMzIzEgsSBxD46I-8whEYAZIBIwoKcHJvamVjdF9pZBIVQhM1NTg5Nzg1MzM3OTIwMzUxMTEz&filename=&opi=89354086" },
    @{ name="Transaction_History.html"; url="https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sX2FiZDVmYjY0MjRiNTQ2NTA5NTRjOGU5YmYyNmY1NWFiEgsSBxD46I-8whEYAZIBIwoKcHJvamVjdF9pZBIVQhM1NTg5Nzg1MzM3OTIwMzUxMTEz&filename=&opi=89354086" },
    @{ name="Beneficiaries_Management.html"; url="https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sX2Y3MzkwZDFmZDQ2ZTRjNmZhY2U2YTQyMTg4N2IyY2E2EgsSBxD46I-8whEYAZIBIwoKcHJvamVjdF9pZBIVQhM1NTg5Nzg1MzM3OTIwMzUxMTEz&filename=&opi=89354086" },
    @{ name="Main_Dashboard.html"; url="https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sXzNjYzk3OTdkNGMwNjQ1YWRhMmQ4Mjc0ZDdlNjUzY2M5EgsSBxD46I-8whEYAZIBIwoKcHJvamVjdF9pZBIVQhM1NTg5Nzg1MzM3OTIwMzUxMTEz&filename=&opi=89354086" },
    @{ name="Authentication.html"; url="https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sXzZlYWVlOTVlM2Y5MTRlMDc5Nzc1MWQzOWEzOTMwNjQ5EgsSBxD46I-8whEYAZIBIwoKcHJvamVjdF9pZBIVQhM1NTg5Nzg1MzM3OTIwMzUxMTEz&filename=&opi=89354086" },
    @{ name="Scheduled_Transfers.html"; url="https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sXzcxMDdkNTAyZTUxMTQwMTE5Zjc1OTVmZjJhODgyODZmEgsSBxD46I-8whEYAZIBIwoKcHJvamVjdF9pZBIVQhM1NTg5Nzg1MzM3OTIwMzUxMTEz&filename=&opi=89354086" }
)

foreach ($screen in $screens) {
    Invoke-WebRequest -Uri $screen.url -OutFile $screen.name
    Write-Host "Downloaded $($screen.name)"
}
