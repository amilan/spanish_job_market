#!/usr/bin/env python

import argparse
import pandas as pd


def main():
    """Combine two datasets."""
    parser = argparse.ArgumentParser(description="Combine two datasets.")
    parser.add_argument("dataset_1", type=str,
                        help="1st dataset to merge.")
    parser.add_argument("dataset_2", type=str,
                        help="2nd dataset to merge.")
    parser.add_argument("output", type=str,
                        help="Dataset combining the two inputs.")
    args = parser.parse_args()

    dataset_1 = pd.read_csv(args.dataset_1)
    dataset_2 = pd.read_csv(args.dataset_2)
    
    # we could drop na with:
    # dataset_1.dropna(axis=1)
    # dataset_2.dropna(axis=1)
    # but we will not do it here, as we will work later on the data cleaning.

    merged_dataset = dataset_1.append(dataset_2, ignore_index=True)
    merged_dataset.drop_duplicates()
    merged_dataset.to_csv(args.output, index=False)


if __name__ == '__main__':
    main()