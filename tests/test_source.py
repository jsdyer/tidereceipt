import json,sys,unittest
from pathlib import Path
from datetime import datetime,timezone
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from collect import parse
class TideTests(unittest.TestCase):
    def test_observation_qc_is_retained_not_silently_upgraded(self):
        raw=json.dumps([{'eventDate':'2026-11-21T00:00:00Z','value':2.8,'qcFlagCode':'3'}]).encode()
        result=parse(raw,'observation',datetime(2026,11,22,tzinfo=timezone.utc));self.assertEqual(result[0]['quality'],'3')
    def test_nonhourly_and_future_observations_are_not_matched(self):
        raw=json.dumps([{'eventDate':'2026-11-21T00:30:00Z','value':2.8},{'eventDate':'2026-11-23T00:00:00Z','value':2.8}]).encode()
        self.assertEqual(parse(raw,'observation',datetime(2026,11,22,tzinfo=timezone.utc)),[])
    def test_bad_forecast_window_fails_instead_of_replacing_archive(self):
        raw=json.dumps([{'eventDate':'2026-11-23T00:00:00Z','value':2.8}]).encode()
        with self.assertRaises(ValueError):parse(raw,'forecast',datetime(2026,11,22,tzinfo=timezone.utc))
