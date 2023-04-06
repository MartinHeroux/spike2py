






""""

how to provide background window for trials such as trains; needed to id threshold

# --------------------------

User inputs trigger channel to use (e.g. 'stim') and keyboard (e.g. 'keyboard')

Clean the trigger channel if required (carrier_fq, pair_isi, train_fq);
if not, assume that every pulse is a trigger

#------------
User specified if should process entire trial or if want to pick section (ginput) or use Keyboard markers:
if ginput:
asked/provide number of windows of interest; and provide labels [ ['mMax', window], ['threshold single', window], ['ins', background']]

??? for trains...are they all useful and at same intensity, or is there different intensity, and there is a need to find a steady ampl before
extracting; ask user how many to extract (or duration) and if there is an offset from start of stable stim

if keyboard markers... user provides markers (e.g. {'1': 'threshold period', '2': 'threshold + 5 doubles'}

# -----------
User needs to specify time period to extract for each reflex ([-5, 40] i.e. -5ms to 40ms)

# ------------

extract reflexes, and relevant info and store in ?? structure

 - trigger time
 - extracted waveform (e.g. from -25 to 40ms)
        - entire thing for doubles
        - plus each pulse for doubles
 - peak-to-peak
 - area
 - onset time

# ------------

extract threshold intensity
- average n reflexes for each intensity
- then, based on background activity, select the intensity when the reflex first appears
can try to automate this, but also good to have a visual threshold selector






"""