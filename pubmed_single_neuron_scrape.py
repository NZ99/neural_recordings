from datetime import date
from pathlib import Path

from paperscraper.pubmed import get_and_dump_pubmed_papers


def main():
    # Make sure data directory exists
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)

    # Ensure biorxiv dump is available locally (used by paperscraper for enrichment)
    dumps_dir = Path("server_dumps")
    biorxiv_dump = dumps_dir / "biorxiv_since_2021.jsonl"
    if not biorxiv_dump.exists() or biorxiv_dump.stat().st_size == 0:
        print("Downloading biorxiv dump from 2021-01-01 (first run can take hours)...")
        dumps_dir.mkdir(parents=True, exist_ok=True)
        from paperscraper.get_dumps import biorxiv

        biorxiv(start_date="2021-01-01", save_path=str(biorxiv_dump))
    else:
        size_mb = biorxiv_dump.stat().st_size / 1e6
        print(f"Using cached biorxiv dump ({size_mb:.1f} MB)")

    today = date.today().isoformat()
    out_file = data_dir / f"pubmed_single_neuron_{today}.jsonl"

    # Keep keyword list compact to stay under URL limits but broad enough not to miss papers.
    recording_terms = [
        # generic ephys
        "electrophysiolog*",
        # specific ephys methods / hardware
        "single unit",
        "multiunit",
        "spike train",
        "extracellular recording",
        "intracellular recording",
        "patch clamp",
        "microelectrode array",
        "multi electrode array",
        "Neuropixels",
        # optical calcium / voltage
        "calcium imaging",
        "two photon",
        "three photon",
        "light sheet",
        "miniscope",
        "mesoscope",
        "voltage imaging",
        "GCaMP",
        "GEVI",
    ]

    # Outer list items are ANDed, inner list items are ORed by paperscraper.
    # We intentionally omit an explicit neuron filter to avoid missing relevant papers.
    query = [recording_terms]

    print("Running PubMed query via paperscraper...")
    print("This corresponds roughly to:")
    print("  (recording/ephys/optical) AND (2021+ date)")
    print(f"Saving results to: {out_file}")

    get_and_dump_pubmed_papers(
        query,
        output_filepath=str(out_file),
        start_date="2021/01/01",
    )

    print("Done.")


if __name__ == "__main__":
    main()
