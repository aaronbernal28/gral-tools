import os
from typing import List, Optional
from pypdf import PdfReader, PdfWriter


def merge_pdfs(
    input_pdf_paths: List[str],
    output_pdf_path: str,
    preserve_bookmarks: bool = True,
    page_range: Optional[tuple] = None
) -> bool:
    """
    Merge multiple PDF files into a single PDF.

    Args:
        input_pdf_paths: List of paths to source PDFs.
        output_pdf_path: Path to target merged PDF.
        preserve_bookmarks: Whether to preserve bookmarks from source PDFs (default True).
        page_range: Optional tuple (start, end) to merge only specific pages from each PDF.
    Returns:
        True on success, False on failure.
    """
    try:
        if not input_pdf_paths:
            raise ValueError("No input PDF paths provided.")
        
        # Verify all input files exist
        for pdf_path in input_pdf_paths:
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"Input file not found: {pdf_path}")
        
        writer = PdfWriter()
        total_pages = 0
        
        print(f"Merging {len(input_pdf_paths)} PDF files...")
        
        for i, pdf_path in enumerate(input_pdf_paths):
            print(f"Processing: {os.path.basename(pdf_path)}")
            
            reader = PdfReader(pdf_path)
            num_pages = len(reader.pages)
            
            # Determine page range
            if page_range:
                start_page, end_page = page_range
                start_page = max(0, min(start_page, num_pages - 1))
                end_page = max(start_page, min(end_page, num_pages))
                pages_to_add = list(range(start_page, end_page))
            else:
                pages_to_add = list(range(num_pages))
            
            # Add pages to writer
            for page_num in pages_to_add:
                page = reader.pages[page_num]
                writer.add_page(page)
                total_pages += 1
            
            # Preserve bookmarks if requested
            if preserve_bookmarks and reader.outline:
                try:
                    writer.clone_reader_document_root(reader)
                except Exception as e:
                    print(f"Warning: Could not preserve bookmarks from {pdf_path}: {e}")
            
            print(f"  Added {len(pages_to_add)} pages from {os.path.basename(pdf_path)}")
        
        # Write merged PDF
        with open(output_pdf_path, "wb") as fout:
            writer.write(fout)
        
        print(f"Successfully merged {len(input_pdf_paths)} PDFs")
        print(f"Total pages in output: {total_pages}")
        print(f"Saved: {output_pdf_path}")
        return True
        
    except Exception as exc:
        import traceback
        print("Error merging PDFs:", exc)
        traceback.print_exc()
        return False


def merge_two_pdfs(
    first_pdf_path: str,
    second_pdf_path: str,
    output_pdf_path: str,
    preserve_bookmarks: bool = True
) -> bool:
    """
    Merge exactly two PDF files into a single PDF.

    Args:
        first_pdf_path: Path to first PDF file.
        second_pdf_path: Path to second PDF file.
        output_pdf_path: Path to target merged PDF.
        preserve_bookmarks: Whether to preserve bookmarks from source PDFs (default True).
    Returns:
        True on success, False on failure.
    """
    return merge_pdfs([first_pdf_path, second_pdf_path], output_pdf_path, preserve_bookmarks)


def convert_merge_pdfs(input_paths, output_path=None, preserve_bookmarks=True):
    """
    Main function to merge PDF files.
    
    Args:
        input_paths (list or str): List of paths to input PDFs, or single path for two-file merge
        output_path (str, optional): Path to output PDF. If None, creates name based on first input
        preserve_bookmarks (bool): Whether to preserve bookmarks from source PDFs
    """
    # Handle single path input (assume it's a pattern or directory)
    if isinstance(input_paths, str):
        if os.path.isdir(input_paths):
            # Get all PDF files from directory
            pdf_files = [f for f in os.listdir(input_paths) if f.lower().endswith('.pdf')]
            input_paths = [os.path.join(input_paths, f) for f in sorted(pdf_files)]
        else:
            raise ValueError("Single string input must be a directory path")
    
    # Verify we have at least 2 files
    if len(input_paths) < 2:
        print("Error: At least 2 PDF files are required for merging.")
        return False
    
    # Generate output path if not provided
    if output_path is None:
        first_file = os.path.splitext(input_paths[0])[0]
        output_path = f"{first_file}_merged.pdf"
    
    print(f"Input files: {len(input_paths)} PDFs")
    for i, path in enumerate(input_paths, 1):
        print(f"  {i}. {os.path.basename(path)}")
    print(f"Output file: {os.path.basename(output_path)}")
    print(f"Preserve bookmarks: {preserve_bookmarks}")
    
    return merge_pdfs(input_paths, output_path, preserve_bookmarks)