# CMHC 2024 Census hardship document recovery

## Bibliographic identity

- Title: *New insights on affordability: update on housing hardship from the 2021 Census*
- Series: CMHC Research Insight
- Catalogue: `NH18-33/85-2024E-PDF`
- French edition: `NH18-33/85-2024F-PDF` (*Nouveau regard sur l’abordabilité*)
- Internal production marks: `70484 20240527-002A` (EN); `70485 20240527-002A.2` (FR)
- Imprint: Ottawa, CMHC/SCHL, [2024], ©2023 (English record)
- Extent: 6 pages + A1
- Catalogue record: https://publications.gc.ca/site/eng/9.949944/publication.html

Page [1] of the catalogue abstract states that STIR > 30% does not directly test whether housing costs leave enough income for other necessities. That is a conceptual statement, not a 2021 national hardship rate.

## Documented withdrawal

The Government of Canada Publications record states:

> The publication in PDF format was removed on 25 November 2025 at the request of Canada Mortgage and Housing Corporation.

The former collection URL

`https://publications.gc.ca/collections/collection_2024/schl-cmhc/NH18-33-85-2024-eng.pdf`

now redirects to an archived-removal page (`archivee-archived.html`). The HTTP payload is HTML, not a PDF.

## Retrieval attempts (17 October 2026)

| Source | Result |
| --- | --- |
| publications.gc.ca English and French catalogue records | Record exists; PDF withdrawn |
| publications.gc.ca collections URL | 307 → archived-removal HTML |
| CMHC assets host (guessed research-report path) | HTTP 404 `BlobNotFound` |
| Internet Archive CDX for the collections PDF | empty result `[]` |
| Library and Archives Canada weekly-acquisitions path | HTTP 404 |
| Ottawa Public Library / BiblioCommons record | Catalogue metadata only; eBook not retrieved here |
| Community Housing Transformation Centre summary page | Qualitative description only; no national rate |
| Indexed research citations | No independently recoverable 2021 Canada-wide hardship percentage |

## What remains unverified

- The official CMHC 2021 Census housing-hardship rate for Canada.
- Official 2021 owner / renter hardship rates from that report.
- Any methodological updates in the 2024 note that differ from the January 2020 Research Insight.

**Do not invent a 2021 CMHC hardship rate.** CIS 2017 ≈ 9% from CMHC Research Insight 69619 remains the only recovered official national hardship benchmark, and it is a different survey, year, and income concept.

## Recovered official methodology that *is* on disk

CMHC Research Insight, *Introducing the Housing Hardship Concept* (January 2020):

https://assets.cmhc-schl.gc.ca/sites/cmhc/data-research/publications-reports/research-insight/2020/research-insight-introducing-housing-hardship-concept-69619-en.pdf

Documented rules used in Stage 1:

- Residual income versus the **non-shelter** MBM, square-root equivalence.
- Regional MBM thresholds.
- MBM disposable income (not Census `TOTINC_AT`).
- Private non-farm non-band non-reserve households.
- Negative residual income excluded from the universe.
- Equivalized income above the **provincial median** cannot be classified as hardship.
- Additional restrictions for investment income/losses, capital gains/losses, or farm income.

The last group of income-source restrictions is **not implementable** on these PUMFs.
