#!/usr/bin/env python3
# coding: utf-8

from pathlib import Path
import os, tempfile, subprocess

class MulandException(Exception):
    pass

class ModelNotFound(MulandException):
    pass

class DependencyError(MulandException):
    pass

class Muland:
    '''Access Muland Application'''

    muland_binary='bin/muland'
    model_folder='model'
    work_folder='work'
    agents_file='agents.csv'
    agents_zones_file='agents_zones.csv'
    bids_adjustments_file='bids_adjustments.csv'
    bids_functions_file='bids_functions.csv'
    demand_file='demand.csv'
    demand_exogenous_cutoff_file='demand_exogenous_cutoff.csv'
    real_estates_zones_file='real_estates_zones.csv'
    rent_adjustments_file='rent_adjustments.csv'
    rent_functions_file='rent_functions.csv'
    subsidies_file='subsidies.csv'
    supply_file='supply.csv'
    zones_file='zones.csv'
    model_files=[agents_file, agents_zone_file, bids_adjustments_file,
        bids_functions_file, demand_file, demand_exogenous_cutoff_file,
        real_estates_zones_file, rent_adjustments_file, rent_functions_file,
        subsidies_file, supply_file, zones_file]

    # Check if muland binary, model folder and work folder are in place
    if not os.access(work_folder, os.R_OK & os.W_OK):
        if os.access(work_folder, os.F_OK):
            raise DependencyError('Could not access work directory.')
        os.mkdir(work_folder)

    if not os.access(muland_binary, os.X_OK):
        raise DependencyError('Could not find muland binary.')

    if not os.access(model_folder, os.R_OK):
        raise DependencyError('Could not access model directory.')

    def __init__(self, model):
        '''Initialize Muland'''
        # Check if model exists
        model_folder = self.model_folder
        for file in self.model_files:
            acessible=os.access(str(Path(model_folder, file)), os.R_OK)
            if not accessible:
                raise ModelNotFound('Specified model was not found.')
        self.model=model

    def _populate_working_dir(self, working_dir):
        '''Prepares data for Muland reading'''
        # Create input and output directories
        os.mkdir(str(Path(working_dir.name, 'input')))
        os.mkdir(str(Path(working_dir.name, 'output')))

        # Populate input directory
        for file in self.model_files:
            model_file_path=str(Path(model_folder, file))
            work_file_path=str(Path(working_dir.name, 'input', file))
            os.symlink(model_file_path, work_file_path)

    def _run_muland(self, working_dir):
        '''Run Muland on working dir'''
        subprocess.Popen(self.muland_binary, working_dir)

    def _collect_data(self, working_dir):
        '''Collects data generated by Muland'''
        pass

    def run(self):
        '''Runs Muland'''
        model=self.model

        # Create data directory
        with tempfile.TemporaryDirectory(dir=self.work_folder) as working_dir:
            # Prepare directory
            self._populate_working_dir(working_dir)

            # Run Muland
            self._run_muland(working_dir)

            # Collect data
            self._collect_data(working_dir)