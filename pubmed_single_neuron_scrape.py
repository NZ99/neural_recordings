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
        "single neuron recording",
        "spike train",
        "spiking activity",
        "extracellular recording",
        "intracellular recording",
        "multi-unit recording",
        "neuronal firing",
        "action potentials",
    ]

    ephys_hardware = [
        "Neuropixels",
        "silicon probe",
        "tetrode",
        "multi-electrode array",
        "Utah array",
        "depth electrode",
    ]

    # 2) Optical - calcium and voltage imaging
    optical_calcium_voltage = [
        "calcium imaging",
        "two-photon calcium imaging",
        "voltage imaging",
        "genetically encoded calcium indicator",
        "genetically encoded voltage indicator",
    ]

    optical_hardware = [
        "light-sheet microscopy",
        "mesoscope",
        "miniscope",
        "head-mounted microscope",
    ]

    # 3) Neuron-y terms to bias away from purely glial / bulk stuff
    neuron_terms = [
        "neuron",
        "neuronal",
        "neurons",
        "pyramidal cell",
        "interneuron",
        "Purkinje cell",
        "motor neuron",
        "sensory neuron",
        "single neuron",
    ]

    # 4) Optional "large-scale" bias (can drop this if you want everything)
    large_scale = [
        "population recording",
        "neural population activity",
        "simultaneous recording",
        "simultaneously recorded neurons",
        "high-density recording",
        "brain-wide recording",
    ]

    # Combine recording-related keywords
    recording_terms = (
        ephys_single_neuron
        + ephys_hardware
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
