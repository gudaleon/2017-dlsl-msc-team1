# Paper 1 Draft 4.0 — current status

Date: 17 October 2026  
Branch: `cursor/paper1-draft4-methods-0ace`

Draft 3.0 in `papers/paper1_highschool/` is frozen.

## Verification

The 2011–2021 household series **passes** independent checks (weights, median income, 2021 core-need flag). The 2006 all-household series **fails** income validation because of shelter suppression. Rates are reconstructed research estimates, not official CMHC housing-hardship statistics.

## Primary rates (weighted households)

| Year | n | N | Hardship |
| --- | --- | --- | --- |
| 2011 NHS | 130,242 | 13.02M | 18.2% |
| 2016 | 139,869 | 14.04M | 17.3% |
| 2021 | 148,085 | 14.86M | 14.9% |

## Next increment

Draft 4.0 is locked. The next agent should follow `NEXT_AGENT_INSTRUCTIONS.md` (Draft 5.0): measure distance to official CMHC, recover missing documents, decompose the 2016–2021 decline (COVID ERB vs 2018-base MBM), then lock a publication series. Do not overwrite this folder.
