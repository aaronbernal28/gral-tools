import sys
from scripts._2pagesPerSheet import convert_pdf_2_pages_per_sheet

def print_usage():
    """Print usage instructions."""
    print("Usage:")
    print("  python pdf_converter.py <input_pdf> [output_pdf] [format]")
    print("")
    print("Arguments:")
    print("  input_pdf   : Path to the input PDF file")
    print("  output_pdf  : Path to the output PDF file (optional)")
    print("  format      : Output format 'A4' or 'Letter' (default: A4)")
    print("")
    print("Example:")
    print("  python run_2pagesPerSheet.py document.pdf")
    print("  python run_2pagesPerSheet.py document.pdf output.pdf A4")


def main():
    """Command line interface."""
    if len(sys.argv) < 2:
        print_usage()
        return
    
    input_pdf = sys.argv[1]
    output_pdf = sys.argv[2] if len(sys.argv) > 2 else None
    page_format = sys.argv[3] if len(sys.argv) > 3 else "A4"
    
    success = convert_pdf_2_pages_per_sheet(input_pdf, output_pdf, page_format)
    
    if success:
        print("Conversion completed successfully!")
    else:
        print("Conversion failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()