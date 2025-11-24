from datetime import date
from pathlib import Path

from paperscraper.pubmed import get_and_dump_pubmed_papers


def main():
    # Make sure data directory exists
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    out_file = data_dir / f"pubmed_single_neuron_{today}.jsonl"

    # Keep keyword lists short so the generated PubMed query stays under URL limits.
    recording_terms = [
        "single-unit recording",
        "spike train",
        "extracellular recording",
        "multi-unit recording",
        "Neuropixels",
        "silicon probe",
        "calcium imaging",
        "voltage imaging",
    ]

    neuron_terms = [
        "neuron",
        "neuronal",
    ]

    large_scale = [
        "population recording",
        "simultaneous recording",
        "high-density recording",
    ]

    # Outer list items are ANDed, inner list items are ORed by paperscraper.
    query = [recording_terms, neuron_terms, large_scale]

    print("Running PubMed query via paperscraper...")
    print("This corresponds roughly to:")
    print("  (recording) AND (neuron) AND (large-scale-ish) AND (2021+ date)")
    print(f"Saving results to: {out_file}")

    get_and_dump_pubmed_papers(
        query,
        output_filepath=str(out_file),
        start_date="2021/01/01",
    )

    print("Done.")


if __name__ == "__main__":
    main()
