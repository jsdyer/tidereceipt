export default {
  "kind": "tide",
  "unit": "m",
  "accent": "#126a7c",
  "tint": "#e0f1f3",
  "staleHours": 10,
  "text": {
    "eyebrow": "COASTAL OBSERVATIONS / CANADA",
    "intro": "What did the tide table predict—and where did the water actually rise? Follow saved hourly predictions at Vancouver and Halifax.",
    "entity-label": "Tide gauge",
    "bias-help": "Positive = prediction above the gauge",
    "cadence": "Collected every six hours. Each receipt saves the next 72 hourly tide predictions; later runs retrieve gauge readings.",
    "observed-heading": "Gauge reading (m)",
    "target-heading": "Target hour (UTC)",
    "difference-heading": "Prediction − gauge",
    "obs-legend": "Gauge reading"
  },
  "method": [
    "Each receipt freezes future hourly astronomical tide predictions before their target time. Later gauge observations are matched at exactly the same UTC hour and station, in metres relative to chart datum.",
    "The difference includes non-tidal effects such as weather and water pressure. It is a tidal residual, not a score for a storm-surge forecast. Positive signed difference means the prediction was higher than the gauge.",
    "Only gauge observations with CHS quality flag 1 are scored. Suspect, unknown and missing observations stay unmatched. Later observation revisions are retained in separate receipts; the dashboard uses the latest collected reading.",
    "Every source receipt is retained in the repository and downloadable. The dashboard shows the most recent 14 days of collections. This independent research view is not for navigation."
  ],
  "sources": [
    {
      "label": "CHS water-level API and documentation",
      "url": "https://tides.gc.ca/en/web-services-offered-canadian-hydrographic-service"
    },
    {
      "label": "Vancouver station 07735",
      "url": "https://tides.gc.ca/en/stations/07735"
    },
    {
      "label": "Halifax station 00490",
      "url": "https://tides.gc.ca/en/stations/00490"
    },
    {
      "label": "CHS licence and attribution",
      "url": "https://tides.gc.ca/en/licence-agreement"
    }
  ],
  "chartCaption": "The line is the saved tide prediction. Dots appear only when a quality-checked gauge reading matches that hour.",
  "tableNote": "No interpolation or substitution of a nearby gauge is used.",
  "id": "tidereceipt"
};
