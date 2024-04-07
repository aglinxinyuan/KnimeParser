from zipfile import ZipFile

with ZipFile(filename) as zf:
    for filename in zf.namelist():
        if filename.count("/") == 1 and filename.endswith("workflow.knime"):
            parse(zf, filename)