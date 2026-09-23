# Audio Analysis Ecosystem Review

This is an initial engineering review, not a substitute for checking exact versions before release.

## NumPy and SciPy

NumPy provides mature arrays and FFT primitives with a permissive BSD-style license. SciPy adds established signal-processing and statistical routines under a BSD-style license. They are the default research foundation because they are small enough for the current needs and straightforward to test numerically.

## aubio

aubio is focused on onset, pitch, beat, and tempo analysis, with C and Python interfaces and a GPL-3.0-or-later license. It is a plausible experimental backend for event/f0 detection, but GPL obligations require legal review for proprietary redistribution. Keep it behind an interface and compare its outputs against the current reference implementation before adopting it.

## Essentia

Essentia offers a large, mature C++/Python audio-analysis catalog and is attractive for specialized descriptors. It is primarily AGPL-3.0-or-later, with licensing implications for proprietary products. Its dependency/build surface is larger than Phase 1 needs. It is a candidate research comparison tool, not the default core dependency.

## libsndfile and bindings

libsndfile is a mature C library for common sound-file formats and is licensed under LGPL-2.1-or-later. It is a strong future option for broader PCM/float/container support and C++ integration. It is not needed while the standard-library PCM WAV reader covers the controlled corpus.

## Timbre Toolbox

Timbre Toolbox is useful as a reference point for timbre-analysis concepts and published methodology. Its MATLAB-centered distribution and workflow do not fit the current portable, reproducible Python/C++ direction, so it is not selected as a runtime dependency.

## Recommendation

Start with NumPy and the standard library, introduce SciPy when its tested routines remove meaningful custom code, and isolate optional aubio/Essentia/libsndfile adapters. Avoid implementing FFTs or mature file-format parsing ourselves. Implement the project-specific manifest model, event records, feature schema, provenance, aggregation, confound metadata, and report interpretation ourselves.
