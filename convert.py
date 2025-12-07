import os
import rawpy
import imageio.v2 as imageio  # v2-API ist stabiler

# --- CONFIG -----------------------------------------------------------------

INPUT_FOLDER = "/Users/beratuzun/Desktop/einzel"
OUTPUT_FOLDER = "/Users/beratuzun/Desktop/pngs"

SUPPORTED_RAW_EXT = (".cr2", ".nef", ".arw", ".dng", ".rw2")

# ---------------------------------------------------------------------------

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def is_raw_file(filename: str) -> bool:
    return filename.lower().endswith(SUPPORTED_RAW_EXT)

def main():
    # Alle Dateien im Input-Ordner
    all_files = [f for f in os.listdir(INPUT_FOLDER) if os.path.isfile(os.path.join(INPUT_FOLDER, f))]
    raw_files = [f for f in all_files if is_raw_file(f)]

    total_raw = len(raw_files)
    processed = 0
    failed = 0

    print(f"Gefundene RAW-Dateien: {total_raw}")

    for filename in raw_files:
        raw_path = os.path.join(INPUT_FOLDER, filename)
        name_without_ext, _ = os.path.splitext(filename)
        output_png = os.path.join(OUTPUT_FOLDER, f"{name_without_ext}.png")

        print(f"\nVerarbeite: {filename}")
        try:
            # RAW -> RGB
            with rawpy.imread(raw_path) as raw:
                rgb = raw.postprocess()

            # als PNG speichern
            imageio.imwrite(output_png, rgb)
            print(f"✅ Gespeichert als: {output_png}")
            processed += 1

        except Exception as e:
            print(f"❌ Fehler bei {filename}: {e}")
            failed += 1

    print("\n--- Zusammenfassung ---")
    print(f"RAW-Dateien gefunden:    {total_raw}")
    print(f"Erfolgreich konvertiert: {processed}")
    print(f"Fehlgeschlagen:          {failed}")
    print(f"PNG-Output-Ordner:       {OUTPUT_FOLDER}")

if __name__ == "__main__":
    main()