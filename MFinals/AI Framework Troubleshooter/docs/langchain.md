How to load PDFs
Portable Document Format (PDF), standardized as ISO 32000, is a file format developed by Adobe in 1992 to present documents, including text formatting and images, in a manner independent of application software, hardware, and operating systems.

This guide covers how to load PDF documents into the LangChain Document format that we use downstream.

Text in PDFs is typically represented via text boxes. They may also contain images. A PDF parser might do some combination of the following:

Agglomerate text boxes into lines, paragraphs, and other structures via heuristics or ML inference;
Run OCR on images to detect text therein;
Classify text as belonging to paragraphs, lists, tables, or other structures;
Structure text into table rows and columns, or key-value pairs.
LangChain integrates with a host of PDF parsers. Some are simple and relatively low-level; others will support OCR and image-processing, or perform advanced document layout analysis. The right choice will depend on your needs. Below we enumerate the possibilities.

