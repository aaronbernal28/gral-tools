import sys
from scripts._merge import convert_merge_pdfs

def print_usage():
    """Print usage instructions."""
    print("Usage:")
    print("  python run_merge.py <input1_pdf> <input2_pdf> [output_pdf]")
    print("  python run_merge.py <directory_path> [output_pdf]")
    print("")
    print("Arguments:")
    print("  input1_pdf   : Path to the first input PDF file")
    print("  input2_pdf   : Path to the second input PDF file")
    print("  directory_path : Path to directory containing PDF files to merge")
    print("  output_pdf   : Path to the output PDF file (optional)")
    print("")
    print("Examples:")
    print("  python run_merge.py document1.pdf document2.pdf")
    print("  python run_merge.py document1.pdf document2.pdf merged.pdf")
    print("  python run_merge.py /path/to/pdf/folder/")
    print("  python run_merge.py /path/to/pdf/folder/ all_merged.pdf")

def main():
    """Command line interface."""
    if len(sys.argv) < 2:
        print_usage()
        return
    
    # Parse arguments
    if len(sys.argv) == 2:
        # Single argument - must be directory
        input_pdfs = sys.argv[1]
        output_pdf = None
        print(f"Mode: Directory merge - {input_pdfs}")
    elif len(sys.argv) == 3:
        # Two arguments - could be two files or directory + output
        import os
        if os.path.isdir(sys.argv[1]):
            # Directory + output file
            input_pdfs = sys.argv[1]
            output_pdf = sys.argv[2]
            print(f"Mode: Directory merge with output - {input_pdfs} -> {output_pdf}")
        else:
            # Two PDF files
            input_pdfs = [sys.argv[1], sys.argv[2]]
            output_pdf = None
            print(f"Mode: Two file merge - {input_pdfs}")
    elif len(sys.argv) == 4:
        # Three arguments - two input files + output
        input_pdfs = [sys.argv[1], sys.argv[2]]
        output_pdf = sys.argv[3]
        print(f"Mode: Two file merge with output - {input_pdfs} -> {output_pdf}")
    else:
        print("Error: Too many arguments.")
        print_usage()
        return

    success = convert_merge_pdfs(input_pdfs, output_pdf)

    if success:
        print("Merge completed successfully!")
    else:
        print("Merge failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()