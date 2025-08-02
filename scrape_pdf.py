from openai import OpenAI
import argparse
from pypdf import PdfReader
from olmocr.data.renderpdf import render_pdf_to_base64png


def prompt_text():
    return (
        "Attached is one page of a document that you must process. "
        "Just return the plain text representation of this document as if you were reading it naturally. Convert equations to LateX and tables to markdown.\n"
        "Return your output as markdown, with a front matter section on top specifying values for the primary_language, is_rotation_valid, rotation_correction, is_table, and is_diagram parameters."
    )


def build_page_query(args, pdf_path, page_number):
    image_base64 = render_pdf_to_base64png(pdf_path, page_number)
    return {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}},
                    {"type": "text", "text": prompt_text()},
                ],
            }
        ],
        "max_tokens": args.max_tokens,
        "temperature": args.temperature,
    }

def scrape_pdf_page(client, args, pdf_path, page_number):
    query = build_page_query(args, pdf_path, page_number)
    response = client.chat.completions.create(
        model=args.model,
        **query,
    )
    return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser(description='Extract text from PDF using OCR')
    parser.add_argument('--model', type=str, help='Model to use for OCR')
    parser.add_argument('--api-key', type=str, help='API key for the model')
    parser.add_argument('--pdf-path', type=str, help='Path to the PDF file')
    parser.add_argument('--max-tokens', type=int, default=4500, help='Maximum number of tokens to generate')
    parser.add_argument('--temperature', type=float, default=0.0, help='Temperature for the model')

    args = parser.parse_args()

    client = OpenAI(base_url="https://api.deepinfra.com/v1/openai", api_key=args.api_key)

    reader = PdfReader(args.pdf_path)
    page_count = reader.get_num_pages()

    result = []

    for page_number in range(1, page_count + 1):
        result.append(scrape_pdf_page(client, args, args.pdf_path, page_number))

    print(result)

    
if __name__ == "__main__":
    main()

