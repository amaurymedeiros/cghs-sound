<CsoundSynthesizer>
<CsOptions>
</CsOptions>
<CsInstruments>
sr = 48000
ksmps = 10
nchnls = 2
0dbfs = 1

gihandle OSCinit 7777
alwayson 1

instr   1
    kf1 init 0

nxtmsg:
    kk  OSClisten gihandle, "/csd", "f", kf1
    if (kk == 0) goto ex
        event "i", 2, 0, 0.5, kf1
    kgoto nxtmsg
ex:
endin

instr 2
	kEnv linseg 0, 0.01, 1, 0.4, 0
	aSig oscils 1/16, p4, 0
	outs aSig*kEnv, aSig*kEnv
endin

</CsInstruments>
<CsScore>
f0 36000
</CsScore>
</CsoundSynthesizer>