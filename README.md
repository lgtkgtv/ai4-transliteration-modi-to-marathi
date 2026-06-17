# मोडी ते मराठी · modi-to-marathi

**Turn handwritten Modi-script documents into readable Marathi (Devanagari).**

<!-- edit: one honest line on why you started this -->
> I started this to help open up the millions of Modi documents that almost no
> one can read anymore — assisting the experts who can, not replacing them.

![How it works](assets/pipeline.excalidraw.svg)

## Start here

| You want to… | Go to |
|---|---|
| Run it on a Modi image | [`docs/quickstart.md`](docs/quickstart.md) |
| Know where the data comes from | [`docs/data.md`](docs/data.md) |
| Understand the model | [`docs/model.md`](docs/model.md) |
| See an example | [`examples/`](examples/) |

## What this is (and isn't)

It's an **assistive** transliteration pipeline: the model produces a first draft,
a human expert checks and corrects it, and those corrections improve the next
version. It is **not** an autonomous reader — historical records are too important
to trust to an unchecked model.

## Status

Early. Dataset and pipeline work in progress.

## Background & planning

The history of the Modi script, the concept primers, and the project planning docs
live in a separate companion handbook (kept out of this code repo on purpose).

## License

See [`LICENSE`](LICENSE).
