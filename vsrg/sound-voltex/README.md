# SOUND VOLTEX (and K-Shoot MANIA)

SOUND VOLTEX (SDVX) is Konami's arcade game (since 2012; 6 buttons + 2 analog knobs): four white BT buttons (A-D) and two FX buttons along the bottom, and two laser lanes (left blue knob, right red knob). Laser notes are connected paths across the full width of the highway, with "slams" (instant jumps) and lane tilt/spin camera effects. Fan-made simulators use the K-Shoot MANIA format: K-Shoot MANIA (KSM, Windows/macOS), Unnamed SDVX Clone (USC), voltedit, Nautica (chart database), etc.

Category: vsrg (borderline). The six button lanes are fixed vertical lanes with taps and holds falling toward a judgement line, the VSRG column model. Lasers have free analog position along the width (a continuous curve per knob plus slams), so converting to a plain ROX column chart loses laser data.

Formats:
- [`ksh`](ksh/README.md): K-Shoot MANIA text chart (de-facto community format; complete public spec).
- [`kson`](kson/README.md): K-Shoot MANIA JSON successor (formal spec, pulse resolution 240/beat).
- [`vox`](vox/README.md): arcade game chart text file (reverse-engineered; versions 10/12/13).

Related non-chart files (not documented as formats here): `.s3v` / `.s3p` audio containers (the rmstZ changelog lists their reading), arcade `music_db.xml`.

Links: https://www.kshootmania.com/ · https://github.com/kshootmania/ksm-chart-format · https://www.sdvx.org/en/charting/kshfile · https://github.com/Drewol/unnamed-sdvx-clone · https://kson.dev/
