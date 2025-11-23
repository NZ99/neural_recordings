from datetime import date
from pathlib import Path

from paperscraper.pubmed import get_and_dump_pubmed_papers


def main():
    # Make sure data directory exists
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    out_file = data_dir / f"pubmed_single_neuron_{today}.jsonl"

    # 1) Ephys - single-unit / spikes / intracellular
    ephys_single_neuron = [
        "single-unit recording",
        "single unit recording",
        "single-units",
        "single units",
        "single-neuron recording",
        "single neuron recording",
        "single-neuron activity",
        "spike sorting",
        "spike-sorted",
        "spike train",
        "spike trains",
        "spiking activity",
        "extracellular recording",
        "extracellular recordings",
        "multi-unit recording",
        "multiunit recording",
        "multi-unit activity",
        "MUA",
        "single-unit activity",
        "SUA",
        "intracellular recording",
        "intracellular recordings",
        "intracortical recording",
        "intracortical recordings",
        "neuronal firing",
        "action potentials",
    ]

    ephys_hardware = [
        "Neuropixels",
        "Neuropixel",
        "silicon probe",
        "silicon probes",
        "polytrode",
        "polytrodes",
        "tetrode",
        "tetrodes",
        "stereotrode",
        "stereotrodes",
        "multi-electrode array",
        "multielectrode array",
        "microelectrode array",
        "micro-electrode array",
        "MEA",
        "laminar probe",
        "laminar probes",
        "Utah array",
        "Utah electrode array",
        "depth electrode",
        "depth electrodes",
        "microelectrode",
        "microelectrodes",
    ]

    patch_intracellular = [
        "patch clamp",
        "patch-clamp",
        "whole-cell patch clamp",
        "whole cell patch clamp",
        "in vivo patch clamp",
        "in vivo whole-cell",
        "cell-attached recording",
        "cell attached recording",
        "juxtacellular recording",
        "juxtacellular recordings",
        "sharp electrode recording",
        "sharp-electrode recording",
        "current-clamp",
        "current clamp",
        "voltage-clamp",
        "voltage clamp",
        "two-photon targeted patching",
    ]

    # 2) Optical - calcium and voltage imaging
    optical_calcium_voltage = [
        "calcium imaging",
        "Ca2+ imaging",
        "two-photon calcium imaging",
        "two photon calcium imaging",
        "2-photon calcium imaging",
        "2 photon calcium imaging",
        "three-photon calcium imaging",
        "three photon calcium imaging",
        "3-photon calcium imaging",
        "3 photon calcium imaging",
        "widefield calcium imaging",
        "wide-field calcium imaging",
        "one-photon calcium imaging",
        "one photon calcium imaging",
        "voltage imaging",
        "optical voltage imaging",
        "genetically encoded calcium indicator",
        "genetically encoded calcium indicators",
        "GECI",
        "GCaMP",
        "GCaMP6",
        "genetically encoded voltage indicator",
        "genetically encoded voltage indicators",
        "GEVI",
    ]

    optical_hardware = [
        "two-photon microscopy",
        "two photon microscopy",
        "2-photon microscopy",
        "2 photon microscopy",
        "three-photon microscopy",
        "three photon microscopy",
        "3-photon microscopy",
        "3 photon microscopy",
        "light-sheet microscopy",
        "light sheet microscopy",
        "scanning light-sheet",
        "light-field microscopy",
        "light field microscopy",
        "confocal microscopy",
        "spinning disk confocal",
        "mesoscope",
        "mesoscopes",
        "miniscope",
        "miniscopes",
        "microendoscope",
        "microendoscopes",
        "head-mounted microscope",
        "head mounted microscope",
    ]

    # 3) Neuron-y terms to bias away from purely glial / bulk stuff
    neuron_terms = [
        "neuron",
        "neuronal",
        "neurons",
        "pyramidal cell",
        "pyramidal cells",
        "interneuron",
        "interneurons",
        "Purkinje cell",
        "Purkinje cells",
        "motoneuron",
        "motoneurons",
        "motor neuron",
        "motor neurons",
        "sensory neuron",
        "sensory neurons",
        "principal cell",
        "principal cells",
        "single-neuron",
        "single neuron",
    ]

    # 4) Optional "large-scale" bias (can drop this if you want everything)
    large_scale = [
        "large-scale neural recordings",
        "large scale neural recordings",
        "large-scale recording",
        "large scale recording",
        "population recording",
        "population recordings",
        "population activity",
        "neural population activity",
        "simultaneous recording",
        "simultaneously recorded neurons",
        "simultaneously recorded",
        "simultaneous multi-site recording",
        "high-density recording",
        "high density recording",
        "brain-wide recording",
        "brain wide recording",
        "whole-brain imaging",
        "whole brain imaging",
        "thousands of neurons",
        "hundreds of neurons",
    ]

    # Combine recording-related keywords
    recording_terms = (
        ephys_single_neuron
        + ephys_hardware
        + patch_intracellular
        + optical_calcium_voltage
        + optical_hardware
    )

    # PubMed date filter: 2021-01-01 to "far future"
    # This uses official PubMed syntax: "2021/01/01"[Date - Publication] : "3000"[Date - Publication]
    date_filter = ['"2021/01/01"[Date - Publication] : "3000"[Date - Publication]']

    # Build the paperscraper query:
    # (recording_terms) AND (neuron_terms) AND (date_filter) AND (large_scale)
    # You can remove "large_scale" from the list below if you want a broader net.
    query = [
        recording_terms,
        neuron_terms,
        date_filter,
        large_scale,
    ]

    print("Running PubMed query via paperscraper...")
    print("This corresponds roughly to:")
    print("  (recording) AND (neuron) AND (2021+ date) AND (large-scale-ish)")
    print(f"Saving results to: {out_file}")

    get_and_dump_pubmed_papers(
        query,
        output_filepath=str(out_file),
    )

    print("Done.")


if __name__ == "__main__":
    main()
