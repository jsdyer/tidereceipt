#!/usr/bin/env python3
"""Capture future CHS predictions and quality-labelled observations at Canadian tide gauges."""
import json,math,time
from datetime import timedelta
from urllib.parse import urlencode
from common import ROOT,download,now,iso,date,record,save,status
BASE='https://api-iwls.dfo-mpo.gc.ca/api/v1/stations/'
from stations import STATIONS

def parse(raw,kind,captured):
    source=json.loads(raw)
    if not isinstance(source,list): raise ValueError('CHS response is not an array')
    points={}
    for item in source:
        when=date(item['eventDate']);value=item.get('value')
        if not isinstance(value,(int,float)) or not math.isfinite(value) or not -10<=value<=25: raise ValueError('Invalid water level')
        if when.minute or when.second: continue
        if kind=='forecast' and when<=captured: continue
        if kind=='observation' and when>captured: continue
        points[iso(when)]={'target':iso(when),'value':value,'quality':str(item.get('qcFlagCode','')),'reviewed':bool(item.get('reviewed',False))}
    result=[points[t] for t in sorted(points)]
    if not result and kind=='forecast': raise ValueError('CHS returned no usable hourly values')
    if kind=='forecast' and len(result)<48: raise ValueError('Incomplete future prediction window')
    return result

def main():
    records=[];states=[]
    for station in STATIONS:
        stamp=now();start=stamp.replace(minute=0,second=0)
        observation_count=0
        for kind,series,begin,end in [('forecast','wlp',start,start+timedelta(days=3)),('observation','wlo',start-timedelta(days=14),start)]:
            url=BASE+station.api_id+'/data?'+urlencode({'time-series-code':series,'from':iso(begin),'to':iso(end),'resolution':'SIXTY_MINUTES'})
            raw=download(url);captured=now();points=parse(raw,kind,captured)
            if kind=='observation': observation_count=len(points)
            if points: records.append(record(kind,station.code,station.name,url,raw,points,captured_at=iso(captured),provenance='prospective' if kind=='forecast' else 'observed',measurement='water-level',units='m',datum='chart datum',series=series))
            time.sleep(.5)
        states.append({'name':station.name,'status':'collected' if observation_count else 'predictions saved; gauge readings unavailable'})
    for receipt in records:save(receipt)
    status(states)
    print(f'Saved {len(records)} CHS receipts; future predictions are kept separate from observations.')
if __name__=='__main__':main()
