import subprocess
import topcoffea.modules.dataDrivenEstimation as dataDrivenEstimation
from work_queue import Factory
from os.path import exists
from os import getcwd

def filecmp(src_fname, dst_fname):
    a = open(src_fname).read().strip()
    b = open(dst_fname).read().strip()
    return a == b

def test_topcoffea():
    args = [
        "time",
        "python",
        "analysis/topEFT/run.py",
        "topcoffea/json/test_samples/UL17_private_ttH_for_CI.json",
        "-o",
        "output_check_yields",
        "-p",
        "analysis/topEFT/histos/",
        "--fixed-seed"
    ]

    # Run TopCoffea
    subprocess.run(args)

    assert(exists('analysis/topEFT/histos/output_check_yields.pkl.gz'))


def test_nonprompt():
    a=dataDrivenEstimation.DataDrivenProducer('analysis/topEFT/histos/output_check_yields.pkl.gz', 'analysis/topEFT/histos/output_check_yields_nonprompt')
    a.dumpToPickle() # Do we want to write this file when testing in CI? Maybe if we ever save the CI artifacts

    assert(exists('analysis/topEFT/histos/output_check_yields_nonprompt.pkl.gz'))

def test_make_yields():
    args = [
        "python",
        "analysis/topEFT/get_yield_json.py",
        "-f",
        "analysis/topEFT/histos/output_check_yields.pkl.gz",
        "-n",
        "analysis/topEFT/output_check_yields"
    ]

    # Produce json
    subprocess.run(args)

def test_compare_yields():
    args = [
        "python",
        "analysis/topEFT/comp_yields.py",
        "analysis/topEFT/output_check_yields.json",
        "analysis/topEFT/test/UL17_private_ttH_for_CI_yields.json",
        "-t1",
        "New yields",
        "-t2",
        "Ref yields"
    ]

    # Run comparison
    subprocess.run(args)

def test_datacard_2l():
    args = [
        "python",
        "analysis/topEFT/datacard_maker.py",
        "analysis/topEFT/histos/output_check_yields_nonprompt.pkl.gz",
        "-j",
        "0",
    ]

    # Run datacard maker
    subprocess.run(args)

    assert filecmp('histos/ttx_multileptons-2lss_p_2b.txt', 'analysis/topEFT/test/ttx_multileptons-2lss_p_2b_ref.txt')

def test_datacard_2l_ht():
    args = [
        "python",
        "analysis/topEFT/datacard_maker.py",
        "analysis/topEFT/histos/output_check_yields.pkl.gz",
        "-j",
        "9"
    ]

    # Run datacard maker
    subprocess.run(args)

    assert filecmp('histos/ttx_multileptons-2lss_p_4j_2b_ht.txt', 'analysis/topEFT/test/ttx_multileptons-2lss_p_4j_2b_ht_ref.txt')

def test_datacard_3l():
    args = [
        "python",
        "analysis/topEFT/datacard_maker.py",
        "analysis/topEFT/histos/output_check_yields.pkl.gz",
        "-j",
        "6"
    ]

    # Run datacard maker
    subprocess.run(args)

    assert filecmp('histos/ttx_multileptons-3l_sfz_1b.txt', 'analysis/topEFT/test/ttx_multileptons-3l_sfz_1b_ref.txt')

def test_datacard_3l_ptbl():
    args = [
        "python",
        "analysis/topEFT/datacard_maker.py",
        "analysis/topEFT/histos/output_check_yields.pkl.gz",
        "-j",
        "24"
    ]

    # Run datacard maker
    subprocess.run(args)

    assert filecmp('histos/ttx_multileptons-3l_onZ_1b_2j_ptbl.txt', 'analysis/topEFT/test/ttx_multileptons-3l_onZ_1b_2j_ptbl_ref.txt')
