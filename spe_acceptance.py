#!/project/lgrandi/anaconda3/envs/pax_head/bin/python

#### takes two arguments ####

# 1: LED run number (not blank)
# 2: blank run number
# 3: LED run path
# 4: blank run path

# TODO: find blank run number automatically

import logging
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib
matplotlib.use('Agg')
matplotlib.rc('font', size=16)
import matplotlib.pyplot as plt
from pax import core, units, dsputils
import multihist
from hax.pmt_plot import plot_on_pmt_arrays, pmt_data
from channel_dict import channel_dict
from DB_stuff import get_file_path
from analyze import data_dir_base
import sys
import os
import scipy.integrate as integrate
import shutil

# load run into pax
def get_run(run):
    mypax = core.Processor(config_names='XENON1T', config_dict={
        'pax': {
            'plugin_group_names': ['input', 'preprocessing'],
            'preprocessing':      ['CheckPulses.SortPulses',
                                   'CheckPulses.ConcatenateAdjacentPulses',],
            'input':              'Zip.ReadZipped',
            'encoder_plugin':     None,
            #'decoder_plugin':     'BSON.DecodeZBSON',
            'input_name':          run
        }
    })
    return mypax

# generator used to loop over events
def get_events(RUN):
    for event in RUN.get_events():
        event = RUN.process_event(event)
        yield event

# loop over LED and noise runs, fill histograms
def loop_over_events(LED_file, noise_file, LED_multihist, noise_multihist, spe_integral, noise_integral):
    LED_run = get_run(LED_file)
    noise_run = get_run(noise_file)

    LED_events = LED_run.input_plugin.number_of_events
    noise_events = noise_run.input_plugin.number_of_events

    noise_event_generator = get_events(noise_run)
    LED_event_generator = get_events(LED_run)

    n_loop_events = min(noise_events, LED_events)

    amplitude_bounds = (-100, 1000)
    n_channels = 254

    LED_window = [125, 175]

    noise_good_events_seen = 0
    LED_good_events_seen = 0

    runs = ['noise', 'LED']

    # get first event to check parameters:

    noise_event_0 = next(noise_event_generator)
    LED_event_0 = next(LED_event_generator)

    noise_pulses = len(noise_event_0.pulses)
    LED_pulses = len(LED_event_0.pulses)
    print("noise_run pulses per event: %d" % noise_pulses)
    print("LED_run pulses per event: %d" % LED_pulses)
    noise_samples_per_pulse = len(noise_event_0.pulses[0].raw_data)
    LED_samples_per_pulse = len(LED_event_0.pulses[0].raw_data)
    print("noise_run samples per pulse: %d" % noise_samples_per_pulse)
    print("LED_run samples per pulse: %d" % LED_samples_per_pulse)

    if noise_samples_per_pulse == LED_samples_per_pulse:
        samples_per_pulse = noise_samples_per_pulse
    else:
        print("noise samples per pulse different than LED samples per pulse. Aborting.")
        return

    for event_i in tqdm(range(n_loop_events - 1)):
        for run in runs:
            if run == 'noise':
                event = next(noise_event_generator)

            else:
                event = next(LED_event_generator)

            if not (len(event.pulses) == n_channels):
                # Ignore weird events where not all channels are present
                # These are probably due to a bug in the event builder
                continue

            if run == 'noise':
                noise_good_events_seen += 1
            else:
                LED_good_events_seen += 1

            channel_list = np.ones(n_channels)

            amplitude_list = np.ones(n_channels)  # (len(show_channels))

            charge_list = np.ones(n_channels)

            counter = 0

            for p in event.pulses:
                w = p.raw_data
                assert len(w) == samples_per_pulse

                w = np.median(w) - w  # Baseline the waveform by subtracting the median, flip signal

                spe = w[LED_window[0]:LED_window[1]]  # consider LED window only
                spe = np.clip(spe, *amplitude_bounds)


                channel_list[counter] = p.channel

                amplitude_list[counter] = max(spe)

                # for the charge spectrum
                charge = integrate.simps(spe)
                charge_list[counter] = charge

                counter += 1

            if run == 'noise':
                noise_multihist.add(channel_list, amplitude_list)
                noise_integral.add(channel_list, charge_list)

            else:
                LED_multihist.add(channel_list, amplitude_list)
                spe_integral.add(channel_list, charge_list)

    print("noise: %d proper events seen in %d events" % (noise_good_events_seen, n_loop_events))
    print("LED: %d proper events seen in %d events" % (LED_good_events_seen, n_loop_events))


def find_threshold(hist1d, acc_frac):
    acceptance = 1 - hist1d.cumulative_density
    next_a, next_b = (-99, -99)  # inital nonsense values
    thresh = 0

    for a, b in zip(reversed(acceptance), reversed(hist1d.bin_edges)):
        if (a >= acc_frac >= next_a):
            if (abs(a - acc_frac) < abs(next_a - acc_frac)):
                thresh = b
            else:
                thresh = next_b
            break
        next_a = a
        next_b = b

    return int(thresh)

def calculate_acceptances(LED_multihist, noise_multihist, spe_integral, noise_integral, data_dir, show_channels = channel_dict["all_channels"]):
    from matplotlib import cm

    n_channels = 254
    WRITE = True
    acceptance_list = np.arange(0.05, 1, 0.05)

    thresholds_file = data_dir + "/thresholds.csv"
    histograms_file = data_dir + "/histograms.csv"

    if WRITE:
        print("Writing to %s and %s" % (thresholds_file, histograms_file))
        f_thresh = open(thresholds_file, 'w')
        f_hist = open(histograms_file, 'w')

        f_thresh.write("ch")
        for a in acceptance_list:
            f_thresh.write("," + str(a))
        f_thresh.write("\n")

        f_hist.write("ch,amplitude,LED,LEDerr,NOISE,NOISEerr,NOISEcorr,residual,residualerr,"
                     "acceptance,LED_charge,NOISE_charge,spe_spectrum\n")

    channel_list = []
    threshold_list = [[], [], [], [], []]

    correct_bins = [3, 4, 5, 6, 7]
    correct_bins = [6]
    corrections = []
    corr_chan_list = []


    for bin_correct_i, bin_correct in enumerate(correct_bins):
        plt.figure(1)
        for ch in tqdm(range(n_channels)):
            if ch not in channel_dict["all_channels"]:
                continue
            channel = ch

            noise_spectrum = noise_multihist.slice(ch, ch, 'channel').project('amplitude')
            LED_spectrum = LED_multihist.slice(ch, ch, 'channel').project('amplitude')

            noise_integral_spectrum = noise_integral.slice(ch,ch, 'channel').project('charge')
            spe_integral_spectrum = spe_integral.slice(ch,ch, 'channel').project('charge')

            noise_errors = np.sqrt(noise_spectrum.histogram)
            LED_errors = np.sqrt(LED_spectrum.histogram)

            noise_run_before_correction = noise_spectrum.histogram
            noise_errors_before_correction = noise_errors

            bin0 = np.where(noise_spectrum.bin_edges == 0)[0][0]
            LED_firstN = LED_spectrum.histogram[bin0:(bin0 + bin_correct)].sum()
            noise_firstN = noise_spectrum.histogram[bin0:(bin0 + bin_correct)].sum()

            LED_charge_firstN = spe_integral_spectrum.histogram[0 : (bin0 - 5)].sum()
            noise_charge_firstN = noise_integral_spectrum.histogram[0 : (bin0 - 5)].sum()

            correction = LED_firstN / noise_firstN
            area_correction = LED_charge_firstN/noise_charge_firstN
            corrections.append(correction)
            corr_chan_list.append(ch)

            noise_spectrum.histogram = noise_run_before_correction * correction
            noise_errors = noise_errors_before_correction * correction

            residual_spe = LED_spectrum - noise_spectrum
            residual_spe_errors = np.sqrt(LED_errors ** 2 + noise_errors ** 2)

            thresh_90 = find_threshold(residual_spe, 0.9)

            noise_integral_before_corr = noise_integral_spectrum.histogram
            noise_integral_spectrum.histogram *= area_correction
            spe_distribution = spe_integral_spectrum - noise_integral_spectrum

            if WRITE and bin_correct == 6:
                f_thresh.write(str(ch))

                for a in acceptance_list:
                    T = find_threshold(residual_spe, a)
                    f_thresh.write("," + str(T))
                f_thresh.write("\n")

            residual_cum = residual_spe.cumulative_density
            residual_cum = 1 - residual_cum

            if bin_correct_i == 0:
                channel_list.append(ch)
            threshold_list[bin_correct_i].append(thresh_90)

            if WRITE and bin_correct == 6:
                for BIN in range(len(residual_spe.histogram)):
                    f_hist.write("{CH},{amp},{LED},{LEDerr},{NOISE},{NOISEerr},{NOISEcorr},"
                                 "{residual},{residualerr},{acceptance},{LED_charge},{noise_charge},{spe_area}\n".format(
                        CH=ch,
                        amp=residual_spe.bin_centers[BIN], LED=LED_spectrum.histogram[BIN],
                        LEDerr=LED_errors[BIN], NOISE=noise_spectrum.histogram[BIN], NOISEerr=noise_errors[BIN],
                        NOISEcorr=correction, residual=residual_spe.histogram[BIN],
                        residualerr=residual_spe_errors[BIN],
                        acceptance=residual_cum[BIN], LED_charge=spe_integral_spectrum.histogram[BIN],
                        noise_charge=noise_integral_before_corr[BIN],
                        spe_area=spe_distribution.histogram[BIN]))

            plt.plot(residual_spe.bin_centers, residual_cum,
                     color=cm.spectral(1 * show_channels.index(ch) / len(show_channels)), label='%i' % ch)

            plt.xlim(-20, 200)
            plt.ylim(-0.1, 1.2)
            plt.title("Acceptance (correct %d bin)" % bin_correct)

            plt.xlabel('threshold')
            plt.ylabel('spe acceptance')
            # plt.legend(loc = 'upper left', bbox_to_anchor=(1, 1), fontsize = 10, frameon=False)
            plt.grid(b=True)
            plt.savefig(data_dir + '/acceptance_corr%d.png' % bin_correct)

def main(args):
    # set logging default to INFO, setup plotting stuff
    logging.basicConfig(level=logging.INFO)
    plt.rcParams['figure.figsize'] = (12.0, 10.0)    # resize plots

    # make sure we have right number of args
    if len(args) != 4:
        print("4 arguments required, (1) LED, (2) noise run numbers, (3) LED path, (4) noise path")
        return

    # get LED and blank run numbers from args
    LED_run_number = int(args[0])
    noise_run_number = int(args[1])

    LED_file = args[2]
    noise_file = args[3]

    print("LED run: %d at %s" % (LED_run_number, LED_file))
    print("noise run: %d at %s" % (noise_run_number, noise_file))

    amplitude_bounds = (-100, 1000)
    n_channels = 254

    noise_multihist = multihist.Histdd(axis_names=['channel', 'amplitude'],
                                       bins=(np.arange(-1, n_channels + 1),
                                             np.arange(*amplitude_bounds)))

    LED_multihist = multihist.Histdd(axis_names=['channel', 'amplitude'],
                                     bins=(np.arange(-1, n_channels + 1),
                                           np.arange(*amplitude_bounds)))

    spe_integral = multihist.Histdd(axis_names=['channel', 'charge'],
                                    bins=(np.arange(-1, n_channels + 1),
                                          np.arange(*amplitude_bounds)))

    noise_integral = multihist.Histdd(axis_names=['channel', 'charge'],
                                      bins=(np.arange(-1, n_channels + 1),
                                            np.arange(*amplitude_bounds)))

    loop_over_events(LED_file, noise_file, LED_multihist, noise_multihist, spe_integral, noise_integral)

    data_dir = data_dir_base + "run_%d" % LED_run_number

    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)

    calculate_acceptances(LED_multihist, noise_multihist, spe_integral, noise_integral, data_dir)



if __name__ == "__main__":
    main(sys.argv[1:])
    # remove raw data so not to take up space on midway
    shutil.rmtree(sys.argv[3])



