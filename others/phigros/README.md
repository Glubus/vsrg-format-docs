# Phigros and Phigros fan-chart ecosystem

Phigros (Pigeon Games, 2021) is a touch rhythm game where notes fall onto freely moving, rotating **judgement lines**; every chart has dozens of lines with their own position/rotation/opacity/speed event tracks, and each note belongs to one line (above or below). Fan engines (Re:PhiEdit, PhiEdit, Phira, phi-chart-render, prpr, Phichain) added more formats around it.

Category: **others**. There are no fixed lanes or columns: a note's horizontal position is relative to a line that moves and rotates, so the ROX column model cannot represent it without destroying the chart.

Formats documented:

- [`official-json/`](official-json/README.md) - official Phigros chart JSON (`formatVersion` 1 / 3).
- [`rpe/`](rpe/README.md) - Re:PhiEdit chart JSON ("RPEJSON": BPMList, META, eventLayers, beat triples).
- [`pec/`](pec/README.md) - PhiEdit Chart text (`.pec`).
- [`phi-common-chart/`](phi-common-chart/README.md) - PhiFanmade "PhiCommonChart" protobuf-based interchange model (stub).

Links: <https://github.com/Hxjjxg/phi_reversed>, <https://github.com/TeamFlos/phira-docs>, <https://docs.nuanr-mxi.com/en/>, <https://ivan-1f-phichain.mintlify.app/>.
