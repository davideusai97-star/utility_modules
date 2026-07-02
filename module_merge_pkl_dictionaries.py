#!/usr/bin/env python3
import pickle
import sys

'''merges 2 pickle dictionaries, sorting inner and middle keys. outer keys could change
positions due to comparisons. Gives in output a merged pickle dictionary'''

def load_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)

def main():
    if len(sys.argv) != 4:
        print("Usage: python merge_nested.py dict1.pkl dict2.pkl output.pkl")
        sys.exit(1)

    file1, file2, outfile = sys.argv[1], sys.argv[2], sys.argv[3]

    d1 = load_pickle(file1)
    d2 = load_pickle(file2)

    merged = {}

    # Loop outer keys
    for outer in set(d1) | set(d2):
        merged[outer] = {}

        # union of middle keys
        mids = set()
        if outer in d1:
            mids |= set(d1[outer])
        if outer in d2:
            mids |= set(d2[outer])

        # merge inner levels
        for mid in sorted(mids, key=float):
            inner1 = d1.get(outer, {}).get(mid, {})
            inner2 = d2.get(outer, {}).get(mid, {})

            # merge then sort
            merged_inner = {**inner1, **inner2}
            merged_inner = {k: merged_inner[k] for k in sorted(merged_inner)}

            merged[outer][mid] = merged_inner

    with open(outfile, "wb") as f:
        pickle.dump(merged, f)

    print("Merged written to", outfile)

if __name__ == "__main__":
    main()
