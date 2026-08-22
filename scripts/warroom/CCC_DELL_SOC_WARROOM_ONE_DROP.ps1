#requires -Version 5.1
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$Branch = 'hotfix/ccc-soc-five-live-evidence-v1'
$Launcher = 'C:\CCC\START_CCC_SOC_LAB_UPGRADED.ps1'
$StatePath = 'C:\CCC\State\ccc-soc-live-state.json'
$Step = 'INIT'

function Fail-WarRoom {
    param([string]$Message)
    Write-Host ''
    Write-Host '============================================================' -ForegroundColor Red
    Write-Host 'CCC DELL WAR ROOM HARD FAIL' -ForegroundColor Red
    Write-Host ("FAILED STEP: {0}" -f $script:Step) -ForegroundColor Red
    Write-Host ("DETAIL: {0}" -f $Message) -ForegroundColor Red
    Write-Host 'NEXT REPAIR TARGET: correct the failed hard gate before rerunning. No later gate is authorized.' -ForegroundColor Yellow
    Write-Host '============================================================' -ForegroundColor Red
    exit 1
}

function Step {
    param([string]$Id, [string]$Text)
    $script:Step = $Id
    Write-Host ''
    Write-Host ("[{0}] {1}" -f $Id, $Text) -ForegroundColor Cyan
}

function Test-IsAdministrator {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($identity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function ConvertTo-SafeValue {
    param($Value)
    $Forbidden = @('password','secret','token','api_key','credential','private_key','shell','command_to_execute','script_body')
    if ($null -eq $Value) { return $null }
    if ($Value -is [System.Collections.IDictionary]) {
        $out = [ordered]@{}
        foreach ($key in $Value.Keys) {
            $name = [string]$key
            if ($Forbidden -contains $name.ToLowerInvariant()) { continue }
            $out[$name] = ConvertTo-SafeValue $Value[$key]
        }
        return [pscustomobject]$out
    }
    if ($Value -is [System.Collections.IEnumerable] -and -not ($Value -is [string])) {
        $items = @()
        foreach ($item in $Value) { $items += ,(ConvertTo-SafeValue $item) }
        return $items
    }
    if ($Value -is [psobject] -and -not ($Value -is [string]) -and -not ($Value.GetType().IsPrimitive)) {
        $out = [ordered]@{}
        foreach ($prop in $Value.PSObject.Properties) {
            if ($Forbidden -contains $prop.Name.ToLowerInvariant()) { continue }
            $out[$prop.Name] = ConvertTo-SafeValue $prop.Value
        }
        return [pscustomobject]$out
    }
    return $Value
}

function Get-FileSha256 {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { return $null }
    return (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant()
}

function Test-EventLogExists {
    param([string]$LogName)
    try { Get-WinEvent -ListLog $LogName -ErrorAction Stop | Out-Null; return $true } catch { return $false }
}

try {
    Step 'PREFLIGHT-01' 'Require Windows PowerShell 5.1 and Administrator'
    if ($PSVersionTable.PSEdition -ne 'Desktop' -or $PSVersionTable.PSVersion.Major -ne 5) {
        Fail-WarRoom 'Run this launcher in Windows PowerShell 5.1, not PowerShell 7.'
    }
    if (-not (Test-IsAdministrator)) { Fail-WarRoom 'Administrator elevation is required.' }

    Step 'PREFLIGHT-02' 'Verify existing CCC SOC launcher'
    if (-not (Test-Path -LiteralPath $Launcher)) { Fail-WarRoom ("Missing launcher: {0}" -f $Launcher) }

    Step 'PREFLIGHT-03' 'Run existing launcher preflight only'
    & $Launcher -PreflightOnly
    if ($LASTEXITCODE -ne 0 -and $null -ne $LASTEXITCODE) { Fail-WarRoom ("Launcher preflight exit code {0}" -f $LASTEXITCODE) }

    Step 'RUNTIME-04' 'Start approved CCC SOC lab only after preflight success'
    & $Launcher
    if ($LASTEXITCODE -ne 0 -and $null -ne $LASTEXITCODE) { Fail-WarRoom ("Launcher runtime exit code {0}" -f $LASTEXITCODE) }

    Step 'STATE-05' 'Validate authoritative Dell live-state JSON contract'
    if (-not (Test-Path -LiteralPath $StatePath)) { Fail-WarRoom ("Missing live state: {0}" -f $StatePath) }
    $State = Get-Content -Raw -LiteralPath $StatePath | ConvertFrom-Json
    $Required = @('timestamp','run_id','phase','status','host_health','vm_health','evidence','next_action')
    $Missing = @()
    foreach ($field in $Required) {
        if (-not ($State.PSObject.Properties.Name -contains $field)) { $Missing += $field }
    }
    if ($Missing.Count -gt 0) { Fail-WarRoom ("State contract missing: {0}" -f ($Missing -join ', ')) }
    $RunId = [string]$State.run_id
    if ([string]::IsNullOrWhiteSpace($RunId)) { Fail-WarRoom 'run_id is empty.' }

    Step 'EVIDENCE-06' 'Create physical evidence workspace'
    $EvidenceRoot = Join-Path 'C:\CCC\Evidence\warroom' $RunId
    New-Item -ItemType Directory -Force -Path $EvidenceRoot | Out-Null
    New-Item -ItemType Directory -Force -Path (Join-Path $EvidenceRoot 'normalized') | Out-Null
    New-Item -ItemType Directory -Force -Path (Join-Path $EvidenceRoot 'report') | Out-Null

    Step 'VM-07' 'Inventory Hyper-V VM state without issuing new power commands'
    $VmHealth = @()
    if (Get-Command Get-VM -ErrorAction SilentlyContinue) {
        $VmHealth = @(Get-VM | Sort-Object Name | ForEach-Object {
            [pscustomobject][ordered]@{
                name = $_.Name
                state = [string]$_.State
                status = [string]$_.Status
                cpu_usage = $_.CPUUsage
                memory_assigned = $_.MemoryAssigned
                uptime_seconds = [math]::Round($_.Uptime.TotalSeconds)
                observed_at = (Get-Date).ToUniversalTime().ToString('o')
            }
        })
    }
    $VmHealth | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $EvidenceRoot 'vm-health.json')

    Step 'SENSOR-08' 'Inventory host-visible sensors and log sources honestly'
    $SensorHealth = @()
    $SensorChecks = @(
        @{ sensor='Windows Security Log'; host='ccc-dell-compute-01'; installed=(Test-EventLogExists 'Security'); running=$true; source='Security'; scenarios=@('DET-02','DET-05') },
        @{ sensor='Windows System Log'; host='ccc-dell-compute-01'; installed=(Test-EventLogExists 'System'); running=$true; source='System'; scenarios=@() },
        @{ sensor='Sysmon'; host='ccc-dell-compute-01'; installed=(Test-EventLogExists 'Microsoft-Windows-Sysmon/Operational'); running=(Test-EventLogExists 'Microsoft-Windows-Sysmon/Operational'); source='Microsoft-Windows-Sysmon/Operational'; scenarios=@('DET-05') },
        @{ sensor='Hyper-V VMMS'; host='ccc-dell-compute-01'; installed=(Test-EventLogExists 'Microsoft-Windows-Hyper-V-VMMS-Admin'); running=(Test-EventLogExists 'Microsoft-Windows-Hyper-V-VMMS-Admin'); source='Microsoft-Windows-Hyper-V-VMMS-Admin'; scenarios=@() },
        @{ sensor='Wazuh'; host='guest-scope'; installed=$false; running=$false; source='GUEST_NOT_QUERIED_BY_HOST_ONE_DROP'; scenarios=@('DET-02','DET-04','DET-05') },
        @{ sensor='Cowrie'; host='CCC-HONEY-TARGET'; installed=$false; running=$false; source='GUEST_NOT_QUERIED_BY_HOST_ONE_DROP'; scenarios=@('DET-03') },
        @{ sensor='Zeek'; host='guest-scope'; installed=$false; running=$false; source='GUEST_NOT_QUERIED_BY_HOST_ONE_DROP'; scenarios=@('DET-01') },
        @{ sensor='Suricata'; host='guest-scope'; installed=$false; running=$false; source='GUEST_NOT_QUERIED_BY_HOST_ONE_DROP'; scenarios=@('DET-01') }
    )
    foreach ($s in $SensorChecks) {
        $SensorHealth += [pscustomobject][ordered]@{
            sensor = $s.sensor
            host = $s.host
            installed = [bool]$s.installed
            running = [bool]$s.running
            source_path_channel = $s.source
            freshness = if ($s.running) { 'OBSERVED_NOW' } else { 'UNKNOWN' }
            scenario_support = $s.scenarios
            state = if ($s.running) { 'AVAILABLE' } elseif ($s.source -eq 'GUEST_NOT_QUERIED_BY_HOST_ONE_DROP') { 'UNKNOWN_GUEST_NOT_QUERIED' } else { 'HOLD' }
        }
    }
    $SensorInventoryPath = Join-Path $EvidenceRoot 'sensor-inventory.json'
    $SensorHealth | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 -LiteralPath $SensorInventoryPath

    Step 'NORMALIZE-09' 'Extract control gates and existing real scenario records without inventing results'
    $ControlGates = @()
    if ($State.evidence -is [System.Collections.IEnumerable]) {
        foreach ($row in $State.evidence) {
            $id = [string]($row.id)
            if ($id -match '^SOC-0[1-5]$') { $ControlGates += ,(ConvertTo-SafeValue $row) }
        }
    }
    $ControlGatesPath = Join-Path $EvidenceRoot 'control-gates.json'
    $ControlGates | ConvertTo-Json -Depth 12 | Set-Content -Encoding UTF8 -LiteralPath $ControlGatesPath

    $ScenarioRunsPath = Join-Path $EvidenceRoot 'scenario-runs.jsonl'
    if (-not (Test-Path -LiteralPath $ScenarioRunsPath)) { New-Item -ItemType File -Path $ScenarioRunsPath | Out-Null }
    $ScenarioRuns = @()
    foreach ($line in @(Get-Content -LiteralPath $ScenarioRunsPath -ErrorAction SilentlyContinue)) {
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        try { $ScenarioRuns += ,($line | ConvertFrom-Json) } catch { Fail-WarRoom 'scenario-runs.jsonl contains invalid JSON.' }
    }

    $Definitions = @('DET-01','DET-02','DET-03','DET-04','DET-05')
    $ScenarioSummary = foreach ($id in $Definitions) {
        $runs = @($ScenarioRuns | Where-Object { $_.scenario_id -eq $id })
        $real = @($runs | Where-Object { $_.synthetic -eq $false -and $_.evidence_refs.Count -gt 0 }).Count
        [pscustomobject][ordered]@{ scenario_id=$id; real_runs=$real; required_runs=3; state=if($real -eq 0){'UNKNOWN'}elseif($real -lt 3){'PARTIAL'}else{'VERIFY_REVIEW_REQUIRED'} }
    }
    $ScenarioSummary | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $EvidenceRoot 'scenario-summary.json')

    Step 'BRIDGE-10' 'Generate strict sanitized one-way bridge payload'
    $EvidenceRefs = @()
    $StateHash = Get-FileSha256 $StatePath
    if ($StateHash) { $EvidenceRefs += ("sha256:{0}:ccc-soc-live-state.json" -f $StateHash) }
    $SensorHash = Get-FileSha256 $SensorInventoryPath
    if ($SensorHash) { $EvidenceRefs += ("sha256:{0}:sensor-inventory.json" -f $SensorHash) }

    $Payload = [pscustomobject][ordered]@{
        schema = 'ccc.soc.evidence.bridge.v1'
        timestamp = (Get-Date).ToUniversalTime().ToString('o')
        source_host = 'ccc-dell-compute-01'
        run_id = $RunId
        control_gates = @($ControlGates)
        scenario_runs = @($ScenarioRuns | ForEach-Object { ConvertTo-SafeValue $_ })
        vm_health = @($VmHealth)
        sensor_health = @($SensorHealth)
        evidence_refs = @($EvidenceRefs)
        next_action = 'RUN_AUTHORIZED_GUEST_DETECTION_SCENARIOS_AND_RECONCILE_EVIDENCE'
    }
    $PayloadPath = Join-Path $EvidenceRoot 'ccc-soc-bridge-payload.json'
    $PayloadJson = $Payload | ConvertTo-Json -Depth 20 -Compress
    [IO.File]::WriteAllText($PayloadPath, $PayloadJson + [Environment]::NewLine, (New-Object Text.UTF8Encoding($false)))

    Step 'HASH-11' 'Hash evidence package'
    $HashLines = @()
    Get-ChildItem -File -LiteralPath $EvidenceRoot | Where-Object { $_.Name -ne 'sha256sums.txt' } | Sort-Object Name | ForEach-Object {
        $HashLines += ("{0}  {1}" -f (Get-FileSha256 $_.FullName), $_.Name)
    }
    $HashLines | Set-Content -Encoding ASCII -LiteralPath (Join-Path $EvidenceRoot 'sha256sums.txt')
    [pscustomobject][ordered]@{ run_id=$RunId; source=$StatePath; state_sha256=$StateHash; files=$HashLines } | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $EvidenceRoot 'evidence-index.json')

    Step 'TRANSPORT-12' 'Send signed sanitized evidence if HP session variables are supplied, else preserve file fallback'
    $BridgeMode = 'FILE_FALLBACK'
    $BridgeAddress = [Environment]::GetEnvironmentVariable('CCC_HP_BRIDGE_ADDRESS')
    $BridgeToken = [Environment]::GetEnvironmentVariable('CCC_HP_BRIDGE_TOKEN')
    if (-not [string]::IsNullOrWhiteSpace($BridgeAddress) -and -not [string]::IsNullOrWhiteSpace($BridgeToken)) {
        try {
            $Bytes = [Text.Encoding]::UTF8.GetBytes($PayloadJson)
            $Hmac = New-Object Security.Cryptography.HMACSHA256
            $Hmac.Key = [Text.Encoding]::UTF8.GetBytes($BridgeToken)
            $Signature = ([BitConverter]::ToString($Hmac.ComputeHash($Bytes))).Replace('-','').ToLowerInvariant()
            $Headers = @{ Authorization=("Bearer {0}" -f $BridgeToken); 'X-CCC-Signature'=("sha256={0}" -f $Signature) }
            $Response = Invoke-RestMethod -Method Post -Uri $BridgeAddress -Headers $Headers -ContentType 'application/json' -Body $PayloadJson -TimeoutSec 10
            if ($Response.status -eq 'ACCEPTED') { $BridgeMode = 'HTTP_LAN' }
        } catch {
            Write-Warning ("HTTP bridge unavailable; retaining sanitized file fallback. {0}" -f $_.Exception.Message)
            $BridgeMode = 'FILE_FALLBACK'
        }
    }

    Step 'REPORT-13' 'Print exact next physical scenario action'
    Write-Host ''
    Write-Host '============================================================' -ForegroundColor Green
    Write-Host 'CCC DELL SOC WAR ROOM PHYSICAL PRODUCER COMPLETE' -ForegroundColor Green
    Write-Host '============================================================'
    Write-Host ("Run ID        : {0}" -f $RunId)
    Write-Host ("State source  : {0}" -f $StatePath)
    Write-Host ("Evidence dir  : {0}" -f $EvidenceRoot)
    Write-Host ("Bridge mode   : {0}" -f $BridgeMode)
    Write-Host ("VM count      : {0}" -f $VmHealth.Count)
    Write-Host ("Sensor records: {0}" -f $SensorHealth.Count)
    Write-Host ("Control gates : {0} evidence records bound" -f $ControlGates.Count)
    Write-Host ("Scenario runs : {0} real/recorded rows currently present" -f $ScenarioRuns.Count)
    if ($BridgeMode -eq 'FILE_FALLBACK') {
        Write-Host ("HP next       : transfer ONLY this sanitized file to HP runtime/soc/: {0}" -f $PayloadPath) -ForegroundColor Yellow
    } else {
        Write-Host 'HP next       : verify the dashboard Bridge State/current run updated from this signed payload.' -ForegroundColor Yellow
    }
    Write-Host 'Scenario next : execute DET-01..DET-05 helpers manually inside their registered guests, one bounded scenario at a time.' -ForegroundColor Yellow
    Write-Host '============================================================'
    exit 0
}
catch {
    Fail-WarRoom $_.Exception.Message
}
