from pathlib import Path
import importlib.util,json,os

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('export_infinity',ROOT/'scripts'/'export_infinity_evidence.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)


def test_pr_event_preserves_source_branch_and_head_sha(monkeypatch,tmp_path):
    event={
      'pull_request':{
        'head':{'ref':'upgrade/ccc-infinity-composition-v1','sha':'source-head-sha'},
        'base':{'ref':'hotfix/ccc-soc-five-live-evidence-v1','sha':'base-sha'}
      }
    }
    path=tmp_path/'event.json'; path.write_text(json.dumps(event),encoding='utf-8')
    monkeypatch.setenv('GITHUB_EVENT_PATH',str(path))
    monkeypatch.setenv('GITHUB_HEAD_REF','upgrade/ccc-infinity-composition-v1')
    monkeypatch.setenv('GITHUB_SHA','temporary-merge-sha')
    branch,source_sha,validation_sha=mod.github_source_identity()
    assert branch=='upgrade/ccc-infinity-composition-v1'
    assert source_sha=='source-head-sha'
    assert validation_sha not in ('', 'UNKNOWN')
    assert source_sha!='temporary-merge-sha'
