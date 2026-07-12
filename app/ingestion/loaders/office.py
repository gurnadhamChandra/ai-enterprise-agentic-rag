import logfire
from unstructured.partition.auto import partition

def parse_office_files(file_path:str):
    """
    Parses Office files (Word, PowerPoint, PDF) using Unstructured.
    """
    with logfire.span("📄 Office Parsing", filename=file_path):
        try:
            elements = partition(filename=file_path)

            full_text = "\n".join([str(el) for el in elements])
            if not full_text.strip():
                logfire.warning(f"⚠️ Unstructured returned empty text for {file_path}")
            else:
                logfire.info(f"✅ Successfully parsed {len(full_text)} characters")

            return full_text
            
        except Exception as e:
            logfire.error(f"❌ Office Parse Failed", error=str(e))
            raise