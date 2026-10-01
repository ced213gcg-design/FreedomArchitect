#!/usr/bin/env python3
import json, os, pathlib, socket, subprocess, sys

HOME=pathlib.Path.home()
SOCK=HOME/".local/state/lilced/lilced.sock"
APP=HOME/"LilCed/app"
OUT=HOME/"LIL_CED_CABINET/10_TESTS_AND_REGRESSIONS/provider_all_acceptance_latest.json"

def req(text):
    with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as s:
        s.settimeout(5); s.connect(str(SOCK)); s.sendall((text+"\n").encode())
        data=b""
        while True:
            b=s.recv(65536)
            if not b: break
            data+=b
        return data.decode(errors="replace").strip()

status=json.loads(req("/status"))
providers=json.loads(req("/providers"))
expected=["anthropic","openai","google","xai","compatible","ollama"]
tests={}
tests["service_active"]=subprocess.run(["systemctl","--user","is-active","lilced-core.service"],capture_output=True,text=True).stdout.strip()=="active"
tests["version"]=status.get("version")=="0.9-provider-all"
tests["provider_mode_all"]=status.get("provider_mode")=="all"
tests["provider_set_exact"]=list(providers)==expected
tests["all_unconfigured_without_secrets"]=all(v.get("state")=="UNCONFIGURED" for v in providers.values())
tests["safe_no_model"]=req("provider-all no-key acceptance probe").startswith("SAFE_NO_MODEL:")
tests["brain_integrity"]=status.get("brain_integrity")=="PASS"
tests["socket_0600"]=oct(SOCK.stat().st_mode & 0o777)=="0o600"
tests["secret_0600"]=oct((HOME/".config/lilced/secrets.env").stat().st_mode & 0o777)=="0o600"
tests["secret_empty"]=(HOME/".config/lilced/secrets.env").stat().st_size==0
tests["one_call_rule"]=json.loads((APP/"config.json").read_text()).get("max_inflight_model_calls")==1

sys.path.insert(0,str(APP))
import lilced_providers as lp
original=dict(os.environ)
try:
    os.environ["ANTHROPIC_API_KEY"]="test"; os.environ["OPENAI_API_KEY"]="test"
    os.environ["GEMINI_API_KEY"]="test"; os.environ["XAI_API_KEY"]="test"
    os.environ["COMPAT_API_KEY"]="test"; os.environ["COMPAT_MODEL"]="test-model"
    os.environ["COMPAT_BASE_URL"]="https://example.invalid/v1"; os.environ["OLLAMA_MODEL"]="test-local"
    detected=lp.statuses()
    tests["configuration_detection"]=all(v.get("state")=="CONFIGURED" for v in detected.values())
finally:
    os.environ.clear(); os.environ.update(original)

for name in expected+["all"]:
    out=req("/provider "+name)
    tests["select_"+name]=("PROVIDER_MODE="+name in out) if name!="all" else ("PROVIDER_MODE=all" in out)
req("/provider all")

result={
 "schema":"lilced.provider_all.acceptance.v1",
 "version":"0.9-provider-all",
 "tests":tests,
 "provider_status":json.loads(req("/providers")),
 "final_provider_mode":json.loads(req("/status")).get("provider_mode"),
 "state":"PASS" if all(tests.values()) else "HOLD"
}
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(result,indent=2)+"\n")
mirror=HOME/"CCC_FILING_CABINET/14_LIL_CED/10_TESTS_AND_REGRESSIONS/provider_all_acceptance_latest.json"
mirror.parent.mkdir(parents=True,exist_ok=True)
mirror.write_text(OUT.read_text())
print(json.dumps(result,indent=2))
sys.exit(0 if result["state"]=="PASS" else 2)