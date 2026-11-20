// Writes the entry image to the output directory.
//
// The image lives beside this program as entry.png. The grader runs this
// program twice in a fresh sandbox and both runs must produce the same
// bytes, so this program only copies the file: no drawing, no timestamps,
// no randomness.
import { closeSync, copyFileSync, mkdirSync, openSync, readSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
const source = join(here, "entry.png");
const target = join(outDir, "entry.png");

// The source must be a whole PNG: check the 8-byte signature before
// copying, so a corrupt or truncated file fails loudly here instead of
// reaching the judge as a broken image.
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const fd = openSync(source, "r");
const head = Buffer.alloc(8);
readSync(fd, head, 0, 8, 0);
closeSync(fd);
if (!head.equals(PNG_SIGNATURE)) {
  throw new Error("entry.png is not a valid PNG");
}
copyFileSync(source, target);

// Guard against a truncated copy: the run must fail loudly instead of
// submitting a partial image.
if (statSync(source).size !== statSync(target).size) {
  throw new Error("entry.png copy is incomplete");
}
