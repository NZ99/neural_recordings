from datetime import date
from pathlib import Path

from paperscraper.pubmed import get_and_dump_pubmed_papers


def main():
    # Make sure data directory exists
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    out_file = data_dir / f"pubmed_single_neuron_{today}.jsonl"

    # Build a compact PubMed boolean query to avoid 414 URI errors.
    query = (
        '(Neuropixels OR "silicon probe" OR "single-unit recording" OR '
        '"spike train" OR "extracellular recording" OR "calcium imaging" OR '
        '"voltage imaging") AND (neuron OR neuronal) AND '
        '("2021/01/01"[Date - Publication] : "3000"[Date - Publication])'
    )

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
