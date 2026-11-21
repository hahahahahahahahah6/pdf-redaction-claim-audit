# Documentation claim auditor

An offline static auditor compares exact documentation claims with Python source patterns without executing inspected source. It scans the root README and Markdown under directories named docs, excluding fenced blocks; inline code counts. Normalization ignores case, expands contractions, replaces hyphens with spaces, and collapses whitespace. Denial spans are removed before positive matching.

```text
pdf-redaction-claim-audit audit [repo] [--json] [--verbose] [--ignore PREFIX] [--fail-on high|medium]
python3 -m pdf_redaction_claim_audit audit [repo]
documented-pdf-redaction-claim-false
documented-no-pdf-redaction-claim-false
```

The default failure threshold is high. A finding supported only by tests has medium severity. Exit status is 0 for pass, 2 for findings at the threshold, and 1 for usage or I/O errors. Ignore prefixes can be repeated. Source under fixtures, docs and examples is excluded; test files are reported separately. Symbolic links are excluded.

## Differentiation

The checked feature concerns removing page content; extraction, generation, merging, splitting, encryption, rotation, form filling, watermarking and electronic signatures are separate capabilities. This audit looks for the listed calls, not those adjacent operations.

## Limitations

This phrase

```text
pdf redaction
```

May name a roadmap item.

This phrase

```text
redact pdf
```

May describe a writer wrapper that never performs the checked operation.

This phrase

```text
remove text from pdf
```

May describe rebuilding a document without a page.

This phrase

```text
black out text in pdf
```

May describe a black rectangle that leaves text extractable.

This phrase

```text
redact sensitive information from pdf
```

May describe scrubbing metadata.

This phrase

```text
redact text in pdf
```

May describe a white rectangle hiding text.

This phrase

```text
add redaction to pdf
```

May describe an annotation that is never applied.

This phrase

```text
apply redaction to pdf
```

May describe a configuration flag.

This phrase

```text
redact pdf page
```

May describe deleting a whole page.

This phrase

```text
redact confidential information from pdf
```

May describe stripping metadata.

This phrase

```text
redact personal information from pdf
```

May describe anonymising a filename.

An opener and an unrelated annotation call in the same module count together.

The pair counts even if the annotation is never applied.

The pair counts even if the annotated rectangle is empty.

The dedicated redactor call counts even if its options have no content filters.

A generic named call counts even with no arguments.

A lone opener does not count.

An annotation call alone does not count.

An apply call alone does not count.

An opener with an apply call but no annotation does not count.

An opener with a save call alone does not count.

A scrub call alone does not count.

An opener with a scrub call but no annotation does not count.

Drawing a black rectangle alone does not count; covered text remains extractable.

Constructing options alone does not count.

A bare redactor name without the relevant import does not count.

pikepdf has no detected dedicated API.

pypdf has no detected dedicated API.

PyPDF2 has no detected dedicated API.

pdfrw has no detected dedicated API.

A writer that appends or merges whole files does not count.

A writer that adds pages does not count.

A writer that encrypts does not count.

A reader or writer that rotates pages does not count.

An opener with a page rotation call does not count.

A writer that updates form fields does not count.

A reader with a page merge call does not count.

An opener with a page overlay call does not count.

An opener with rotated text insertion does not count.

A pyhanko or endesive signing call does not count.

A reader alone does not count.

Document generation alone does not count.

Whole-file merging alone does not count.

Splitting alone does not count.

Encryption alone does not count.

Rotation alone does not count.

Form filling alone does not count.

Watermarking alone does not count.

Extraction alone does not count.

Electronic signature operations alone do not count.

External qpdf, pdftk and Ghostscript subprocesses do not count.

Mindee parsing with any product does not count.

Azure document analysis with any model does not count.

Veryfi calls of any kind do not count.

Google Document AI processing with any processor does not count.

Eden AI universal calls with any model do not count.

Textract calls of any kind do not count.

LlamaParse calls do not count.

Nanonets calls with opaque identifiers do not count.

Docsumo uploads do not count.

ABBYY Vantage calls with opaque identifiers do not count.

Rossum calls with opaque identifiers do not count.

Klippa calls with opaque identifiers do not count.

Parseur calls with opaque identifiers do not count.

Extend calls with opaque identifiers do not count.

Hand-written raw dictionary and content stream edits are missed.

A detected operation does not prove text is gone or unrecoverable.

Static patterns do not judge semantics.

Dead code counts.

Alias chains the tracer cannot follow are missed.

Only exact phrases match.

Denials depend on the listed phrases.

Each paired route must occur in one module.

PDF extraction claims are outside the phrase lists.

PDF generation claims are outside the phrase lists.

PDF merging claims are outside the phrase lists.

PDF splitting claims are outside the phrase lists.

PDF encryption claims are outside the phrase lists.

PDF rotation claims are outside the phrase lists.

PDF form filling claims are outside the phrase lists.

spreadsheet reading claims are outside the phrase lists.

spreadsheet generation claims are outside the phrase lists.

Word document reading claims are outside the phrase lists.

Word document generation claims are outside the phrase lists.

presentation reading claims are outside the phrase lists.

presentation generation claims are outside the phrase lists.

table extraction claims are outside the phrase lists.

invoice extraction claims are outside the phrase lists.

receipt extraction claims are outside the phrase lists.

ID document extraction claims are outside the phrase lists.

bank check extraction claims are outside the phrase lists.

bank statement extraction claims are outside the phrase lists.

tax form extraction claims are outside the phrase lists.

pay stub extraction claims are outside the phrase lists.

health insurance card extraction claims are outside the phrase lists.

business card extraction claims are outside the phrase lists.

credit card extraction claims are outside the phrase lists.

contract extraction claims are outside the phrase lists.

mortgage extraction claims are outside the phrase lists.

resume extraction claims are outside the phrase lists.

bill of lading extraction claims are outside the phrase lists.

delivery note extraction claims are outside the phrase lists.

carte grise extraction claims are outside the phrase lists.

energy bill extraction claims are outside the phrase lists.

marriage certificate extraction claims are outside the phrase lists.

bank account details extraction claims are outside the phrase lists.

nutrition facts label extraction claims are outside the phrase lists.

material certificate extraction claims are outside the phrase lists.

US mail extraction claims are outside the phrase lists.

invoice splitter claims are outside the phrase lists.

multi-receipts detection claims are outside the phrase lists.

French health card extraction claims are outside the phrase lists.

Indian passport extraction claims are outside the phrase lists.

driver license extraction claims are outside the phrase lists.

vaccination card extraction claims are outside the phrase lists.

document cropping claims are outside the phrase lists.

image rotation claims are outside the phrase lists.

e-signature claims are outside the phrase lists.

payment processing claims are outside the phrase lists.

OCR claims are outside the phrase lists.

PDF watermarking claims are outside the phrase lists.
