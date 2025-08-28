import os
from typing import Tuple, Union
from pypdf import PdfReader, PdfWriter, PageObject, Transformation
from reportlab.lib.pagesizes import letter, A4


def create_2_pages_per_sheet(
    input_pdf_path: str,
    output_pdf_path: str,
    page_size: Union[str, Tuple[float, float]] = "A4",
    margin_pt: float = 12.0,
    scale_up: bool = False,
) -> bool:
    """
    Convert a PDF to 2-pages-per-sheet (landscape) and save result.

    Args:
        input_pdf_path: Path to source PDF.
        output_pdf_path: Path to target PDF.
        page_size: "A4" or (width_pts, height_pts) tuple. Default "A4".
        margin_pt: margin in points to leave around each placed page (default 12pt).
        scale_up: whether to upscale small pages to fill available area (default False).
    Returns:
        True on success, False on failure.
    """
    try:
        # Resolve page size
        if isinstance(page_size, str):
            if page_size.upper() == "A4":
                page_w, page_h = A4
            else:
                raise ValueError("Unknown page_size string. Use 'A4' or provide (w,h) in points.")
        else:
            page_w, page_h = page_size

        # Force landscape: width must be >= height
        output_width = max(page_w, page_h)
        output_height = min(page_w, page_h)

        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()
        total_pages = len(reader.pages)
        print(f"Input pages: {total_pages}")
        print(f"Output sheet size (pts): {output_width:.2f} x {output_height:.2f} (landscape)")

        # Available area for each source page: half sheet minus margins
        half_width = output_width / 2.0
        available_width = half_width - 2 * margin_pt
        available_height = output_height - 2 * margin_pt
        if available_width <= 0 or available_height <= 0:
            raise ValueError("Margins too large for chosen page size.")

        # Process pages in pairs
        for i in range(0, total_pages, 2):
            # new blank landscape page
            new_page = PageObject.create_blank_page(width=output_width, height=output_height)

            for side in (0, 1):  # 0 -> left, 1 -> right
                src_index = i + side
                if src_index >= total_pages:
                    # no source page (odd count), leave blank
                    continue

                src = reader.pages[src_index]

                # get source width/height and rotation
                orig_src_w = float(src.mediabox.width)
                orig_src_h = float(src.mediabox.height)
                try:
                    rotation = int(src.get("/Rotate", 0)) % 360
                except Exception:
                    rotation = 0

                # Compute viewed (effective) dimensions after rotation
                if rotation in (90, 270):
                    viewed_w = orig_src_h
                    viewed_h = orig_src_w
                else:
                    viewed_w = orig_src_w
                    viewed_h = orig_src_h

                # compute scale (don't upscale unless scale_up True)
                scale_x = available_width / viewed_w
                scale_y = available_height / viewed_h
                scale = min(scale_x, scale_y)
                if not scale_up:
                    scale = min(scale, 1.0)

                # final scaled dimensions
                scaled_w = viewed_w * scale
                scaled_h = viewed_h * scale

                # compute center position (left or right half)
                center_x = (output_width * (0.25 if side == 0 else 0.75))
                center_y = output_height / 2.0

                tx = center_x - (scaled_w / 2.0)
                ty = center_y - (scaled_h / 2.0)

                # Build transformation: start with identity
                transform = Transformation()

                # If rotated, flatten by applying equivalent transformation (bake /Rotate into content)
                if rotation != 0:
                    rot_deg = -rotation  # Transform rotate is counterclockwise; /Rotate is clockwise
                    flatten_tx = 0
                    flatten_ty = 0
                    if rotation == 90:
                        flatten_ty = orig_src_w
                    elif rotation == 180:
                        flatten_tx = orig_src_w
                        flatten_ty = orig_src_h
                    elif rotation == 270:
                        flatten_tx = orig_src_h
                    else:
                        raise ValueError("Rotation must be a multiple of 90 degrees.")
                    transform = transform.rotate(rot_deg).translate(flatten_tx, flatten_ty)

                # Add scale and position translate
                transform = transform.scale(scale, scale).translate(tx, ty)

                # Merge transformed source into the new page
                new_page.merge_transformed_page(src, transform)

            writer.add_page(new_page)

        # write output
        with open(output_pdf_path, "wb") as fout:
            writer.write(fout)

        print(f"Saved: {output_pdf_path}")
        print(f"Sheets produced: {len(writer.pages)} (each sheet is landscape with 2-up layout)")
        return True

    except Exception as exc:
        import traceback
        print("Error creating 2-up PDF:", exc)
        traceback.print_exc()
        return False

def convert_pdf_2_pages_per_sheet(input_path, output_path=None, page_format="A4"):
    """
    Main function to convert PDF to 2-pages-per-sheet format.
    
    Args:
        input_path (str): Path to input PDF
        output_path (str, optional): Path to output PDF. If None, adds '_2pp' suffix
        page_format (str): Output page format ("A4" or "Letter")
    """
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.")
        return False
    
    if output_path is None:
        base_name = os.path.splitext(input_path)[0]
        output_path = f"{base_name}_2pp.pdf"
    
    # Set page size based on format
    page_size = A4 if page_format.upper() == "A4" else letter
    
    print(f"Converting '{input_path}' to 2-pages-per-sheet format...")
    print(f"Output page format: {page_format} (landscape)")
    
    return create_2_pages_per_sheet(input_path, output_path, page_size)