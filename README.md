# gerrit
Code for gerrit

---

# Data setup: Data download and make compatible

- `cd projworks`
- `python gerrit/datasetup.py`


---

# Test `project.py`
- Data setup assumed done.
- `cd projworks`
- `python gerrit/test_project.py --get_data --modelname dplsr__gerritall-phenolics__all__id`
- `python gerrit/test_project.py --get_xtransforms`
- `python gerrit/test_project.py --get_ytransforms`
- `python gerrit/test_project.py --get_modelnames --pattern '*'`

---

# CHTC setup: Create submit files

- `cd projworks`
- `python gerrit/chtcsetup.py --models_per_submit 12`

---

# Note for `run.py`
- `cd projworks`
- Two ways to specify `--train_model`:
   - `python gerrit/run.py --train_model MODELNAME`
   - `python gerrit/run.py --train_model MODELNAME1:MODELNAME2:MODELNAME3:...`
    
---

# CHTC

### local
- `cd projworks`
- `tar --exclude hytraits/test -czf  forchtc/hytraits.tar.gz hytraits/`
- `tar --exclude gerrit/assets --exclude gerrit/origdata --exclude gerrit/gendata -czf forchtc/gerrit.tar.gz gerrit`

### staging
- `hytraits-cpu.sif` must be in `gerrit/toremote`
- Clean `gerrit/fromremote` as needed!

### submit
- Clean `/home/pravindran/gerrit`

### local to staging
- `cd projworks`
- `scp forchtc/hytraits.tar.gz forchtc/gerrit.tar.gz pravindran@transfer.chtc.wisc.edu:/staging/p/pravindran/gerrit/toremote`

### local to submit
- `cd projworks`
- `scp gerrit/assets/chtc_run.sh gerrit/gendata/forchtc/* pravindran@townsend-ap.chtc.wisc.edu:/home/pravindran/gerrit`


### staging to local
- `cd projworks`
- `scp pravindran@transfer.chtc.wisc.edu:/staging/p/pravindran/gerrit/fromremote/<PATTERN>.tar.gz .`

### Extract tar.gzs
- `for file in *.tar.gz; do tar -xzf "$file"; done`
---






