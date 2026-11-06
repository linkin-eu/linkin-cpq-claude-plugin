---
# No weight per metre: no band applies, so the die's figures are missing too (golden 207's shape).
# Only the powder coating could be priced.
expect:
  customerReference: string
  items: array
---

{"modelVersion":"1.1.0","contractVersion":"1.2.0","header":{"soldToParty":"0001999999","salesArea":{"salesOrganization":"1102","salesOrganizationText":"LINKIN Bulgaria","distributionChannel":"10"},"division":"20","currency":"EUR","pricingDate":"2026-11-06","timeZone":"Europe/Sofia","incoterms":{"classification":"EXW","location":"Plovdiv, Bulgaria"},"customerReference":"RFQ EVAL-7"},"status":"incomplete","issuableAs":[],"inputHash":"h1:2eaee9b4ca565eea4682e5db0e73d4e924b4a72fe2af70f89d76033a2f3fa8c5","priceHash":"p1:7e855222b0f6ada519d59503e89d57c6aa1850f94319a69a18ff6cdbb99a1b45","totals":{"netValue":808.32,"lines":{"total":1,"ok":0,"incomplete":1,"inconsistent":0,"refused":0,"rounded":0,"belowMinimum":0}},"groups":[],"messages":[],"items":[{"item":"10","customerMaterial":"Frame EV-210","material":"9876543210","status":"incomplete","quantity":{"entered":400,"order":400,"unit":"H87"},"packs":[],"bars":{"count":400,"piecesPerBar":1,"length":6000},"stockBars":[],"netValue":808.32,"uplift":0,"groups":[],"missing":["ZA_KG_PER_M_EST","ZA_DIE_CAVITIES_EST","ZA_EXTR_M_MIN_EST","ZA_DIE_LIFE_M_EST","ZA_AGE_FACE_MM2_EST"],"messages":[],"values":{"ZA_DIE_EST":"EV-210","ZA_ALLOY":"6060","ZA_TEMPER":"T5","ZA_LENGTH_MM":"6000","ZA_PROF_PERI_MM_EST":"240","ZA_SURFACE_FINISH":"POWDER_COATED","ZA_POWDER_TYPE":"RAL","ZA_POWDER_NUMBER":"9016","ZA_POWDER_FINISH":"SMOOTH_GLOSS","ZA_POWDER_CLASS":"CL1","ZA_PRE_ANODIZED":"-","ZA_PROT_WIDTH_EST":"0","ZA_PROT_WIDTH_EST_2":"0","ZA_PROT_WIDTH_EST_3":"0","ZA_PROT_WIDTH_EST_4":"0"}}]}
