from typing import List, Dict, Tuple, Union, Callable
from pathlib import Path
import numpy as np
import pandas as pd
from pandas import DataFrame
import argparse
import json
import requests
import time
from pprint import pprint
from paths import PATHS


def save_df(df: DataFrame,
            save_dir: Path,
            stem: str,
            ext: str) -> None:
    '''
    Helper to save DataFrames.
    '''
    if ext == 'parquet':
        df.to_parquet(save_dir/f'{stem}.parquet',
                      index=False)
    if ext == 'csv':
        df.to_csv(save_dir/f'{stem}.csv',
                  index=False)


def compatible(orig_dir: Path,
               comp_dir: Path,
               ext: str) -> None:

    prefix = 'gerrit'
    comp_dir.mkdir(parents=True, 
                   exist_ok=True)

    # compatible trait file
    t_file = orig_dir/'trait_clean.csv'
    tdf = pd.read_csv(t_file)
    tdf_remap = {}
    tdf_wanted = ['sample_id']
    trait_cols = []
    for c in tdf.columns:
        tkns = c.split('_')
        if tkns[-1] == 'M':
            tdf_remap[c] = tkns[0].lower()
            tdf_wanted.append(tdf_remap[c])
            trait_cols.append(tdf_remap[c])
        elif tkns[-1] == 'SD':
            tdf_remap[c] = f'{tkns[0].lower()}_sdev'
            tdf_wanted.append(tdf_remap[c])
        else:
            tdf_remap[c] = c
    tdf = tdf.rename(columns=tdf_remap)
    tdf = tdf[tdf_wanted]    
    tdf = tdf.dropna(subset=['sample_id'])
    
    tdf_sids = sorted(list(set(tdf['sample_id'].values)))
    trait_cols = sorted(trait_cols)
    
    
    # compatible spectra files
    s_files = [orig_dir/'spec_vnir_clean.csv',
               orig_dir/'spec_swir_clean.csv',
               orig_dir/'spec_all_clean.csv']
    for s_file in s_files:
        key = s_file.stem.split('_')[1]
        
        sdf = pd.read_csv(s_file)
        
        sdf_remap = {}
        sdf_wanted = ['sample_id']
        min_wave, max_wave = 3000.0, 0.0
        for c in sdf.columns:
            try:
                f = float(c)
                sdf_remap[c] = f'X_{f:4.3f}'
                sdf_wanted.append(sdf_remap[c])
                if f < min_wave:
                    min_wave = f
                if f > max_wave:
                    max_wave = f
            except:
                sdf_remap[c] = c
        sdf = sdf.rename(columns=sdf_remap)
        
        sdf = sdf.loc[sdf['sample_id'].isin(tdf_sids)]
        sdf = sdf.dropna()
        sdf['spectrum_id'] = sdf.groupby('sample_id').cumcount() + 1
        sdf['unique_id'] = sdf.apply(lambda r: (str(r['sample_id']) + 
                                                '__' + 
                                                str(r['spectrum_id'])),
                                     axis=1)
        sdf_wanted.insert(1, 'spectrum_id')
        sdf_wanted.insert(2, 'unique_id')
        sdf = sdf[sdf_wanted]
        
        # save
        # saving renamed versions of trait file! 
        # change this if file size gets larger.
        sdf = sdf.sort_values(by=['sample_id', 'spectrum_id'])
        save_df(df=sdf,
                save_dir=comp_dir,
                stem=f'{prefix}{key}_spectra',
                ext=ext)
        wave_ranges = [(min_wave, max_wave)]
        with open(comp_dir/f'{prefix}{key}_waveranges.json', 'w') as fp:
            json.dump(wave_ranges, fp, indent=4)

        tdf = tdf.sort_values(by=['sample_id'])
        save_df(df=tdf,
                save_dir=comp_dir,
                stem=f'{prefix}{key}_traits',
                ext=ext)
        with open(comp_dir/f'{prefix}{key}_traitcols.json', 'w') as fp:
            json.dump(trait_cols, fp, indent=4)

        
if __name__ == '__main__':
    
    # See README.
    
    parser = argparse.ArgumentParser('datasetup.')    
    parser.add_argument('--extension',
                        action='store',
                        default='parquet',
                        choices=['csv', 'parquet'])

    args = parser.parse_args()

    compatible(orig_dir=PATHS['origdata'],
               comp_dir=PATHS['compdata'],
               ext=args.extension)