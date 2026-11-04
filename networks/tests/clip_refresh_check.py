"""Renaming a phase must not leave an old video in its clips folder."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from types import SimpleNamespace
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from build import export_clips

with TemporaryDirectory() as tmp:
    folder=Path(tmp); clips=folder/'clips';clips.mkdir()
    old=clips/'01-old-heading.mp4';old.write_bytes(b'old')
    unrelated=clips/'my-recording.mp4';unrelated.write_bytes(b'keep')
    deck={'frames':60,'sections':[{'frame':0,'name':'Start with one message'}]}
    def encode(command,**kwargs):
        Path(command[-1]).write_bytes(b'new')
        return SimpleNamespace(returncode=0)
    with patch('build.subprocess.run',side_effect=encode):export_clips(folder,deck)
    assert not old.exists()
    assert (clips/'01-start-with-one-message.mp4').read_bytes()==b'new'
    assert unrelated.read_bytes()==b'keep'
    # A failed export must preserve the previous set for recovery.
    old.write_bytes(b'old')
    with patch('build.subprocess.run',return_value=SimpleNamespace(returncode=1,stderr='failure')):
        try:export_clips(folder,deck)
        except RuntimeError:pass
        else:raise AssertionError('Expected encoder failure')
    assert old.exists()
print('PASS: renamed generated clips are refreshed; failed exports preserve previous files.')
